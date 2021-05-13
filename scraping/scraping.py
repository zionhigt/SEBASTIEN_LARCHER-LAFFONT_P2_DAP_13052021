import requests
from bs4 import BeautifulSoup as BS

class Scrap(object):
	def __init__(self, source_type, source, template):#('str', 'list')
		'''This module expect two constructor's arguments \n\r
		 - The first is URL of website page you want to be scraping \n\r
		 - The seconde is a list of that you want to get'''

		
		self.search_template = template
		self.soup = ""
		self.wanted_tags = []

		if source_type == "request":
			self.hyper_soup = requests.get(source).text

		elif source_type == "text":
			self.hyper_soup = source

		elif source_type == "file":
			with open(source, 'r') as file_source:
				self.source = file_source.read()

	def deleteTwiceWantedTags(self):
		new_array = []
		for i in self.wanted_tags:
			if not i in new_array:
				new_array.append(i)

		self.wanted_tags = new_array
	
	def get(self):

		self.soup = BS(self.hyper_soup, 'html.parser')
		self.wanted_tags = []
		for wanteds in self.search_template:
			#wanteds is a soup of elements templated
			wanteds = BS(wanteds, 'html.parser')
			for wanted in wanteds:
				for scraped in self.soup.find_all(wanted.name):
					if wanted.attrs:
						for w_attr in wanted.attrs:
							try:
								if type(wanted.attrs[w_attr]) == list:
									for a in wanted.attrs[w_attr]:
										if a in scraped.attrs[w_attr]:
											self.wanted_tags.append(scraped)
											

								elif type(wanted.attrs[w_attr] == str):
									if wanted.attrs[w_attr] == scraped.attrs[w_attr]:
										self.wanted_tags.append(scraped)
											
							except KeyError:
								continue
					else:
						self.wanted_tags.append(scraped)

		self.deleteTwiceWantedTags()
		return self.wanted_tags