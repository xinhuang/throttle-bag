from .throttled_server import ThrottledServer, ThrottledException

import time
import unittest


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
        time.sleep(seconds / 2)
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
