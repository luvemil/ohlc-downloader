import unittest

import datetime as dt
from dateutil import parser, tz
from dateutil.tz import tzlocal

from utils.functions import *

class ParitioningFunctionTest(unittest.TestCase):
    def test_round_timeframe_notz(self):
        tf = '5m'
        ts_dt = parser.parse('2019-01-01 15:46')
        ts_floor_dt = parser.parse('2019-01-01 15:45')
        ts_ceil_dt = parser.parse('2019-01-01 15:50')

        res_floor = round_timeframe(ts_dt,tf)
        res_ceil = round_timeframe(ts_dt,tf,'CEIL')

        self.assertEqual(res_floor,ts_floor_dt)
        self.assertEqual(res_ceil,ts_ceil_dt)

    def test_round_timeframe_tz(self):
        tf = '5m'
        ts_dt = parser.parse('2019-01-01 15:46 Z')
        ts_floor_dt = parser.parse('2019-01-01 15:45 Z')
        ts_ceil_dt = parser.parse('2019-01-01 15:50 Z')

        res_floor = round_timeframe(ts_dt,tf)
        res_ceil = round_timeframe(ts_dt,tf,'CEIL')

        self.assertEqual(res_floor,ts_floor_dt)
        self.assertEqual(res_ceil,ts_ceil_dt)

    def test_interval_creation(self):
        tf = '5m'
        start_time = '2019-01-01 15:46 Z'
        end_time = '2019-01-01 17:59 Z'

        expected_res = [ parser.parse(x) for x in [
            '2019-01-01 15:45 Z',
            '2019-01-01 16:45 Z',
            '2019-01-01 17:45 Z',
            '2019-01-01 18:00 Z'
        ]]

        res = create_intervals(start_time,end_time,tf,12)

        self.assertSequenceEqual(expected_res,res)

    # TODO:
    # - add test for raising correcly

if __name__ == "__main__":
    unittest.main()
