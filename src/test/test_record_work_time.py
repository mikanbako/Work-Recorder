#!/usr/bin/env python
# coding: UTF-8

# Unit test for record_work_time.py.

import create_work_record
import work_recorder
import record_work_time

import os.path
import sqlite3
import unittest

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
        except work_recorder.InvalidArgumentFormatException:
            pass

    def test_invalid_day_count(self):
        try:
            record_work_time.convert_work_times(
                u'project', u'20101128', [u'900', u'1200', u'1310'])
            self.fail()
        except work_recorder.InvalidArgumentFormatException:
            pass

    def test_invalid_time(self):
        try:
            record_work_time.convert_work_times(
                u'project', u'20101128', [u'7000', u'1200'])
            self.fail()
        except work_recorder.InvalidArgumentFormatException:
            pass

    def test_invalid_time_order_when_one(self):
        try:
            record_work_time.convert_work_times(
                u'project', u'20101128', [u'1200', u'1159'])
            self.fail()
        except work_recorder.InvalidArgumentFormatException:
            pass

    def test_invalid_time_order_when_two(self):
        try:
            record_work_time.convert_work_times(
                u'project', u'20101128', [u'1100', u'1159', u'110', u'1200'])
            self.fail()
        except work_recorder.InvalidArgumentFormatException:
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

