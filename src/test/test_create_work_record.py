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

# Unit test for create_work_record.py.

import work_recorder
import create_work_record
import os.path
import sqlite3
import tempfile
import unittest

class TestCreatedDbFile(unittest.TestCase):
    def setUp(self):
        (fd, path) = tempfile.mkstemp()
        os.fdopen(fd).close()
        if os.path.exists(path):
            os.remove(path)
        self.db_file_path = path

    def test_create_database(self):
        create_work_record.create_dbfile(self.db_file_path)
        with sqlite3.connect(self.db_file_path) as conn:
            conn.execute(u'select * from {table}'.format(
                table = work_recorder.TABLE_WORK_TIME))

    def test_create_database_if_file_exists(self):
        create_work_record.create_dbfile(self.db_file_path)
        try:
            create_work_record.create_dbfile(self.db_file_path)
            fail()
        except create_work_record.FileAlreadyExistsException:
            pass

    def tearDown(self):
        if os.path.exists(self.db_file_path):
            os.remove(self.db_file_path)

if __name__ == '__main__':
    unittest.main()

