from bs4 import BeautifulSoup as BS
try:
	from scraping import Scrap
except ImportError:
	from scraping.scraping import Scrap

class Category(object):
	def __init__(self, config):
		'''That module has a config parametre which is the result of categories module. \n It going to be srcaping all the pages of category to get all the books'''
		self.books = []
		self.url = config['url']
		self.name = config['name']
		pagination = Scrap("request", self.url, ['<li class=\"current\">']).get()
		self.pages_count = int(pagination[0].text.replace('\n', "").replace("Page 1 of ", "")) if len(pagination) else 1

	def get(self):
		for page_id in range(self.pages_count):
			page_url = self.url
			page_id += 1
			if page_id > 1:
				page_url = self.url.replace('index.html', 'page-{}.html'.format(page_id))
			self.books+=Scrap('request', page_url, ['<article class=\"product_pod\">']).get()
		return self.books

if __name__ == '__main__':
	
	help(Category)
