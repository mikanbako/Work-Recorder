# coding: UTF-8

# ユニットテストを行うテストスイートを定義する。

import os.path
import unittest

def suite():
	u"""
	テストスイートを定義する。
	"""
	test_loader = unittest.TestLoader()
	return test_loader.discover(os.path.dirname(__file__))

if __name__ == '__main__':
	unittest.TextTestRunner().run(suite())

