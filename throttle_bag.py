import time
import datetime
import bisect

__version__ = '0.1'


class Throttle(object):
    def __init__(self, obj, seconds, times=1, *args, **kwargs):
        self._obj = obj
        self._seconds = seconds
        self._times = times
        self._calls = []

    def _delay(self, seconds):
        time.sleep(seconds)

    def __getattr__(self, name):
        if self._times == 1:
            self._delay(self._seconds)
        else:
            now = datetime.datetime.utcnow().timestamp()
            start_time = now - self._seconds
            i = bisect.bisect_left(self._calls, start_time)
            self._calls = self._calls[i:]
            if len(self._calls) >= self._times:
                wait_time = self._seconds - (now - self._calls[0])
                self._delay(wait_time)
                now = datetime.datetime.utcnow().timestamp()
            self._calls.append(now)

        return self._obj.__getattribute__(name)
