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

import os
import subprocess

#
# Constraints that represent path.
#

# Source directory.
PATH_SRC = 'src'
# Main source directory.
PATH_SRC_MAIN = os.path.join(PATH_SRC, 'main')
# Test source directory.
PATH_SRC_TEST = os.path.join(PATH_SRC, 'test')
# External scripts directory.
PATH_EXTERNALS = 'externals'
# External scripts for test directory.
PATH_EXTERNALS_TEST = os.path.join(PATH_EXTERNALS, 'test')

#
# Set environment variables.
#
os.environ['PYTHONPATH'] = os.pathsep.join([PATH_SRC_MAIN, PATH_SRC_TEST, PATH_EXTERNALS_TEST])

#
# Commands to build.
#

def report_coverage(target, source, env):
    """
    Report code coverage as HTML.

    Arguments:
        target : Ignored.
        source : Script executed as test.
        env : Environment.
    """
    subprocess.call('coverage run %s' % (source[0]), shell = True)
    subprocess.call('coverage html')

def run_test(target, source, env):
    """
    Run test.

    Arguments:
        target : Ignored.
        source : Script executed as test.
        env : Environment.
    """
    subprocess.call('python %s' % (source[0]), shell = True)

def run_test_hudson(target, source, env):
    """
    Run test for Hudson.

    Arguments:
        target : Ignored.
        source : Script executed as test.
        env : Environment.
    """
    subprocess.call('python %s > unittest_result.xml' % (source[0]), shell = True)

#
# Build.
#

env = Environment()
test_suite = env.File(os.path.join(PATH_SRC_TEST, 'unittest_suite.py'))

if 'test' in COMMAND_LINE_TARGETS:
    env.AlwaysBuild(env.Alias('test', test_suite, run_test))
if 'test_hudson' in COMMAND_LINE_TARGETS:
    hudson_test_suite = env.File(
        os.path.join(PATH_SRC_TEST, 'hudson_unittest.py'))
    env.AlwaysBuild(env.Alias('test_hudson', hudson_test_suite, run_test_hudson))
if 'coverage' in COMMAND_LINE_TARGETS:
    env.AlwaysBuild(env.Alias('coverage', test_suite, report_coverage))

Default(None)
