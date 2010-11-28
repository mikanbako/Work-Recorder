# coding: UTF-8

# Common definition for work recorder.

from datetime import date, datetime
import re

# Name of database file.
DATABASE_FILE_NAME = u'work_record.db'

# Name of table that represents the work record.
TABLE_WORK_TIME = u'work_time'

# Name of column that represents the day of work.
# Format is YYYY-MM-DD.
COLUMN_DAY = u'day'

# Name of column that represents the start time of work.
# Format is HH:MM or HH:MM:SS.
COLUMN_START = u'start'

# Name of column that represents the end time of work.
# Format is HH:MM or HH:MM:SS.
COLUMN_END = u'end'

# Name of column that represents project name that related to the time.
COLUMN_PROJECT = u'project'

# Name of column that represents comment that related to the time.
COLUMN_COMMENT = u'comment'

# Pattern of a day.
# Year must be 2xxx.
PATTERN_DAY = re.compile(ur'^(?P<year>2\d{3})?(?P<month>\d?\d)(?P<day>\d{2})$')
# Pattern of a time.
PATTERN_TIME = re.compile(ur'^(?P<hour>\d?\d)(?P<minute>\d{2})$')

class InvalidArgumentFormatException(Exception):
    u"""
    Exception that represents inputed command line arguments is invalid.
    """
    pass

def convert_day(day_string):
    u"""
    Convert a string to day (YYYY-MM-DD).

    If this method could not convert, raise InvalidArgumentFormatException.
    """
    match = PATTERN_DAY.match(day_string)
    if not match:
        raise InvalidArgumentFormatException()

    year = match.group(u'year')
    if not year:
        today = date.today()
        year = today.year
    month = match.group(u'month')
    day = match.group(u'day')

    try:
        converted_datetime = datetime.strptime(
                u'{year} {month} {day}'.format(
                    year = year, month = month, day = day),
                u'%Y %m %d')
    except ValueError, e:
        raise InvalidArgumentFormatException()

    return converted_datetime.date().isoformat()

def convert_time(time_string):
    u"""
    Convert a string to time (HH:MM).

    If this method could not convert, raise InvalidArgumentFormatException.
    """
    match = PATTERN_TIME.match(time_string)
    if not match:
        raise InvalidArgumentFormatException()

    hour = match.group(u'hour')
    minute = match.group(u'minute')

    try:
        time = datetime.strptime(
                u'{hour} {minute}'.format(hour = hour, minute = minute),
                u'%H %M').time()
    except ValueError:
        raise InvalidArgumentFormatException()

    time.replace(microsecond = 0)
    return time.isoformat()

