A script set that records and aggregates working time.

1. How to use.
  The below examples are executed on bash.

  1. Put scripts into new directory. Working time is recorded to the directory.

  2. Create a recording file.

    Execute the below.

      ./create_work_record.py

  3. Record working time.

    For example, you works for a project that are named "example_project"
    between 9:00 and 12:00, 13:00 and 18:00 on 2011-05-29. You execute the
    below and record the work.

      ./record_work_time.py example_project 20110529 900 1200 1300 1800

    Format of working day is YYYYMMDD, MMDD or MDD. Y is a character that
    represents year.  M is a character that represents month. D is a character
    that represents day. When characters of year are omitted, the year
    represents this year.

    Format of working time is HHMM or HMM. H is a character that represents
    hour. M is a character that represents minute. The working time should be
    pair. Because pair working time represent their interval. You can specify
    multiple pair working time.

    For detail, execute the below.
    
      ./record_work_time.py -h

  4. Aggregate recorded working time.

    When the below is executed, working time for every project on 2011-05
    displayed. When you specify an intrval that is more than a month,
    working time for every project for every month is displayed.

      ./aggregate_work_time.py 20110501 20110531

    Format of term is a pair of YYYYMMDD, MMDD or MDD. Y is a character that
    represents year.  M is a character that represents month. D is a character
    that represents day. When characters of year are omitted, year is this
    year.

    For detail, execute the below.

      ./aggregate_work_time.py -h

2. Requires

  This script requires the below softwares.

  * Python 2.7 (http://www.python.org/)

3. Limitation

  1. You cannot modify and delete working time by this scripts.
     Use sqlite3 software or related utility.

4. For developers

  1. Requires

    * SCons (http://www.scons.org/)

  2. Run all unit test

    Execute the below on the top directory of this project.

      scons test

  3. Set up environment

    Execute the below on th top directory of this project.
    The script sets PYTHONPATH for this project.
    
      source environment.sh

