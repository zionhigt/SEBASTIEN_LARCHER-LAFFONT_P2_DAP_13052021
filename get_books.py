from bs4 import BeautifulSoup as BS
import urllib.parse
import requests
import csv
import os
import sys
import time


# TODO:
# Extracting all the books from https://books.toscrape.com/
# Transforming got data earlier
# Loading into .csv files, each books of categories
def click_next_gen(base_url, run=True):
    # Generator function which get a url as start point
    # For each pages get, it finding for a next page button
    # It'll broke up if page or button has miss
    while run:
        page = get_html(base_url)
        if page:
            soup_point = BS(page, 'html.parser')
            next_button = soup_point.find('li', {'class', 'next'})
            if next_button:
                next_rel_url = next_button.a['href']
                next_url = urllib.parse.urljoin(base_url, next_rel_url)
                current_url = base_url
                base_url = next_url
                yield [page, current_url]
            else:
                yield [page, base_url]
                run = False
        else:
            run = False


def get_html(url):
    # Return a HTML page from an URL
    with requests.get(url) as HTML:
        if HTML.status_code == 200:
            return HTML.text
        else:
            print("La requête a échoué avec le status {} \n\r {}".format(str(HTML.status_code), url))
            return False


def get_image(url, image_location):
    # Bring a extract an load images system
    # It get image's url and relative save path from root project.
    # Path doesn't need a pictures extension just the name of file
    image_extension = os.path.splitext(url)[-1]
    image_path = image_location + image_extension
    with open(image_path, 'wb') as image:
        with requests.get(url) as IMG:
            if IMG.status_code == 200:
                image.write(IMG.content)
                image.close()
                return image_path
            else:
                print("La requête a échoué avec le status {} \n\r {}".format(str(IMG.status_code), url))
                return False


def show_time(second):
    # Convert a seconds as a --m--s format
    s = str(int(second % 60))
    s = s if len(s) == 2 else '0' + s
    show = '{}m{}s'.format(int(second / 60), s)
    return show


def extract_a_book(url):
    # Bring a book page from url
    # Injection of his own url into the page
    book_page = get_html(url)
    book_soup = BS(book_page, 'html.parser')

    url_tag = book_soup.new_tag("div", id="selfURL", url=url)
    book_soup.append(url_tag)
    return str(book_soup)


def extractor(url):
    # Get the home page and all the pagination
    # For each pages was got, get all found books
    # Return a list of page_book:

    books_list = []

    categories_pages = click_next_gen(url)
    page_id = 0

    for page in categories_pages:
        print('\n\r' + page[1])
        current_soup = BS(page[0], 'html.parser')
        books_elements = current_soup.find_all('article', {'class': "product_pod"})
        sys.stdout.write('\x1b[2K\r {} pages indexées '.format(page_id))

        book_id = 0
        page_id += 1
        for book_element in books_elements:
            rel_book_url = book_element.a['href']
            book_url = urllib.parse.urljoin(page[1], rel_book_url)
            book_page = extract_a_book(book_url)
            books_list.append(book_page)

            book_id += 1
            b = book_id % 5
            decorator = "".join(['.'] * b)
            sys.stdout.write('\x1b[2K\r téléchargement de {} livres {}'.format(book_id, decorator))

    return list(books_list)


def transformer(extracted_data):
    # Run through the extracted_data
    # Return a dictionary such as:
    """
    {
        categoryName: [{transformed_data_of_book_1}, {transformed_data_of_book_2}, ...],
        ...
    }
    """

    a = 0
    organized_books = {}  # dictionary returned

    for page in extracted_data:

        sys.stdout.write('\x1b[2K\r {}/{} livres traités'.format(a, len(extracted_data)))
        a += 1

        page_book = BS(page, 'html.parser')
        url_parent = page_book.find('div', {'id': "selfURL"})
        url = url_parent.attrs['url']
        table = page_book.find("table")
        upc = ""
        pit = 0.0
        pet = 0.0
        stock = 0
        for row in table.find_all('tr'):
            if row.th.text == "UPC":
                upc = row.td.text
            elif row.th.text == "Price (incl. tax)":
                pit = float(row.td.text.split('£')[1])
            elif row.th.text == "Price (excl. tax)":
                pet = float(row.td.text.split('£')[1])
            elif row.th.text == "Availability":
                stock = int(row.td.text.replace('In stock (', "").replace(' available)', ""))

        translate_number = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five']
        rating_element = page_book.find('p', {'class': 'star-rating'})
        rating_count_letter = rating_element.attrs['class'][1]
        rating = translate_number.index(rating_count_letter)

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

        formatted_book = {
            'product_page_url': url,
            'UPC': upc,
            'title': title,
            'price_including_tax': pit,
            'price_excluding_tax': pet,
            'number_available': stock,
            'product_description': description,
            'category': category,
            'review_rating': rating,
            'image_url': img_url
        }

        if category not in organized_books:
            organized_books[category] = []
        organized_books[category].append(formatted_book)

    return organized_books


def loader(transformed_data):
    # Run through the transformed_data
    # Saving all elements as a [category_name].csv

    data_folder = 'data'
    if not os.path.isdir(data_folder):
        os.system("mkdir {}".format(data_folder))

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
        clean_cat_name = category.lower().replace(" ", "_")
        cat_folder = os.path.join(data_folder, clean_cat_name)
        if not os.path.isdir(cat_folder):
            os.system("mkdir {}".format(cat_folder))

        images_folder = os.path.join(cat_folder, 'images')
        if not os.path.isdir(images_folder):
            os.system("mkdir {}".format(images_folder))

        # Get the book's images
        save_image = map(lambda book: get_image(book['image_url'], os.path.join(images_folder, book['UPC'])),
                         transformed_data[category])
        for i in save_image:
            sys.stdout.write('\x1b[2K\r {} à été créé'.format(i))
        file_data_name = clean_cat_name + '.csv'
        with open(os.path.join(cat_folder, file_data_name), 'w', encoding="utf-8") as save_data_file:
            writer = csv.DictWriter(save_data_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(transformed_data[category])
            sys.stdout.write('\x1b[2K\r {} à été créé'.format(file_data_name))

    return True


def main():
    time_start = time.perf_counter()

    extracted_data = extractor("http://books.toscrape.com/index.html")
    if extracted_data:
        transformed_data = transformer(extracted_data)
        if transformed_data:
            loader(transformed_data)
            print("\n\r" + show_time(round(time.perf_counter() - time_start, 3)))


if __name__ == '__main__':
    main()
