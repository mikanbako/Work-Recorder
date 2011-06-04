#!/usr/bin/env python
# coding: UTF-8

import argparse
import os
import os.path
import sqlite3
import sys

import work_recorder

# Name of column that represents month. Format is YYYY-MM.
COLUMN_MONTH = u'month'
# Name of column that represents hours.
COLUMN_HOURS = u'hours'

# Key of time that represents a month.
TIME_KEY_MONTH = COLUMN_MONTH
# Key of time that represents a project.
TIME_KEY_PROJECT = work_recorder.COLUMN_PROJECT
# Key of time that represents hours a project.
TIME_KEY_HOURS = COLUMN_HOURS

def aggregate_work_time(start_day, end_day, conn):
    u"""
    Aggregate work times a project.

    Parameters:
        start_day : Day of start. Format is YYYY-MM-DD.
        end_day : Day of end. Format is YYYY-MM-DD.
        conn : Connection of database.
    Return:
        A list of dictionary. Key is a name of project. Value is its work time.
    """
    cursor = conn.execute(u"""
        select strftime('%Y-%m', {day}) as {month},
            {project},
            round(sum(strftime('%s', {day} || ' ' || {end}) -
                strftime('%s', {day} || ' ' || {start})) / 60.0 / 60.0, 2) as {hours}
        from {work_time}
        where {day} between :start and :end
        group by {month}, {project}
        order by {month} asc, {hours} desc
        """.format(month = COLUMN_MONTH,
            project = work_recorder.COLUMN_PROJECT,
            day = work_recorder.COLUMN_DAY,
            end = work_recorder.COLUMN_END,
            hours = COLUMN_HOURS,
            start = work_recorder.COLUMN_START,
            work_time = work_recorder.TABLE_WORK_TIME),
        {u'start': start_day, u'end': end_day})
    return [
            {TIME_KEY_MONTH: a_row[0],
                TIME_KEY_PROJECT: a_row[1],
                TIME_KEY_HOURS: a_row[2]}
            for a_row in cursor]

def print_result(times):
    previous_month = None
    for a_time in times:
        month = a_time[TIME_KEY_MONTH]
        if month != previous_month:
            if previous_month != None:
                print
            print month
            previous_month = month
        print u'\t%s: %s hours' % (a_time[TIME_KEY_PROJECT], a_time[TIME_KEY_HOURS])

def main():
    u"""
    Aggregate work time a project.

    Command line arguments:
        <start day> : Day of start, format : YYYYMMDD or MMDD, MDD (required)
        <end day> : Day of end, format : YYYYMMDD or MMDD, MDD (required)
    """
    parser = argparse.ArgumentParser(description = u'Aggregate work time a project.')
    parser.add_argument(u'start_day',
            help = u'Day of start. Format is YYYYMMDD or MMDD, MDD')
    parser.add_argument(u'end_day',
            help = u'Day of end. Format is YYYYMMDD or MMDD, MDD')
    args = parser.parse_args()

    try:
        start_day = work_recorder.convert_day(args.start_day)
        end_day = work_recorder.convert_day(args.end_day)
    except work_recorder.InvalidArgumentFormatException:
        print u'Your arguments discords with formats.'
        sys.exit(1)

    database = os.path.join(os.getcwdu(), work_recorder.DATABASE_FILE_NAME)
    with sqlite3.connect(database) as conn:
        times = aggregate_work_time(start_day, end_day, conn)
    print_result(times)

if __name__ == '__main__':
    main()

