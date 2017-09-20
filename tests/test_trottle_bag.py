from .context import *

import unittest
import datetime

calls = []

def now():
    return datetime.datetime.utcnow().timestamp()

class ApiObj(object):
    def foo(self):
        global calls
        calls.append(now())

class ThrottleBagTestSuite(unittest.TestCase):
    def setUp(self):
        global calls
        calls = []

    def check_calls(self, interval):
        l = calls[:-1]
        r = calls[1:]
        for t0, t1 in zip(l, r):
            self.assertLess(interval, t1 - t0)

    def test_given_1_obj_by_throttle_by_10ms(self):
        sut = Throttler(ApiObj()).interval(0.01)

        [sut.foo() for i in range(1, 5)]

        self.check_calls(0.01)
