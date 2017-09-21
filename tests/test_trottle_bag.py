from .context import *
from .throttled_server import ThrottledServer

import unittest


class ThrottleTestSuite(unittest.TestCase):

    def test_given_1_api_when_call_once_every_10ms(self):
        seconds = 0.001
        sut = Throttle(ThrottledServer(seconds=seconds),
                       seconds=seconds)

        [sut.foo() for i in range(1, 5)]

    def test_given_1_api_when_call_2_times_in_10ms(self):
        seconds = 0.001
        times = 2
        sut = Throttle(ThrottledServer(seconds=seconds, times=times),
                       seconds=seconds, times=2)

        t0 = sut.foo()
        t1 = sut.foo()
        self.assertLess(t1 - t0, seconds)
        t0 = sut.foo()
        t1 = sut.foo()
        self.assertLess(t1 - t0, seconds)

    def test_given_2_apis_when_call_2_times_in_10ms(self):
        seconds = 0.001
        times = 2
        sut = Throttle(ThrottledServer(seconds=seconds, times=times),
                       seconds=seconds, times=2)

        t0 = sut.foo()
        t1 = sut.bar()
        self.assertLess(t1 - t0, seconds)
        t0 = sut.bar()
        t1 = sut.foo()
        self.assertLess(t1 - t0, seconds)

    def sync(self, coroutine):
        asyncio.get_event_loop().run_until_complete(coroutine)

    def test_given_1_async_api_when_call_once_every_10ms(self):
        async def wrapper():
            seconds = 0.001
            sut = Throttle(ThrottledServer(seconds=seconds),
                           seconds=seconds, aio=True)
            await sut.async_foo()

        self.sync(wrapper())

    def test_given_1_async_apis_when_call_2_times_in_10ms(self):
        async def wrapper():
            seconds = 0.001
            times = 2
            sut = Throttle(ThrottledServer(seconds=seconds, times=times),
                           seconds=seconds, times=2, aio=True)

            t0 = await sut.async_foo()
            t1 = await sut.async_foo()
            self.assertLess(t1 - t0, seconds)
            t0 = await sut.async_foo()
            t1 = await sut.async_foo()
            self.assertLess(t1 - t0, seconds)

        self.sync(wrapper())

    def test_given_2_async_apis_when_call_2_times_in_10ms(self):
        async def wrapper():
            seconds = 0.001
            times = 2
            sut = Throttle(ThrottledServer(seconds=seconds, times=times),
                           seconds=seconds, times=2, aio=True)

            t0 = await sut.async_foo()
            t1 = await sut.async_bar()
            self.assertLess(t1 - t0, seconds)
            t0 = await sut.async_bar()
            t1 = await sut.async_foo()
            self.assertLess(t1 - t0, seconds)

        self.sync(wrapper())
