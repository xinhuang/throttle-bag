import time

class Throttler(object):
    def __init__(self, obj, seconds, *args, **kwargs):
        self._obj = obj
        self._seconds = seconds

    def __getattr__(self, name):
        time.sleep(self._seconds)
        return self._obj.__getattribute__(name)

