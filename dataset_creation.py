from selenium import webdriver
import database_handler
import document
    

def go_to_next_page(driver: webdriver.Chrome, page_nb: int):
    print("Go To Next Page Function Started...")
    next_page = driver.find_element_by_css_selector("[aria-label='Page " + str(page_nb) + "']")
    next_page.click()
    print("Go To Next Page Function Done")

def get_queries_from_file(file_name):
    print("Get Queries From File Function Started...")
    queries = []
    queries_file = open(file_name, "r")
    for query in queries_file.readlines():
        queries.append(query)
    
    print("Get Queries From File Function Done")
    return queries

def get_URLs_of_query(driver: webdriver.Chrome, query):

    print("Get URLs Of Query Function Started...")
    # Search Query on Google.com
    driver.get("https://www.google.com")
    search = driver.find_element_by_name("q")
    search.send_keys(query)
    search.submit()

    # Get Query's results urls
    list_of_URLs = []
    # Starting with current page (first page)
    URLs = driver.find_element_by_class_name("yuRUbf")
    for URL_element in URLs:
        list_of_URLs.append(URL_element.find_elements_by_tag_name("a").get_attribute('href'))
    # Extract Data till page number 10
    for i in range(2, 11): # 2 -> 10
        go_to_next_page(driver, i)
        # Now Get URLs
        URLs = driver.find_element_by_class_name("yuRUbf")
        for URL_element in URLs:
            list_of_URLs.append(URL_element.find_elements_by_tag_name("a").get_attribute('href'))

    print("Get URLs Of Query Function Done")
    return list_of_URLs


def extract_data(file_name):

    print("Extract Data Function Started...")
    # Get domain & lang of queries in current file
    lang_domain = ((file_name.split("."))[0]).split("_")
    lang = lang_domain[0]
    domain = lang_domain[1]

    # Get all queries in file
    file_name = "Queries/" + file_name
    queries = get_queries_from_file(file_name)

    
    # For each query, get its urls results, iterate them and get their page content and save to Database
    for query in queries:
        driver = webdriver.Chrome('chromedriver')
        list_of_URLs_of_query = get_URLs_of_query(driver, query)

        for url in list_of_URLs_of_query:
            # Get Content
            website_title, page_title, list_of_subtitles, list_of_urls, text_paragraphs_single_string = document.get_webpage_content(driver, url)
            
            subtitles = "___".join(subtitle for subtitle in list_of_subtitles)
            urls = "___".join(url for url in list_of_urls)

            # Save (insert) To Database
            db.insert_into_db(lang, domain, query, url, website_title, page_title, subtitles, urls, text_paragraphs_single_string)
            
        driver.close()
    print("Extract Data Function Done")
    

def extract_all_data():

    print("Extract All Data Function Started...")
    import os
    files = os.listdir("Queries/")
    # Iterate through all files
    for file_name in files:
        extract_data(file_name)

    print("Extract All Data Function Done")

if __name__ ==  '__main__':
    print("main")

    db = database_handler.databaseHandler()
    print("MySQL connection is opened")


    #extract_all_data()

    if db.con.is_connected():
        db.con.close()
        print("MySQL connection is closed")