from ytplay.ytplayer import YoutubeClient
import gdata.youtube.service as service
import pickle


def save_data(data, fname):
    """
    """
    output = open(fname, 'wb')
    # Pickle the list using the highest protocol available.
    pickle.dump(data, output, -1)
    output.close()

def load_data(fname):
    return pickle.load(open(fname, 'rb'))


class MyGData(object):
	"""stub for gdata for testing
    """
	def __init__(self):
		pass

class MyYouTubeService(service.YouTubeService):
	"""
	"""

	def __init__(self):
		"""
		"""
		super(MyYouTubeService, self).__init__(self)
		self.pkl_user = 'samples/user_feed.pkl'
		self.pkl_search = 'samples/search_feed.pkl'
#		self.prepare_GetYouTubeUserFeed('blizshouter')
#		self.prepare_YouTubeQuery()


	def GetYouTubeUserFeed(self, username=""):
		"""
		"""
		pickle_obj = load_data(self.pkl_user)
		return pickle_obj

	def prepare_GetYouTubeUserFeed(self, username=""):
		"""
		"""
		obj = super(MyYouTubeService, self).GetYouTubeUserFeed(username=username)
		pickle_obj = save_data(obj, self.pkl_user)

	def YouTubeQuery(self, query):
		"""
		"""
		pickle_obj = load_data(self.pkl_search)
		return pickle_obj

	def prepare_YouTubeQuery(self):
		"""
		"""
		query = service.YouTubeVideoQuery()
		query.vq = 'piratenpartei'
		query.format = '5'
		query.hd = True
		query.max_results = 25
		query.start_index = 1
		query.racy = 'exclude'

		query.time = 'today'
		feed = super(MyYouTubeService, self).YouTubeQuery(query)

		pickle_obj = save_data(feed, self.pkl_search)




class TestYouTubeClient(object):
	"""
	"""

	def __init__(self):
		my_service = MyYouTubeService()
		service.YouTubeService.GetYouTubeUserFeed = \
				my_service.GetYouTubeUserFeed
		service.YouTubeService.YouTubeQuery = \
				my_service.YouTubeQuery


	def test_user_feed(self):
		yc = YoutubeClient('search', 'u_blizshouter', 'published', '25', \
						   'reverse', 'today')
		# save result-data for comparsion
#		save_data(yc.feed.entry, 'samples/user_feed_filtered.pkl')
		pickle_obj = load_data('samples/user_feed_filtered.pkl')
		for pobj,entry in zip (pickle_obj,yc.feed.entry):
			assert pobj.media.player.url == entry.media.player.url
			assert pobj.title.text == entry.title.text

	def test_search_feed(self):
		pkl_file = 'samples/search_feed_filtered.pkl'
		yc = YoutubeClient('search', 'piratenpartei', 'published', '25', \
						   'reverse', 'week')
		# save result-data for comparsion
#		save_data(yc.feed.entry, pkl_file)
		pickle_obj = load_data(pkl_file)
		for pobj,entry in zip (pickle_obj,yc.feed.entry):
			assert pobj.media.player.url == entry.media.player.url
			assert pobj.title.text == entry.title.text

