from scraping.scraping import Scrap
#get a book
class Book(object):
	def __init__(self, hyper_text_book, category):
		self.base_url = 'https://books.toscrape.com/catalogue/'
		self.book = hyper_text_book
		self.category = category
		self.url = Scrap('text', self.book, ['<a>']).get()[0].attrs['href'].replace('../../../', self.base_url)
		book_info = Scrap('request', self.url, ['<article class=\"product_page\">']).get()[0].prettify()
		table_info = Scrap("text", book_info, ['<table class=\"table table-striped\">']).get()[0].prettify()
		for row in Scrap('text', table_info, ['<tr>']).get():
			current_row_head = row.find('th').text.replace('\n', '').replace(' ', '')
			if current_row_head == "UPC":
				self.UPC = row.find('td').text.replace('\n', '').replace(' ', '')

			elif current_row_head == "Price(excl.tax)":
				self.PET = row.find('td').text.replace('\n', '').replace(' ', '')

			elif current_row_head == "Price(incl.tax)":
				self.PIT = row.find('td').text.replace('\n', '').replace(' ', '')

			elif current_row_head == "Availability":
				self.stock = int(row.find('td').text.replace('\n', '').replace(' ', '').replace('Instock(', "").replace('available)', ""))

			elif current_row_head == "Numberofreviews":
				self.rating = int(row.find('td').text.replace('\n', '').replace(' ', ''))


		self.description = Scrap("text", book_info, ['<p>']).get()[3].text

		self.title = Scrap("text", book_info, ['<h1>']).get()[0].text.replace('\n', '').replace('  ', '')[:-1].replace("\"", "&quot;")
		try:
			self.img_url = Scrap("text", book_info, ['<img alt=\"{}\">'.format(self.title)]).get()[0].attrs['src'].replace('../../', self.base_url).replace('catalogue/', "")
		except IndexError:
			self.img_url = ""
			print(Scrap("text", book_info, ['<img>']).get())

	def get(self):
		
		formated_book = {
		'product_page_url': self.url,
		'UPC': self.UPC,
		'title': self.title,
		'price_incuding_tax': self.PIT,
		'price_excluding_tax': self.PET,
		'number_available': self.stock,
		'product_description': self.description,
		'category': self.category,
		'review_rating': self.rating,
		'image_url': self.img_url, 
		}

		return formated_book