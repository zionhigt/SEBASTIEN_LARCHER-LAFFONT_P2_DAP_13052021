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
    #Return a list of books:

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
                    books_list.append(book_soup)
        print(books_list)
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
    return True

def loader(transformed_data):
    # Run through the transformed_data
    # Saving all elements as a [category_name].csv
    return True

def main():
    extracted_data = extractor("http://books.toscrape.com/index.html")
    transformed_data = transformer(extracted_data)
    loader(transformed_data)

if(__name__ == '__main__'):

    main()

