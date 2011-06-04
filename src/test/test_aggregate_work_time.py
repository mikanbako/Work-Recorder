#!/usr/bin/env python
# coding: UTF-8

# The MIT License
# 
# Copyright (c) 2011 Keita Kita
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# 
# THE SOFTWARE.

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

