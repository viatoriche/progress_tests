# coding: utf-8
__author__ = 'viator'

import datetime
import collections
import types

import tx_logging
from twisted.internet import defer


LOG = tx_logging.getLogger(__name__)

def log_timeit(f, *args, **kwargs):
    pattern_info = kwargs.pop('pattern_info', 'Time for {}: {}'.format(repr(f), '{:.5f}s'))

    start_time = datetime.datetime.now()
    result = f(*args, **kwargs)
    stop_time = datetime.datetime.now()

    time_info = pattern_info.format(
        (stop_time - start_time).total_seconds(),
    )

    LOG.info(time_info)
    return result

class IterationWrapper(object):
    def __init__(self, iterator):
        self.iterator = iterator

    def __iter__(self):
        return self

    def next(self, *args, **kwargs):
        return log_timeit(
            self.iterator.next,
            *args,
            pattern_info='Time for iterator {}.next: {}'.format(self.iterator.__name__, '{:.5f}s'),
            **kwargs
        )

    @property
    def __class__(self):
        return types.GeneratorType

    def send(self, *args, **kwargs):
        return log_timeit(
            self.iterator.send,
            *args,
            pattern_info='Time for iterator {}.send: {}'.format(self.iterator.__name__, '{:.5f}s'),
            **kwargs
        )


class DeferredWrapper(object):
    def __init__(self, deferred):
        self.wrapped_deferred = deferred

    def callback(self, result):
        return log_timeit(
            self.wrapped_deferred.callback,
            result,
            pattern_info='Time for deferred: {:.5f}s',
        )


def twisted_timeit(f, *args, **kwargs):
    def wrapper():
        result = log_timeit(
            f,
            *args,
            pattern_info='Time for function {}: {}'.format(f.__name__, '{:.5f}s'),
            **kwargs
        )
        if isinstance(result, collections.Iterable):
            result = IterationWrapper(result)
        elif isinstance(result, defer.Deferred):
            result = DeferredWrapper(result)

        return result

    return wrapper

