#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gtk as Gtk
from mplayer.gtk2 import GtkPlayerView
import gtk
from ytplay.ytplayer import YoutubeClient
import quvi

class MyWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self)
		self.hbox1 = gtk.HBox(False, 0)
		self.vbox1 = gtk.VBox(False, 0)
		self.button = Gtk.Button(label="PAUSE/PLAY")
		self.button.connect("clicked", self.on_button_clicked)

		self.set_size_request(640, 480)
		self.set_title('GtkPlayer')

		# Quit application when this window is closed
		self.connect('destroy', self.destroy)

		# Create a player view
		self.player_view = GtkPlayerView()
		self.player = self.player_view.player

		# Quit application after file has finished playing
		self.player_view.connect('eof', gtk.main_quit)

		button = gtk.Button("Suchen")
		button.connect("clicked", self.on_button_clicked)
#		button.show()

		self.search_entry = gtk.Entry()
#		self.search_entry.show()
		self.hbox1.pack_start(self.search_entry, expand=False)
		self.hbox1.pack_start(button, expand=False)
#		self.hbox1.show()
		self.vbox1.pack_start(self.hbox1,expand=False)
		self.vbox1.pack_start(self.player_view)
		self.add(self.vbox1)
		self.show_all()
#		yc.gen_temp_file()
#		self.yc = yc

	def on_button_clicked(self, widget):
		self.player.quit()
		search = self.search_entry.get_text()
		yc = YoutubeClient('playlist', search, 'relevance',
						   '-1', "month")
		urls = yc.get_playlist(yc.feed, 'urllist')
		url = urls[0]
		#url = 'http://www.youtube.com/watch?v=tYb606oneP8'
		q = quvi.Quvi()
		q.parse(url)
		media_url = q.get_properties()['mediaurl']
		self.player.spawn()
		# Play the file
		self.player.loadfile(media_url)

	def pause_clicked(self, widget):
		self.player.pause()

	def destroy(self, widget):
#		self.yc.remove_temp_file()
		gtk.main_quit()


# Create a window
w = MyWindow()

# Enter the GTK event loop
gtk.main()
