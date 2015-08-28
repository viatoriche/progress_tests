__author__ = 'viator'

class replace_exception(object):

    def __init__(self, exception=KeyError):
        self.exception = exception

    def __call__(self, cls):
        def __getattr__(self, name):
            raise self.exception

        cls.exception = self.exception
        cls.__getattr__ = __getattr__
        return cls

@replace_exception(KeyError)
class A(object):
    pass

a = A()
try:
    a.test()
except KeyError:
    print 'Cool'
