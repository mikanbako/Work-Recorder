#!/usr/bin/env python
# coding: UTF-8

import os
import os.path
import sqlite3

import work_recorder

class FileAlreadyExistsException(Exception):
    u"""
    Exception that represetns the database file for work recorder that
    will be created already exists.
    """
    pass

def create_database(conn):
    u"""
    Create database for work recorder.

    Parameters:
        conn : Connection object of sqlite3.
    """
    conn.execute(
            u"""
            create table {table_name} (
                {day} text,
                {start} text,
                {end} text not null,
                {project} textn not null,
                {comment} text default '' not null,
                primary key (day, start)
            )
            """.format(table_name = work_recorder.TABLE_WORK_TIME,
                    day = work_recorder.COLUMN_DAY,
                    start = work_recorder.COLUMN_START,
                    end = work_recorder.COLUMN_END,
                    project = work_recorder.COLUMN_PROJECT,
                    comment = work_recorder.COLUMN_COMMENT)
        )

def create_dbfile(path):
    u"""
    Create a database file.

    If file exists, raise FileAlreadyExistsException.

    Parameters:
        path : a path of a database file that will be created.
    """
    if (os.path.exists(path)):
        raise FileAlreadyExistsException()

    with sqlite3.connect(path) as conn:
        create_database(conn)

def main():
    u"""
    Create a database file for work recorder.
    """
    dbfile_path = os.path.join(os.getcwdu(), work_recorder.DATABASE_FILE_NAME)
    try:
        create_dbfile(dbfile_path)
        print u'Database file ({dbfile}) is created.'.format(dbfile = dbfile_path)
    except FileAlreadyExistsException:
        print u'File {dbfile} already exists.'.format(dbfile = dbfile_path)
    except:
        print u'Cannot create a database file because an error occurred.'
        raise
if __name__ == '__main__':
    main()

