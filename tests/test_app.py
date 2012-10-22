#!/usr/bin/env python
#-*- coding:utf-8 -*-

from os import environ as env
import tempfile
import shutil
import os
from ConfigParser import SafeConfigParser
import sys
import subprocess
from subprocess import PIPE, Popen, call
from StringIO import StringIO
import yt_curses
import curses

class MyCursesWindow:
	def __init__(self):
		return
	def getkey(self):
		return 'q'
	def refresh(self):
		"""dummy for clean
		"""
		return None
	def clear(self):
		"""dummy for clear
		"""
		return
	def getmaxyx(self):
		"""dummy for clean
		"""
		return 80,80
	def addstr(self, pos1, pos2, str):
		return
	def border(self, size):
		return


def my_initscr():
	return MyCursesWindow()

def my_endwin():
	return


class Test_MMailer(object):

	def setup(self):
		# self.old_env_home = env['HOME']
		# self.temp_dir = tempfile.mkdtemp()
		# env['HOME'] = self.temp_dir
		# self.config_dir = os.path.join(\
		# 	self.temp_dir, '.config', 'mmailer')
		# self.config_path = os.path.join(self.config_dir, 'config')
		pass

	def teardown(self):
		# env['HOME'] = self.old_env_home
		# shutil.rmtree(self.temp_dir)
		pass

	def test_start_and_quit_works(self):
		"""tests if start and quit with q set works
		"""
		p = subprocess.Popen(['./yt_curses'],\
			stdin=PIPE, stdout=PIPE)
		question = p.communicate('q')[0]
		try:
			p.communicate()
		except:
			pass
		assert p.poll() == 0
		return

	def test_start_and_quit_works2(self, ):
		"""tests if it starts and ends clean
		"""
		curses.initscr = my_initscr
		curses.endwin = my_endwin
		yt_curses.start()
