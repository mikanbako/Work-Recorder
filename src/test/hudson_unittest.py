# coding: UTF-8

# Hudsonでユニットテストを行う。

import sys
import xmlrunner

import unittest_suite

if __name__ == '__main__':
	runner = xmlrunner.XMLTestRunner(sys.stdout)
	runner.run(unittest_suite.suite())

