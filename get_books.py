#TODO
#Extracting all the books from booktosrcap.com
#Transforming got data later
#Loading into .csv files, each books of categories

def extractor(url):
    #Get the list of categories from the home page
    #For each category listed, get all pages of them.
    #For each pages was got, get all found books
    #Return a dictionary such as:
    """
    {
        categoryName: [hyper_text_of_book_1, hyper_text_of_book_2, ...],
        ...
    }
    """
    return True

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
    # Run through the extracted_data
    # Saving all elements as a [category_name].csv
    return True

def main():
    extracted_data = extractor("http://booktoscrap.com/index.html")
    transformed_data = transformer(extracted_data)
    loader(transformed_data)

if(__name__ == '__main__'):

    main()