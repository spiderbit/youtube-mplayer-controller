from ytplay.ytplayer import YoutubeClient

class TestYoutubeClient(YoutubeClient):
	def __init__(self):
		pass
class Player:
	def __init__(self):
		self.url = ''
class Media:
	def __init__(self):
		self.player = Player()
class Title:
	def __init__(self):
		self.text = ''
class TestEntry:
	def __init__(self):
		self.media = Media()
		self.title = Title()

def test_sort_entries():
	"""tests the sort_entries method of ytplayer.py
	"""

	yt = TestYoutubeClient()
	urls = ['url1', 'url2', 'url3', 'url4', 'url5']
	titles = ['x4', 'x3', 'x1', 'x2', 'x5']
	entries = []
	for url, title in zip (urls,titles):
		entry = TestEntry()
		entry.media.player.url = url
		entry.title.text = title
		entries.append(entry)

	sorted_entries = []
	sorted_entries.append(entries[2])
	sorted_entries.append(entries[3])
	sorted_entries.append(entries[1])
	sorted_entries.append(entries[0])
	sorted_entries.append(entries[4])
	sorted_by_method = yt.sort_entries(entries)
	assert len(sorted_by_method) == 5
	assert sorted_entries[0].media.player.url == 'url3'
	for x,y in zip (sorted_entries, sorted_by_method):
		xurl = x.media.player.url
		xtitle = x.title.text
		yurl = y.media.player.url
		ytitle = y.title.text
		assert xurl == yurl, "[%s],[%s]" % (xurl,yurl)
		assert xtitle == ytitle, "[%s],[%s]" % (xtitle,ytitle)
	assert sorted_by_method == sorted_entries, sorted_entries

def test_sort_entries_with_tail():
	"""tests the sort_entries method of ytplayer.py
	"""

	yt = TestYoutubeClient()
	urls = ['url1', 'url2', 'url3', 'url4', 'url5']
	titles = ['x4abc', 'x3abc', 'x1abc', 'x2abc', 'x5abc']
	entries = []
	for url, title in zip (urls,titles):
		entry = TestEntry()
		entry.media.player.url = url
		entry.title.text = title
		entries.append(entry)

	sorted_entries = []
	sorted_entries.append(entries[2])
	sorted_entries.append(entries[3])
	sorted_entries.append(entries[1])
	sorted_entries.append(entries[0])
	sorted_entries.append(entries[4])
	sorted_by_method = yt.sort_entries(entries)
	assert len(sorted_by_method) == 5
	assert sorted_entries[0].media.player.url == 'url3'
	for x,y in zip (sorted_entries, sorted_by_method):
		xurl = x.media.player.url
		xtitle = x.title.text
		yurl = y.media.player.url
		ytitle = y.title.text
		assert xurl == yurl, "[%s],[%s]" % (xurl,yurl)
		assert xtitle == ytitle, "[%s],[%s]" % (xtitle,ytitle)
	assert sorted_by_method == sorted_entries, sorted_entries



def test_sort_entries_crota():
	"""tests the sort_entries method of ytplayer.py
	"""

	yt = TestYoutubeClient()
	urls = ['url1', 'url2', 'url3']
	titles = ["DRG (Z) vs StarTale Bomber (T) - G2 - StarCraft 2 - SC1939",
			  "DRG (Z) vs StarTale Bomber (T) - G3 - StarCraft 2 - SC1940",
			  "DRG (Z) vs StarTale Bomber (T) - G1 - StarCraft 2 - SC1938"]
	entries = []
	for url, title in zip (urls,titles):
		entry = TestEntry()
		entry.media.player.url = url
		entry.title.text = title
		entries.append(entry)

	sorted_entries = []
	sorted_entries.append(entries[2])
	sorted_entries.append(entries[0])
	sorted_entries.append(entries[1])
	sorted_by_method = yt.sort_entries(entries)
	count = len(sorted_by_method)
	#assert len(sorted_by_method) == 3, count
	assert sorted_entries[1].media.player.url == 'url1'
	for x,y in zip (sorted_entries, sorted_by_method):
		xurl = x.media.player.url
		xtitle = x.title.text
		yurl = y.media.player.url
		ytitle = y.title.text
		assert xurl == yurl, "[%s],[%s]" % (xurl,yurl)
		assert xtitle == ytitle, "[%s],[%s]" % (xtitle,ytitle)
	assert sorted_by_method == sorted_entries, sorted_entries
