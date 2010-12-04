# coding: UTF-8

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

