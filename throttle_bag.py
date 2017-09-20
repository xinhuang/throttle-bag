import time

class Throttler(object):
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        time.sleep(0.01)
        return self._obj.__getattribute__(name)

    def interval(self, value):
        return self

