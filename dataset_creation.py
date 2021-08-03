from selenium import webdriver
import pandas as pd
import database_handler
import document
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
import getSimilarity

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
        queries.append(query.strip())
    
    print("Get Queries From File Function Done")
    return queries

def get_URLs_of_query(driver: webdriver.Chrome, query):

    print("Get URLs Of Query Function Started... Query:", query)
    # Search Query on Google.com
    #driver.get("https://www.google.com/")
    driver.get("https://www.google.com/search?q="+query)
    fastrack = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "L2AGLb")))
    fastrack.click()
    # search = driver.find_element_by_name("q")
    # search.send_keys(query)
    # search.send_keys(Keys.RETURN)

    # Get Query's results urls
    list_of_URLs = []
    # Starting with current page (first page)
    URLs = driver.find_elements_by_class_name("yuRUbf")
    for URL_element in URLs:
        list_of_URLs.append(URL_element.find_element_by_tag_name("a").get_attribute('href'))
    # Extract Data till page number 10
    for i in range(2, 11): # 2 -> 10
        go_to_next_page(driver, i)
        # Now Get URLs
        URLs = driver.find_elements_by_class_name("yuRUbf")
        for URL_element in URLs:
            list_of_URLs.append(URL_element.find_element_by_tag_name("a").get_attribute('href'))

    print("Get URLs Of Query Function Done, Query:", query)
    return list_of_URLs


def extract_data(file_name):

    logfile = open("logfile.txt", "w")

    print("Extract Data Function Started... File:", file_name)
    # Get domain & lang of queries in current file
    lang_domain = ((file_name.split("."))[0]).split("_")
    lang = lang_domain[0]
    domain = lang_domain[1]

    # Get all queries in file
    file_name = "Queries/" + file_name
    queries = get_queries_from_file(file_name)
    queries_count = len(queries)

    # For each query, get its urls results, iterate them and get their page content and save to Database
    i = 1
    for query in queries:
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("'--disable-software-rasterizer'")
        driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
        #driver = webdriver.Chrome(executable_path='chromedriver')
        
        list_of_URLs_of_query = get_URLs_of_query(driver, query)
        urls_of_query_count = len(list_of_URLs_of_query)

        j = 1
        for url in list_of_URLs_of_query:

            if j%6 == 0:
                driver.close()
                #driver = webdriver.Chrome(executable_path='chromedriver')
                driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
            
            print("url", j, "of", urls_of_query_count, "/ Query", i, "of", queries_count, ":", query, "/ File:", file_name)
            j = j + 1

            # Get Content
            try:
                website_title, page_title, list_of_subtitles, list_of_urls, text_paragraphs_single_string = document.get_webpage_content(driver, url)
                subtitles = "___".join(subtitle for subtitle in list_of_subtitles)
                urls = "___".join(url for url in list_of_urls)

                # Save (insert) To Database
                if db.insert_into_db(lang, domain, query, url, website_title, page_title, subtitles, urls, text_paragraphs_single_string):
                    logfile.write("Insert Done url: "+ url + " Query: " + query + '\n')
                else:
                    logfile.write("Insert Error in url: "+ url + " Query: " + query + '\n')      

            except TimeoutException as TO_ex:
                print("TimeoutException while getting content of"+ url + " of Query: " + query)
                continue
            except WebDriverException as WD_ex:
                print("TimeoutException while getting content of"+ url + " of Query: " + query)
                continue 
            except Exception as ex:
                print("Exception while getting content of"+ url + " of Query: " + query)
                print(format(ex))
                continue
            

        i = i + 1   
        driver.close()

    print("Extract Data Function Done, File:", file_name)
    logfile.close()   

def extract_all_data():

    print("Extract All Data Function Started...")
    import os
    files = os.listdir("Queries/")
    # Iterate through all files
    for file_name in files:
        extract_data(file_name)

    print("Extract All Data Function Done")

def error():
    logfile = open("logfile.txt", "w")
    lang = 'en'
    domain = 'history'
    query = 'crusades'

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("'--disable-software-rasterizer'")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
    #driver = webdriver.Chrome(executable_path='chromedriver')
    
    list_of_URLs_of_query = get_URLs_of_query(driver, query)
    urls_of_query_count = len(list_of_URLs_of_query)
    list_of_URLs_of_query = list_of_URLs_of_query[94:]
    driver.close()

    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
    #driver = webdriver.Chrome(executable_path='chromedriver')
    j = 95
    for url in list_of_URLs_of_query:

        if j%6 == 0:
            driver.close()
            #driver = webdriver.Chrome(executable_path='chromedriver')
            driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
        
        print("url", j, " of ", urls_of_query_count, "/ Query ", query)
        j = j + 1

        # Get Content
        try:
            website_title, page_title, list_of_subtitles, list_of_urls, text_paragraphs_single_string = document.get_webpage_content(driver, url)
            subtitles = "___".join(subtitle for subtitle in list_of_subtitles)
            urls = "___".join(url for url in list_of_urls)

            # Save (insert) To Database
            if db.insert_into_db(lang, domain, query, url, website_title, page_title, subtitles, urls, text_paragraphs_single_string):
                logfile.write("Insert Done url: "+ url + " Query: " + query + '\n')
            else:
                logfile.write("Insert Error in url: "+ url + '\n')      

        except TimeoutException as TO_ex:
            print("TimeoutException while getting content of"+ url + " of Query: " + query)
            continue
        except WebDriverException as WD_ex:
            print("TimeoutException while getting content of"+ url + " of Query: " + query)
            continue  
        except Exception as ex:
            print("Exception while getting content of"+ url + " of Query: " + query)
            print(format(ex))
            continue

    driver.close()

def test():

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("'--disable-software-rasterizer'")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)


    url = "http://www.sem.admin.ch/dam/sem/fr/data/asyl/verfahren/hb/c/hb-c2-f.pdf"

    website_title, page_title, list_of_subtitles, list_of_urls, text_paragraphs_single_string = document.get_webpage_content(driver, url)
    #print(website_title, '\n', page_title, '\n', list_of_subtitles, '\n', list_of_urls)
    #driver.close()

    db = database_handler.databaseHandler()
    results_from_db = db.select_from_db_by_url(url)
    db.con.close()

    if results_from_db.get('subtitles') == '':
        subtitles = ''
    else:
        subtitles = results_from_db.get('subtitles').split("___")
    if results_from_db.get('urls') == '':
        urls = ''
    else:
        urls = results_from_db.get('urls').split("___")

    from getSimilarity import get_jaccard_of_two_lists_of_sentences as jc, get_cosine_of_2_sentences as cosine

    same = True

    if website_title != results_from_db.get('website_title'):
        print("############################")
        same = False
        print("website_title not same!")
        print("Retrieve:",website_title)
        print("From Database",results_from_db.get('website_title'))
        print("############################")
    if page_title != results_from_db.get('page_title'):
        print("############################")
        same = False
        print("page_title not same!")
        print("Retrieve:",page_title)
        print("From Database",results_from_db.get('page_title'))
        print("############################")

    if subtitles != '' and list_of_subtitles != '' and jc(subtitles, list_of_subtitles)  != 1:
        print("############################")
        same = False
        print("subtitles not same!")
        print("Retrieve:",subtitles)
        print("From Database",results_from_db.get('subtitles'))
        print("############################")

    if jc(urls, list_of_urls)  != 1:
        print("############################")
        same = False
        print("urls not same!")
        print("Retrieve:",urls)
        print("From Database",results_from_db.get('urls'))
        print("############################")
    if text_paragraphs_single_string != results_from_db.get('body'):
        print("############################")
        same = False
        print("body not same!")
        print("############################")
        print("------------------------------------")
        print(text_paragraphs_single_string)
        print("------------------------------------")
        print(results_from_db.get('body'))
        print("------------------------------------")
        print(cosine(text_paragraphs_single_string, results_from_db.get('body')))
    if same:
        print("############################")
        print("ALL SAME !!")
        print("############################")
    else:
        print("############################")
        print("SOMETHING DIFFERENT")
        print("############################")

def calculate_similarity_and_export_to_csv(query):

    print("Function calculate_similarity_and_export_to_csv Started...")

    columns = ['id1', 'id2', 'similarity']
    list_of_ids1 = []
    list_of_ids2 = []
    list_of_similarities = []

    records_of_query = db.select_from_db_by_query(query)

    total = len(records_of_query)
    r1 = 1
    for i in range(total):
        record1 = records_of_query[i]
        r2 = r1+1
        for record2 in records_of_query[i+1:]:
            print (query, ':', r1, '-', r2, '(', total, ')')
            r2 += 1

            final_similarity_score = getSimilarity.get_similarity_record1_record2(record1, record2)

            list_of_ids1.append(record1.get('id'))
            list_of_ids2.append(record2.get('id'))
            list_of_similarities.append(final_similarity_score)
        r1 += 1

    data = {
        'id1':list_of_ids1,
        'id2':list_of_ids2,
        'similarity': list_of_similarities
    }
    df = pd.DataFrame(data, columns= columns)
    file_name = query + "_data.csv"
    file_name = r''+file_name
    df.to_csv (file_name, index = True, header=True)

    print("Function calculate_similarity_and_export_to_csv Done")

if __name__ ==  '__main__':

    print("Dataset Creation Main Started...") 

    db = database_handler.databaseHandler()
    print("MySQL connection is opened")

    #error()
    #extract_all_data()  

    query = 'crusades'
    calculate_similarity_and_export_to_csv(query)

    query = 'benefits of anise'
    calculate_similarity_and_export_to_csv(query)

    if db.con.is_connected():
        db.con.close()
        print("MySQL connection is closed")

    print("Dataset Creation Main Finished...")
    print("Dataset Successfully Created!!")

    #test()
    