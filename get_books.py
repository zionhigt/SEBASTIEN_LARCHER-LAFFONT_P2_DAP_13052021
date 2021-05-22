from bs4 import BeautifulSoup as BS
from multiprocessing import Pool
import urllib.parse, requests, csv, os, sys, time
#TODO
#Extracting all the books from booktosrcap.com
#Transforming got data earlier
#Loading into .csv files, each books of categories

def getHtml(url):
    #Return a HTML page from an URL
    with requests.get(url) as HTML:
        if HTML.status_code == 200:
            return HTML.text
        else:
            print("La requête a échoué avec le status {} \n\r {}".format(str(HTML.status_code), url))
            return False

def show_time(second):
    # Convert a seconds as a --m--s format
	s = str(int(second % 60))
	s = s if len(s) == 2 else '0' + s
	show = '{}m{}s'.format(int(second / 60) , s)
	return show

def extractor(url):
    #Get the home page and all the pagination
    #For each pages was got, get all found books
    #Return a list of page_book:

    a = 1
    book_urls = []

    hyper_menu = getHtml(url)
    if hyper_menu: # if menu page is got
        menu_page = BS(hyper_menu, 'html.parser')

        hyper_pagination = menu_page.find('li', {'class': "current"})
        pages_count = int(hyper_pagination.text.split("Page 1 of")[1]) # Get a number of pages paginated
        for page_id in range(pages_count):
            page_id += 1

            page_url = url
            if page_id > 1:
                page_url = urllib.parse.urljoin(url, 'catalogue/page-{}.html'.format(page_id))

            current_page = getHtml(page_url)
            current_soup = BS(current_page, 'html.parser')
            books_elements = current_soup.find_all('article', {'class': "product_pod"})

            for book_element in books_elements:
                book_urls.append(urllib.parse.urljoin(page_url, book_element.a['href']))

            sys.stdout.write('\x1b[2K\r {}/{} pages indexées '.format(page_id, pages_count))

        with Pool(64) as p:
            extracted_books_list = []
            books_list = p.imap(getHtml, book_urls, 12)

            for book_page in books_list:
                book_url = urllib.parse.urljoin(page_url, book_element.a['href'])
                book_soup = BS(book_page, 'html.parser')

                url_tag = book_soup.new_tag("div", id="selfURL", url=book_url)
                book_soup.append(url_tag)

                extracted_books_list.append(book_soup)

                sys.stdout.write('\x1b[2K\r {}/1000 livres récupéré(s)'.format(a))
                a += 1

        return extracted_books_list
    else:
        return False




def transformer(extracted_data):
    #Run through the extracted_data
    #Return a dictionary such as:
    """
    {
        categoryName: [{transformed_data_of_book_1}, {transformed_data_of_book_2}, ...],
        ...
    }
    """

    a = 0
    organized_books = {} # dictionary returned

    for page_book in extracted_data:
        b = a%5
        decorator = "".join(['.']*b)
        sys.stdout.write('\x1b[2K\r transformmation des donées {}'.format(decorator))
        a+=1

        url_parent = page_book.find('div', {'id': "selfURL"})
        url = url_parent['url']

        for table in page_book.find_all("table"):
            for row in table.find_all('tr'):
                if row.th.text == "UPC":
                    UPC = row.td.text
                elif row.th.text == "Price (incl. tax)":
                    PIT = float(row.td.text.split('£')[1])
                elif row.th.text == "Price (excl. tax)":
                    PET = float(row.td.text.split('£')[1])
                elif row.th.text == "Availability":
                    stock = int(row.td.text.replace('In stock (', "").replace(' available)', ""))
                elif row.th.text == "Number of reviews":
                    rating = int(row.td.text)

        parent_category_name = page_book.find('ul', {'class': "breadcrumb"})
        category = parent_category_name.find_all('a')[2].text

        title = page_book.find('h1').text

        description = page_book.find('div', {'id': "product_description"})
        if not isinstance(description, type(None)):
            description = description.findNext('p').text
        else:
            description = "Données non renseignées"

        brut_img_url = page_book.find('div', {'class': "carousel-inner"}).img['src']
        img_url = urllib.parse.urljoin('https://books.toscrape.com/', brut_img_url)

        formated_book = {
            'product_page_url': url,
            'UPC': UPC,
            'title': title,
            'price_including_tax': PIT,
            'price_excluding_tax': PET,
            'number_available': stock,
            'product_description': description,
            'category': category,
            'review_rating': rating,
            'image_url': img_url
        }

        if category not in organized_books:
            organized_books[category] = []
        organized_books[category].append(formated_book)

    return organized_books

def loader(transformed_data):
    # Run through the transformed_data
    # Saving all elements as a [category_name].csv

    if not os.path.exists('./gotten_data/'):
        os.system('mkdir gotten_data')

    field_names = ['product_page_url',
                   'UPC',
                   'title',
                   'price_including_tax',
                   'price_excluding_tax',
                   'number_available',
                   'product_description',
                   'category',
                   'review_rating',
                   'image_url']

    for category in transformed_data:
        file_name = category.lower().replace(" ", "_")
        with open('./gotten_data/{}.csv'.format(file_name), 'w', encoding="utf-8") as save_data_file:
            writer = csv.DictWriter(save_data_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(transformed_data[category])
            print('\x1b[2K\r {}.csv à été creé'.format(file_name))

    return True

def main():
    time_start = time.perf_counter()
    extracted_data = extractor("http://books.toscrape.com/index.html")
    if extracted_data:
        transformed_data = transformer(extracted_data)
        if transformed_data:
            loader(transformed_data)
            print("" + show_time(round(time.perf_counter() - time_start, 3)))

if(__name__ == '__main__'):

    main()

