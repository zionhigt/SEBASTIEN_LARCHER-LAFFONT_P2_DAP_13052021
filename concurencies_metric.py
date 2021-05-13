from scraping.book import Book
from scraping.category import Category
from scraping.categories import Categories
#from scraping.request import request
# text = request('https://books.toscrape.com/index.html', ['<a></a>']).get()
# book = Book(text)
# book.say()

cats = Categories()
for cat in cats.getCategories():
	category = Category(cat)
	category.get()
