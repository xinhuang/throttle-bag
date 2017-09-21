import time
import datetime
import bisect
import asyncio

__version__ = '0.2'


class Throttle(object):
    def __init__(self, obj, seconds, times=1, aio=False, loop=None):
        if asyncio:
            self._loop = loop if loop else asyncio.get_event_loop()
        else:
            self._loop = None
        self._obj = obj
        self._seconds = seconds
        self._times = times
        self._calls = []

    def _delay(self, seconds):
        if seconds:
            time.sleep(seconds)
        if self._times > 1:
            now = datetime.datetime.utcnow().timestamp()
            self._calls.append(now)

    async def _async_delay(self, seconds):
        assert self._loop
        if seconds:
            await asyncio.sleep(seconds, self._loop)
        if self._times > 1:
            now = datetime.datetime.utcnow().timestamp()
            self._calls.append(now)

    def __getattr__(self, name):
        wait_time = None
        if self._times == 1:
            wait_time = self._seconds
        else:
            now = datetime.datetime.utcnow().timestamp()
            start_time = now - self._seconds
            i = bisect.bisect_left(self._calls, start_time)
            self._calls = self._calls[i:]
            if len(self._calls) >= self._times:
                wait_time = self._seconds - (now - self._calls[0])

        attr = self._obj.__getattribute__(name)
        if not callable(attr):
            self._delay(wait_time)
            return attr
        else:
            if not asyncio.iscoroutinefunction(attr):
                self._delay(wait_time)
                return attr
            else:
                def decorate(async_func, wait_time):
                    async def wrapper(*args, **kwargs):
                        await self._async_delay(wait_time)
                        return await async_func(*args, **kwargs)
                    return wrapper
                return decorate(attr, wait_time)
