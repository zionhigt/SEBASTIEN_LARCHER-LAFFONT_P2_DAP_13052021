from bs4 import BeautifulSoup as BS
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


def extractor(url):
    #Get the home page and all the pagination
    #For each pages was got, get all found books
    #Return a list of page_book:

    books_list = []
    hyper_menu = getHtml(url)
    a = 0
    if hyper_menu:
        menu_page = BS(hyper_menu, 'html.parser')
        hyper_pagination = menu_page.find('li', {'class': "current"})
        if hyper_pagination:
            pages_count = int(hyper_pagination.text.split("Page 1 of")[1])
        else:
            pages_count = 1
        for page_id in range(pages_count):
            page_id += 1
            if page_id > 1:
                page_url = urllib.parse.urljoin(url, 'catalogue/page-{}.html'.format(page_id))
                current_page = getHtml(page_url)
                current_soup = BS(current_page, 'html.parser')
                books_elements = current_soup.find_all('article', {'class': "product_pod"})

                for book_element in books_elements:
                    book_url = urllib.parse.urljoin(url, "catalogue/" + book_element.a['href'])
                    book_page = getHtml(book_url)
                    sys.stdout.write('\r' + str(a))
                    a+=1
                    book_soup = BS(book_page, 'html.parser')
                    url_tag = book_soup.new_tag("div", id="selfURL", url=book_url)
                    book_soup.append(url_tag)
                    books_list.append(book_soup)

                    # debugging
                    if a == 10:
                        return books_list
        return books_list
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
    organized_books = {}
    for page_book in extracted_data:
        url_parent = page_book.find('div', {'id': "selfURL"})
        url = url_parent['url']

        tables = page_book.find_all("table")
        for table in tables:
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

        description = page_book.find('div', {'id': "product_description"}).findNext('p').text

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
   # print(organized_books)
    return organized_books

def loader(transformed_data):
    # Run through the transformed_data
    # Saving all elements as a [category_name].csv
    return True

def main():
    extracted_data = extractor("http://books.toscrape.com/index.html")
    if extracted_data:
        transformed_data = transformer(extracted_data)
        if transformed_data:
            loader(transformed_data)

if(__name__ == '__main__'):

    main()

