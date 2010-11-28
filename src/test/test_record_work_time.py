# coding: UTF-8

# Unit test for record_work_time.py.

import create_work_record
import work_recorder
import record_work_time

from datetime import date
import os.path
import sqlite3
import tempfile
import unittest

class TestDayConverting(unittest.TestCase):
    def test_format_yyyymmdd(self):
        self.assertEquals(u'2010-11-28',
                record_work_time.convert_day(u'20101128'))

    def test_format_mmdd(self):
        today = date.today()
        self.assertEquals(u'%s-11-28' % today.year,
                record_work_time.convert_day(u'1128'))

    def test_format_mdd(self):
        today = date.today()
        self.assertEquals(u'%s-01-28' % today.year,
                record_work_time.convert_day(u'128'))

    def check_invalid(self, date_string):
        try:
            date = record_work_time.convert_day(date_string)
            self.fail(date)
        except record_work_time.InvalidArgumentFormatException:
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
        self.assertEquals(u'17:35:00', record_work_time.convert_time(u'1735'))

    def test_format_hmm(self):
        self.assertEquals(u'05:35:00', record_work_time.convert_time(u'535'))

    def check_invalid(self, time_string):
        try:
            time = record_work_time.convert_time(time_string)
            self.fail(time)
        except record_work_time.InvalidArgumentFormatException:
            pass

    def test_invalid_format_mm(self):
        self.check_invalid(u'35')

    def test_invalid_format_hhhmm(self):
        self.check_invalid(u'11755')

    def test_invalid_time(self):
        self.check_invalid(u'2501')

class TestConvertingWorkTimes(unittest.TestCase):
    def test_one(self):
        project = u'pro'
        work_times = record_work_time.convert_work_times(
                project, u'20101128', [u'900', u'1200'])
        self.assertEquals(1, len(work_times))
        a_work_time = work_times[0]
        self.assertEquals(
                project, a_work_time[record_work_time.WORK_TIME_KEY_PROJECT])
        self.assertEquals(
                u'2010-11-28', a_work_time[record_work_time.WORK_TIME_KEY_DAY])
        self.assertEquals(
                u'09:00:00', a_work_time[record_work_time.WORK_TIME_KEY_START])
        self.assertEquals(
                u'12:00:00', a_work_time[record_work_time.WORK_TIME_KEY_END])
    
    def test_two(self):
        project = u'pro'
        work_times = record_work_time.convert_work_times(
                project, u'20101128', [u'900', u'1200', u'1310', u'2059'])
        self.assertEquals(2, len(work_times))

        except_day = u'2010-11-28'
        a_work_time = work_times[0]
        self.assertEquals(
                project, a_work_time[record_work_time.WORK_TIME_KEY_PROJECT])
        self.assertEquals(
                except_day, a_work_time[record_work_time.WORK_TIME_KEY_DAY])
        self.assertEquals(
                u'09:00:00', a_work_time[record_work_time.WORK_TIME_KEY_START])
        self.assertEquals(
                u'12:00:00', a_work_time[record_work_time.WORK_TIME_KEY_END])

        a_work_time = work_times[1]
        self.assertEquals(
                project, a_work_time[record_work_time.WORK_TIME_KEY_PROJECT])
        self.assertEquals(
                except_day, a_work_time[record_work_time.WORK_TIME_KEY_DAY])
        self.assertEquals(
                u'13:10:00', a_work_time[record_work_time.WORK_TIME_KEY_START])
        self.assertEquals(
                u'20:59:00', a_work_time[record_work_time.WORK_TIME_KEY_END])

    def test_invalid_year(self):
        try:
            record_work_time.convert_work_times(
                u'project', u'20103028', [u'900', u'1200', u'1310', u'2059'])
            self.fail()
        except record_work_time.InvalidArgumentFormatException:
            pass

    def test_invalid_day_count(self):
        try:
            record_work_time.convert_work_times(
                u'project', u'20101128', [u'900', u'1200', u'1310'])
            self.fail()
        except record_work_time.InvalidArgumentFormatException:
            pass

    def test_invalid_time(self):
        try:
            record_work_time.convert_work_times(
                u'project', u'20101128', [u'7000', u'1200'])
            self.fail()
        except record_work_time.InvalidArgumentFormatException:
            pass

    def test_invalid_time_order_when_one(self):
        try:
            record_work_time.convert_work_times(
                u'project', u'20101128', [u'1200', u'1159'])
            self.fail()
        except record_work_time.InvalidArgumentFormatException:
            pass

    def test_invalid_time_order_when_two(self):
        try:
            record_work_time.convert_work_times(
                u'project', u'20101128', [u'1100', u'1159', u'110', u'1200'])
            self.fail()
        except record_work_time.InvalidArgumentFormatException:
            pass

class TestRecordingWorkTimes(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(u':memory:')
        create_work_record.create_database(self.conn)       

    def test_record_a_work_time(self):
        project = u'project'
        work_times = record_work_time.convert_work_times(
                project, u'20101128', [u'910', u'1250'])
        record_work_time.record_work_times(work_times, self.conn)

        cursor = self.conn.execute(
                u'select {project}, {day}, {start}, {end} from {table}'.format(
                    project = work_recorder.COLUMN_PROJECT,
                    day = work_recorder.COLUMN_DAY,
                    start = work_recorder.COLUMN_START,
                    end = work_recorder.COLUMN_END,
                    table = work_recorder.TABLE_WORK_TIME))
        result = cursor.fetchall()
        self.assertEquals(1, len(result))
        a_row = result[0]
        self.assertEquals(
                (project, u'2010-11-28', u'09:10:00', u'12:50:00'),
                a_row)

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()

