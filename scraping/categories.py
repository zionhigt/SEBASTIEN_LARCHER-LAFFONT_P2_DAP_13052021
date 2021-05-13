from scraping.scraping import Scrap
#def __init__(self, source_type, source, template):

class Categories(object):

	def __init__(self):

		self.categories = []
		self.url_to_scrap = 'https://books.toscrape.com/index.html'
	
	def getCategories(self):

		template = ['<div class=\"side_categories\">']
		hyper_text_categories = Scrap("request", self.url_to_scrap, template).get()
		categories_list = Scrap("text", hyper_text_categories[0].prettify(), ['<li>'])

		for category in categories_list.get():
			name = category.text.replace(' ', "").replace("\n", "")
			url = self.url_to_scrap.replace('index.html', category.find('a').attrs['href'])

			self.categories.append({'name': name, 'url': url})
	
		return self.categories