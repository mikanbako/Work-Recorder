# coding: UTF-8

# Unit test for aggregate_work_time.py.

import aggregate_work_time
import create_work_record
import work_recorder
import record_work_time

import os.path
import sqlite3
import unittest

class TestRecordingWorkTimes(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(u':memory:')
        create_work_record.create_database(self.conn)       

    def assert_time(self, month, project, hours, time):
        self.assertEquals(month, time[aggregate_work_time.TIME_KEY_MONTH])
        self.assertEquals(project, time[aggregate_work_time.TIME_KEY_PROJECT])
        self.assertEquals(hours, time[aggregate_work_time.TIME_KEY_HOURS])

    def test_aggregate_normal(self):
        record_work_time.record_work_times(
                record_work_time.convert_work_times(
                    u'projectB', u'20101027',
                    [u'900', u'1300', u'1400', u'1900']),
                self.conn)
        record_work_time.record_work_times(
                record_work_time.convert_work_times(
                    u'projectA', u'20101128',
                    [u'900', u'1200', u'1300', u'1800']),
                self.conn)
        record_work_time.record_work_times(
                record_work_time.convert_work_times(
                    u'projectB', u'20101129',
                    [u'900', u'1300', u'1400', u'1900']),
                self.conn)
        record_work_time.record_work_times(
                record_work_time.convert_work_times(
                    u'projectA', u'20101130',
                    [u'900', u'1200', u'1300', u'1800']),
                self.conn)
        times = aggregate_work_time.aggregate_work_time(
                u'2010-10-01', u'2010-11-30', self.conn)
        self.assertEquals(3, len(times))
        self.assert_time(u'2010-10', u'projectB', 9, times[0])
        self.assert_time(u'2010-11', u'projectA', 16, times[1])
        self.assert_time(u'2010-11', u'projectB', 9, times[2])

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()

