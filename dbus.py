#!/usr/bin/env python
#-*- coding:utf-8 -*-
# dbus-derp.py -- bruecher 2012-11-10

import dbus, dbus.service, dbus.mainloop.glib

class SignalTest(dbus.service.Object):
	def __init__(self, object_path='/'):
		dbus.service.Object.__init__(self, dbus.SessionBus(), '/')

		@dbus.service.signal('com.gnome.mplayer')
		def Open(self, url): pass

		if __name__ == '__main__':
			dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
			SignalTest().Open('/tmp/Whedon On Romney.6TiXUF9xbTo.mp4')