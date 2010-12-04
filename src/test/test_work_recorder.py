# coding: UTF-8

# Unit test for work_recorder.py.

import work_recorder

from datetime import date
import unittest

class TestDayConverting(unittest.TestCase):
    def test_format_yyyymmdd(self):
        self.assertEquals(u'2010-11-28',
                work_recorder.convert_day(u'20101128'))

    def test_format_mmdd(self):
        today = date.today()
        self.assertEquals(u'%s-11-28' % today.year,
                work_recorder.convert_day(u'1128'))

    def test_format_mdd(self):
        today = date.today()
        self.assertEquals(u'%s-01-28' % today.year,
                work_recorder.convert_day(u'128'))

    def check_invalid(self, date_string):
        try:
            date = work_recorder.convert_day(date_string)
            self.fail(date)
        except work_recorder.InvalidArgumentFormatException:
            pass

    def test_invalid_format_yyymmdd(self):
        self.check_invalid(u'0101128')

    def test_invalid_format_yyyyymmdd(self):
        self.check_invalid(u'200101128')

    def test_invalid_format_dd(self):
        self.check_invalid(u'28')

    def test_invalid_day(self):
        self.check_invalid(u'20100232')

class TestTimeConverting(unittest.TestCase):
    def test_format_hhmm(self):
        self.assertEquals(u'17:35:00', work_recorder.convert_time(u'1735'))

    def test_format_hmm(self):
        self.assertEquals(u'05:35:00', work_recorder.convert_time(u'535'))

    def check_invalid(self, time_string):
        try:
            time = work_recorder.convert_time(time_string)
            self.fail(time)
        except work_recorder.InvalidArgumentFormatException:
            pass

    def test_invalid_format_mm(self):
        self.check_invalid(u'35')

    def test_invalid_format_hhhmm(self):
        self.check_invalid(u'11755')

    def test_invalid_time(self):
        self.check_invalid(u'2501')

if __name__ == '__main__':
    unittest.main()

