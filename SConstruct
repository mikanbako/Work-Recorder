# coding: UTF-8

import os
import subprocess

###
# 各種パスを表す定数の用意
###

# ソースディレクトリ
PATH_SRC = 'src'
# main用ソースディレクトリ
PATH_SRC_MAIN = os.path.join(PATH_SRC, 'main')
# test用ソースディレクトリ
PATH_SRC_TEST = os.path.join(PATH_SRC, 'test')
# ライブラリディレクトリ
PATH_LIB = 'lib'
# test用ライブラリディレクトリ
PATH_LIB_TEST = os.path.join(PATH_LIB, 'test')

###
# 環境変数の設定
###
os.environ['PYTHONPATH'] = ';'.join([PATH_SRC_MAIN, PATH_SRC_TEST, PATH_LIB_TEST])

###
# ビルド用コマンド
###

def report_coverage(target, source, env):
	u"""
	コードカバレッジを計測して結果をHTMLとして出力する。

	引数:
		target : 無視する
		source : テストとして実行するスクリプト
		env : 環境
	"""
	subprocess.call('coverage run %s' % (source[0]), shell = True)
	subprocess.call('coverage html')

def run_test(target, source, env):
	u"""
	テストを実行する。

	引数:
		target : 無視する。
		source : テストとして実行するスクリプト
		env : 環境
	"""
	subprocess.call('python %s' % (source[0]), shell = True)

def run_test_hudson(target, source, env):
	u"""
	Hudson用にテストを実行する。

	引数:
		target : 無視する
		source : テストとして実行するスクリプト
		env : 環境
	"""
	subprocess.call('python %s > unittest_result.xml' % (source[0]), shell = True)

###
# ビルド
###
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
