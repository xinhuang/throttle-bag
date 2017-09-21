import datetime


class ThrottledException(Exception):
    pass


class ThrottledServer(object):
    def __init__(self, seconds, times=1):
        self._seconds = seconds
        self._times = times
        self._calls = []

    def _check(self):
        now = self.now()
        if self._times == 1:
            for c in self._calls:
                if now - c < self._seconds:
                    raise ThrottledException(now - c)
            self._calls.append(now)
        else:
            self._calls.append(now)
            self._calls = [c for c in self._calls if now - c < self._seconds]
            if len(self._calls) > self._times:
                msg = 'too many invocations in a short time: {}'.format(
                    len(self._calls))
                raise ThrottledException(msg)
        return now

    def now(self):
        return datetime.datetime.utcnow().timestamp()

    def foo(self):
        return self._check()

    def bar(self):
        return self._check()
