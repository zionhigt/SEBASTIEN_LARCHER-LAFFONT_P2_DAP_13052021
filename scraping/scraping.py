# import urllib.request
import requests
from bs4 import BeautifulSoup as BS

class Scrap(object):
	def __init__(self, source_type, source, template):#('str', 'list')
		'''This module expect three constructor's arguments \n\
		 - The type of the source that you'll bring to it: ['request', 'text', 'file']\n
		 - The source depends to his type, ['request': Page URL, 'text': utf-8 encoded string, 'file': File local path]
		 - A template of what you want to be scraping from the source'''

		
		self.search_template = template
		self.soup = ""
		self.wanted_tags = []

		if source_type == "request":
			with requests.get(source) as HTML:
				if HTML.status_code == 200:
					self.hyper_soup = HTML.text
				else:
					print("La requête a échoué avec le status " + HTML.status)

			### urlib.request deprecated for better performences ###
			# with urllib.request.urlopen(source) as HTML:
			# 	if HTML.status == 200:
			# 		self.hyper_soup = HTML.read().decode('utf-8')
			# 	else:
			# 		print("La requête a échoué avec le status " + HTML.status)

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

		#EXTRACT
		self.soup = BS(self.hyper_soup, 'html.parser')
		self.wanted_tags = []
		
		#TRANSFORM
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
		#LOAD
		self.deleteTwiceWantedTags()
		return self.wanted_tags


if __name__ == '__main__':
	
	help(Scrap)