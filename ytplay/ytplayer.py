#!/usr/bin/env python
#-*- coding:utf-8 -*-


import sys
import random

# from youtube_player import YoutubePlayer
# my player, uses urwid and vlc ^^

import gdata.youtube.service
# http://gdata-python-client.googlecode.com/hg/pydocs/gdata.youtube.service.html#YouTubeVideoQuery
# https://developers.google.com/youtube/1.0/developers_guide_python

#from ytdl import ytdl
#from ytstr import ytstr
# https://bitbucket.org/rg3/youtube-dl/wiki/Home

import re




class YoutubeClient:

	def __init__(self,keyword,q,order,num_results,mode=None,time=None):

		keywords = ['search', 'download', 'stream', 'playlist']
		if keyword in keywords: self.keyword = keyword
		else: sys.exit('invalid keyword')

		self.q = q

		ordering_key = {'rating':'rating', 'viewcount':'viewCount', \
							'relevance':'relevance','published':'published'}
		ordering = ['rating','viewcount','relevance', 'published']
		if order in ordering: self.order = ordering_key[order]
		else: sys.exit('invalid ordering')

		try: self.num = int(num_results)
		except Exception as e: sys.exit('invalid number %s' %e)

		if mode is not None:
			self.mode = mode
		else: self.mode = False

		times_key = {'today':'today','week':'this_week',\
						 'month':'this_month','time':'all_time'}
		times = ['today', 'week', 'month', 'time']
		if time is not None and time in times:
			self.time = times_key[time]
		else:
			self.time = False

		self.client = gdata.youtube.service.YouTubeService()
		self.pre_execute()

	def possible_multipart_name(self, text):
		"""

        Arguments:
        - `text`:
        """
		pattern1 = '(\D*)(\d{1})(.*)'
		match1 = re.search(pattern1, text)
		return match1


	def get_similar_entries(self, match, entries, entry):
		"""

        Arguments:
        - `match`:
		- `entries`:
		- `entry`:
        """
		similar_entries = dict()
		found_part_number = match.groups()[1]
		similar_entries[found_part_number] = entry
		pattern = "(%s)(\d{1})" % (
			re.escape(match.groups()[0])
#			re.escape(match.groups()[2])
		)
		for entry2 in entries:
			if not entry2 == entry:
				similar = re.search(pattern, entry2.title.text)
				if similar != None:
					x = similar.groups()
#					assert similar.groups()[1] == '2', x
					similar_entries[similar.groups()[1]] = entry2
		return similar_entries


	def sort_entries(self, entries):
			"""
            Arguments:
            - `entries`:
            """
			sorted_entries = []
			for entry in entries:
				url = entry.media.player.url
				text = entry.title.text
				if entry in sorted_entries:
					continue
				match = self.possible_multipart_name(text)
				similar = None
				if match:
					similar_entries = self.get_similar_entries(
						match, entries, entry)
					keys = similar_entries.keys()
#					assert False, keys
					keys.sort()

					if keys:
						for key in keys:
					#		print similar_entries[key].title.text+"\n"
							sorted_entries.append(similar_entries[key])
#					assert False, similar_entries
				else:
					#print "else"
					sorted_entries.append(entry)
			return sorted_entries


	def get_playlist(self, feed, pl_format='file', multipart_sort=False):

		if pl_format == 'file':
			lines = []
			lines.append('#EXTM3U\n')
			lines.append("# Playlist created by youtube_mplayer_controller\n")
		elif pl_format == 'urllist':
			urls = []

		if multipart_sort:
			entries = self.sort_entries(feed.entry)
		else:
			entries = feed.entry

		for entry in entries:
			url = str(entry.media.player.url)
			if pl_format == 'file':
				lines.append('#EXTINF:0,%s\n%s\n'%(entry.title.text,url))
			elif pl_format == 'urllist':
				urls.append(url)

		if pl_format == 'file':
			lines.append(feed.entry[0].media.player.url)
			return lines
		elif pl_format == 'urllist':
			return urls

	def playlist(self,feed):
		urls = self.get_playlist(feed)#, 'urllist')
		for url in urls:
			print url


	def search(self,feed):

		for entry in feed.entry:
			try:
				print '\n[video] title: %s' % entry.title.text
				print '[video] url: %s' % entry.media.player.url
				print '[video] rating: %s' % entry.rating.average
				print '[video] view count: %s' % entry.statistics.view_count
				print '[video] id: %s' % entry.media.player.url.split(\
					'watch?v=').pop().split("&")[0]
			except Exception as e:
				print('search failed:\nError: %s' % e)


	def download(self,feed):

		for entry in feed.entry:
			try:
				ytdl.main(entry.media.player.url)
			except Exception as e:
				print('download failed:\nError: %s' % e)

	def gen_temp_file(self):

		feed = self.feed
		import tempfile
		d = tempfile.mkdtemp()
		self.temp_dir = d
		import os
		f = open(os.path.join(d,'test.m3u'), 'w+')
		lines = self.get_playlist(feed)
		self.temp_file = f
		f.writelines(lines)
		f.close()

	def remove_temp_file(self):
		import shutil
		shutil.rmtree(self.temp_dir)

	def stream(self, feed):

		self.gen_temp_file()
		import subprocess
		#subprocess.Popen(["smplayer"])
		#subprocess.Popen(["umplayer"])
		subprocess.check_call(["smplayer", self.temp_file.name])
		self.remove_temp_file()

	def pre_execute(self):

		query = gdata.youtube.service.YouTubeVideoQuery()
		if self.q.startswith('u_'):
			query.author = self.q[2:]
		else:
			query.vq = self.q
		query.format = '5'
		query.hd = True
		if self.num != -1:
			query.max_results = self.num
		query.start_index = 1
		query.racy = 'exclude'
		query.orderby = self.order
		if self.time: query.time = self.time
		feed = self.client.YouTubeQuery(query)
		if self.mode == 'shuffle': random.shuffle(feed.entry)
		elif self.mode == 'reverse': feed.entry.reverse()
		self.feed = feed

	def execute(self):
		feed = self.feed
		command = self.keyword
		if command == 'download': self.download(feed)
		if command == 'stream':
			if len(self.feed.entry) == 0:
				print "search had 0 results, widen your search terms"
				return 0
			else:
				self.stream(feed)
		if command == 'search':	self.search(feed)
		if command == 'playlist': self.playlist(feed)

if __name__ == '__main__':
	yt = None

	if len(sys.argv) == 7:
		yt = YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
	if len(sys.argv) == 6:
		if sys.argv[5] == 'shuffle':
			yt = YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], None)
		elif sys.argv[5] == 'reverse':
			yt = YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], None)
		else:
			yt = YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], None, sys.argv[5])
	if len(sys.argv) == 5:
		yt = YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	if yt != None:
		yt.execute()
