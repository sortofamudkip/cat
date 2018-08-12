import praw, pprint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm

class Cat:
	def __init__(self, username, password, client_id, client_secret, user_agent, subreddit_name):
		self.reddit = praw.Reddit(username = username, password = password, client_id= client_id, 
					client_secret = client_secret, user_agent = user_agent)
		self.subreddit = self.reddit.subreddit(subreddit_name)
		self.stats = {}
		self.upvote_list = []

	def actually_collect_data(self, data_set):
		total_up_pc = 0; comment_total = 0
		for submission in data_set:
			submission.comments.replace_more(limit=None)
			to_process = submission.comments.list()
			scores = [x.score for x in to_process]
			self.upvote_list += scores; comment_total += len(scores)
			upvoted_pc = round(sum(x > 0 for x in scores) / float(max(len(scores), 1)) * 100)
			total_up_pc += upvoted_pc
		total_up_pc /= data_set.limit
		self.stats.update({"upvote_pc" : total_up_pc, "post_count" : data_set.limit, "comment_total" : comment_total})
		return self.upvote_list, self.stats

	def collect_data(self, _type, limit):
		if _type == "top":
			return self.actually_collect_data(self.subreddit.top(limit=limit))
		elif _type == "hot":
			return self.actually_collect_data(self.subreddit.hot(limit=limit))

	def process_data(self):
		data = self.upvote_list
		data = np.array(data)
		mean = np.mean(data); std = np.std(data)
		_max = np.ndarray.max(data); _min = np.ndarray.min(data)
		self.stats.update({"mean" : mean, "std" : std, "max": _max, "min": _min})
		return self.stats
		
	def show_plot(self):
		#init
		data = np.array(self.upvote_list)
		#plot histogram
		n, bins, patches = plt.hist(data, bins=np.arange(data.min(), data.max()+1), density=1)
		#best normal plot
		xmin, xmax = plt.xlim()
		x = np.linspace(xmin, xmax, 100)
		mu, std = norm.fit(data)
		p = norm.pdf(x, mu, std)
		plt.plot(x, p, 'k', linewidth=2)
		title = "black line: N({:.2f},{:.2f})".format(mu, std)
		plt.title(title)
		plt.show()

	def print_stats(self):
		pprint.pprint(self.stats)

	# Just do everything for me
	def run_default(self, _type="hot", limit=10):
		self.collect_data(_type, limit)
		self.process_data()
		self.show_plot()
		self.print_stats()


#usage:
# C = Cat(username = "your_username", password = "your_password", client_id= "your_clientid", 
# 	client_secret = "yourclientsecret", user_agent = "user_agent name", subreddit_name = "CatsStandingUp")


# C.run_default(limit = 200)
