from scraping.book import Book
from scraping.category import Category
from scraping.categories import Categories
from utils.progress import Progress
import csv
#from scraping.request import request
# text = request('https://books.toscrape.com/index.html', ['<a></a>']).get()
# book = Book(text)
# book.say()

cats = Categories().getCategories()
category_id = 1
for cat in cats:
	category = Category(cat)
	with open('./gotten_data/{}.csv'.format(category.name.lower()), 'w', encoding="utf-8") as save_data_file:
		field_names = ['product_page_url',
		'UPC',
		'title',
		'price_incuding_tax',
		'price_excluding_tax',
		'number_available',
		'product_description',
		'category',
		'review_rating',
		'image_url']

		writer = csv.DictWriter(save_data_file, fieldnames= field_names)
		writer.writeheader()
		books =  category.get()
		write_progress = Progress(len(books), 'fraction', '{} {}/{} categories'.format(category.name, category_id, len(cats)), 'lines have been written')
		book_id = 1
		for book in books:
			book = Book(book.prettify(), category.name)
			writer.writerow(book.get())
			write_progress.update(book_id)
			book_id += 1
	category_id += 1
