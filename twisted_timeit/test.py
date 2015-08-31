# coding: UTF-8

__author__ = 'viator'

import logging
from StringIO import StringIO

from twisted.trial import unittest
from twisted.python import log
from tx_logging.observers import LevelFileLogObserver
from twisted.internet import defer

from twisted_timeit import twisted_timeit


def long_calculation(count=100000):
    a = 0
    for i in xrange(count):
        a = 1 + 1
    return a


class TwistedTimeitTest(unittest.TestCase):
    sep_line_one = '-' * 30
    sep_line_two = '=' * 30

    def setUp(self):
        self.count_run = 1000000
        self.count_iteration = 5

    def test_trivial(self):
        stdout = StringIO()
        log.addObserver(LevelFileLogObserver(stdout, logging.INFO))

        @twisted_timeit
        def trivial(count):
            return long_calculation(count)

        self.assertEqual(trivial(self.count_run), 2)
        result_log = stdout.getvalue()
        self.assertEqual('Time for function trivial' in result_log, True)
        print '\n', self.sep_line_two, '\nLog from test_trivial:\n', \
            self.sep_line_one, '\n', result_log, '\n', self.sep_line_two, '\n'

    def test_iteration(self):
        stdout = StringIO()
        log.addObserver(LevelFileLogObserver(stdout, logging.INFO))

        @twisted_timeit
        def iteration(count_iteration, count_run):
            for i in xrange(count_iteration):
                yield long_calculation(count_run)

        for i in iteration(self.count_iteration, self.count_run):
            self.assertEqual(i, 2)

        result_log = stdout.getvalue()
        self.assertEqual('Time for iterator iteration' in result_log, True)
        print '\n', self.sep_line_two, '\nLog from test_iteration:\n', \
            self.sep_line_one, '\n', result_log, '\n', self.sep_line_two, '\n'

    def test_deferred(self):
        stdout = StringIO()
        log.addObserver(LevelFileLogObserver(stdout, logging.INFO))
        self.call_count = 0

        def test_result(d, count):
            long_calculation(count)
            self.call_count += 1


        @twisted_timeit
        def defer_calc(count_iteration, count_run):
            d = defer.Deferred()
            for i in xrange(count_iteration):
                d.addCallback(test_result, count_run)
            return d

        d = defer_calc(self.count_iteration, self.count_run)
        d.callback(None)

        self.assertEqual(self.call_count, self.count_iteration)

        result_log = stdout.getvalue()
        self.assertEqual('Time for deferred' in result_log, True)
        print '\n', self.sep_line_two, '\nLog from test_deferred:\n', \
            self.sep_line_one, '\n', result_log, '\n', self.sep_line_two, '\n'

    def test_inline_callbacks_after(self):
        stdout = StringIO()
        log.addObserver(LevelFileLogObserver(stdout, logging.INFO))
        self.call_long = 0

        @defer.inlineCallbacks
        @twisted_timeit
        def yelding_calculation(count_iteration, count_run):
            for i in xrange(count_iteration):
                self.call_long += 1
                yield long_calculation(count_run)

        yelding_calculation(self.count_iteration, self.count_run)
        self.assertEqual(self.count_iteration, self.call_long)
        result_log = stdout.getvalue()
        self.assertEqual('Time for iterator yelding_calculation.send' in result_log, True)
        print '\n', self.sep_line_two, '\nLog from test_inline_callbacks [AFTER]:\n', \
            self.sep_line_one, '\n', result_log, '\n', self.sep_line_two, '\n'

    def test_inline_callbacks_before(self):
        stdout = StringIO()
        log.addObserver(LevelFileLogObserver(stdout, logging.INFO))
        self.call_long = 0

        @twisted_timeit
        @defer.inlineCallbacks
        def yelding_calculation(count_iteration, count_run):
            for i in xrange(count_iteration):
                self.call_long += 1
                yield long_calculation(count_run)

        yelding_calculation(self.count_iteration, self.count_run)
        self.assertEqual(self.count_iteration, self.call_long)
        result_log = stdout.getvalue()
        self.assertEqual('Time for function yelding_calculation' in result_log, True)
        print '\n', self.sep_line_two, '\nLog from test_inline_callbacks [BEFORE]:\n', \
            self.sep_line_one, '\n', result_log, '\n', self.sep_line_two, '\n'
