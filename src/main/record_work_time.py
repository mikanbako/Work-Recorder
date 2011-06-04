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

from datetime import date, datetime
import argparse
import os
import os.path
import re
import sqlite3
import sys

import work_recorder

# Key of project in a work time.
# Value is a string.
WORK_TIME_KEY_PROJECT = u'project'

# Key of day in a work time.
# Value is a string. Format is YYYY-MM-DD.
WORK_TIME_KEY_DAY = u'day'

# Key of start time in a work time.
# Value is a string. Format is HH:MM:SS.
WORK_TIME_KEY_START = u'start'

# Key of end time in a work time.
# Value is a string. Format is HH:MM:SS.
WORK_TIME_KEY_END = u'end'

def convert_work_times(project, day_string, time_strings):
    u"""
    Convert the arguments to work times.

    If this method could not convert, raise InvalidArgumentFormatException.

    Parameters:
        project : Name of the project.
        day_string : String of the day.
        time_strings : List of string of the times.
    Return:
        A list of work time dictionary.
    """
    # Time are pairs of start and end.
    # Therefore, the number of times should be an even number.
    if len(time_strings) % 2:
        raise work_recorder.InvalidArgumentFormatException()

    day = work_recorder.convert_day(day_string)

    times = [work_recorder.convert_time(a_time_string)
            for a_time_string in time_strings]

    # Input times should be sorted.
    if times != sorted(times):
        raise work_recorder.InvalidArgumentFormatException()

    start_times = []
    end_times = []
    time_count = 0
    for a_time in times:
        if time_count % 2:
            end_times.append(a_time)
        else:
            start_times.append(a_time)
        time_count += 1

    work_times = []
    for index in range(len(start_times)):
        a_work_time = {}
        a_work_time[WORK_TIME_KEY_PROJECT] = project
        a_work_time[WORK_TIME_KEY_DAY] = day
        a_work_time[WORK_TIME_KEY_START] = start_times[index]
        a_work_time[WORK_TIME_KEY_END] = end_times[index]
        work_times.append(a_work_time)

    return work_times

def record_work_times(work_times, conn):
    u"""
    Record work times to database.

    Parameters:
        work_times : A list of work times.
        conn : Connection of database.
    """
    for a_work_time in work_times:
        conn.execute(
            u'insert into {table} ({day}, {start}, {end}, {project}) '.format(
                    table = work_recorder.TABLE_WORK_TIME,
                    day = work_recorder.COLUMN_DAY,
                    start = work_recorder.COLUMN_START,
                    end = work_recorder.COLUMN_END,
                    project = work_recorder.COLUMN_PROJECT) +
                u'values (:day, :start, :end, :project)',
            {u'day' : a_work_time[WORK_TIME_KEY_DAY],
                u'start' : a_work_time[WORK_TIME_KEY_START],
                u'end' : a_work_time[WORK_TIME_KEY_END],
                u'project' : a_work_time[WORK_TIME_KEY_PROJECT]})

def main():
    u"""
    Record a work time in a day.

    Command line arguments:
        <project name> : project name (required)
        <day> : day, format : YYYYMMDD or MMDD, MDD. (required)
        <time> : <start time> <end time> (required, can repetition)
            <start time>, <end time> : time, format : HHMM or HMM.
    """
    parser = argparse.ArgumentParser(description = u'Redord a work time in a day.')
    parser.add_argument(u'project',
            help = u'Name of the project.')
    parser.add_argument(u'day',
            help = u'Day of the work. Format is YYYYMMDD or MMDD, MDD')
    parser.add_argument(u'times', nargs = '+',
            help = u'Work time of the work in the day. Format is <time> <time>.' +
                    'Format of <time> is HHMM or HMM.')
    args = parser.parse_args()

    try:
        work_times = convert_work_times(args.project, args.day, args.times)
    except work_recorder.InvalidArgumentFormatException:
        print u'Your arguments discords with formats.'
        parser.print_help()
        sys.exit(1)

    database = os.path.join(os.getcwdu(), work_recorder.DATABASE_FILE_NAME)
    with sqlite3.connect(database) as conn:
        record_work_times(work_times, conn)

if __name__ == '__main__':
    main()

