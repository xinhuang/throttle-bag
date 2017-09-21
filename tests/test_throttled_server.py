from .throttled_server import ThrottledServer, ThrottledException

import time
import unittest
import asyncio


class ThrottledServerTestSuite(unittest.TestCase):
    def test_given_1_api_throttled_by_1ms_when_sleep_enough_time(self):
        seconds = 0.001
        sut = ThrottledServer(seconds=seconds)

        for i in range(1, 5):
            sut.foo()
            time.sleep(seconds)

    def test_given_1_api_throttled_by_1ms_when_not_sleep_enough_time(self):
        seconds = 0.001
        sut = ThrottledServer(seconds=seconds)

        sut.foo()
        self.assertRaises(ThrottledException, sut.foo)

    def test_given_2_api_throttled_by_1ms_when_sleep_enough_time(self):
        seconds = 0.001
        sut = ThrottledServer(seconds=seconds)
        for i in range(1, 5):
            t0 = sut.foo()
            time.sleep(seconds)
            t1 = sut.bar()
            self.assertGreaterEqual(t1 - t0, seconds)
            time.sleep(seconds)

    def test_given_2_api_throttled_by_1ms_when_not_sleep_enough_time(self):
        seconds = 0.001
        sut = ThrottledServer(seconds=seconds)

        sut.foo()
        time.sleep(seconds / 2)
        self.assertRaises(ThrottledException, sut.bar)

    def test_given_freq_10ms_twice_when_fire_10ms_once(self):
        seconds = 0.01
        times = 2
        sut = ThrottledServer(seconds=seconds, times=times)

        for i in range(1, 5):
            sut.foo()
            time.sleep(seconds / 2)

    def test_given_freq_10ms_twice_when_fire_all_at_once_then_sleep(self):
        seconds = 0.01
        times = 2
        sut = ThrottledServer(seconds=seconds, times=times)

        for i in range(1, 5):
            t0 = sut.foo()
            t1 = sut.foo()
            self.assertLess(t1 - t0, seconds)
            time.sleep(seconds)

    def sync(self, coroutine):
        asyncio.get_event_loop().run_until_complete(coroutine)

    def test_given_1_async_api_throttled_by_1ms_when_sleep_enough_time(self):
        async def wrapper():
            seconds = 0.001
            sut = ThrottledServer(seconds=seconds)

            for i in range(1, 5):
                await sut.async_foo()
                await asyncio.sleep(seconds)

        self.sync(wrapper())

    def test_given_1_async_api_throttled_by_1ms_when_not_sleep_enough_time(self):
        async def wrapper():
            seconds = 0.001
            sut = ThrottledServer(seconds=seconds)

            await sut.async_foo()
            try:
                await sut.async_foo()
                exception_caught = False
            except ThrottledException:
                exception_caught = True
            self.assertTrue(exception_caught)

        self.sync(wrapper())

    def test_given_2_async_apis_throttled_by_1ms_when_sleep_enough_time(self):
        async def wrapper():
            seconds = 0.001
            sut = ThrottledServer(seconds=seconds)
            for i in range(1, 5):
                t0 = await sut.async_foo()
                await asyncio.sleep(seconds)
                t1 = await sut.async_bar()
                self.assertGreaterEqual(t1 - t0, seconds)
                await asyncio.sleep(seconds)

        self.sync(wrapper())

    def test_given_2_api_throttled_by_1ms_when_not_sleep_enough_time(self):
        async def wrapper():
            seconds = 0.001
            sut = ThrottledServer(seconds=seconds)

            await sut.async_foo()
            time.sleep(seconds / 2)
            try:
                await sut.async_bar()
                exception_caught = False
            except ThrottledException:
                exception_caught = True
            self.assertTrue(exception_caught)

        self.sync(wrapper())

    def test_given_freq_10ms_twice_when_fire_10ms_once(self):
        async def wrapper():
            seconds = 0.01
            times = 2
            sut = ThrottledServer(seconds=seconds, times=times)

            for i in range(1, 5):
                await sut.async_foo()
                await asyncio.sleep(seconds / 2)

        self.sync(wrapper())

    def test_given_freq_10ms_twice_when_fire_all_at_once_then_sleep(self):
        async def wrapper():
            seconds = 0.01
            times = 2
            sut = ThrottledServer(seconds=seconds, times=times)

            for i in range(1, 5):
                t0 = await sut.async_foo()
                t1 = await sut.async_foo()
                self.assertLess(t1 - t0, seconds)
                await asyncio.sleep(seconds)

        self.sync(wrapper())
