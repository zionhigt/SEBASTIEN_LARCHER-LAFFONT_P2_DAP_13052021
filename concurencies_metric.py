from scraping.book import Book
from scraping.category import Category
from scraping.categories import Categories
from utils.progress import Progress
import csv
import os
import time
#from scraping.request import request
# text = request('https://books.toscrape.com/index.html', ['<a></a>']).get()
# book = Book(text)
# book.say()

time_start = time.perf_counter()
cats = Categories().getCategories()
category_id = 1

def show_time(second):
	s = str(int(second % 60))
	s = s if len(s) == 2 else '0' + s
	show = '{}m{}s'.format(int(second / 60) , s)
	return show

for cat in cats:
	category = Category(cat)

	if not os.path.exists('./gotten_data/'):
		os.system('mkdir gotten_data')

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
		write_progress = Progress(len(books), 'fraction', '{}.csv {}/{} categories'.format(category.name.lower(), category_id, len(cats)), 'lines have been written')
		book_id = 1
		time_to_exec = 0
		for book in books:
			book = Book(book.prettify(), category.name)
			writer.writerow(book.get())
			write_progress.update(book_id, show_time(round(time.perf_counter() - time_start, 3)))
			book_id += 1

	category_id += 1


