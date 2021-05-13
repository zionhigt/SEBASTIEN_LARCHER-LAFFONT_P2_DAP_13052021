from bs4 import BeautifulSoup as BS
from scraping.scraping import Scrap
from utils.progress import Progress

class Category(object):
	def __init__(self, config):
		self.books = []
		self.url = config['url']
		self.name = config['name']
		pagination = Scrap("request", self.url, ['<li class=\"current\">']).get()
		self.pages_count = int(pagination[0].text.replace('\n', "").replace("Page 1 of ", "")) if len(pagination) else 1

	def get(self):
		#hyper_text_category = Scrap("request", self.url, ['<ul>'])
		for page_id in range(self.pages_count):
			page_url = self.url
			page_id += 1
			if page_id > 1:
				page_url = self.url.replace('index.html', 'page-{}.html'.format(page_id))
			self.books+=Scrap('request', page_url, ['<article class=\"product_pod\">']).get()
		return self.books
