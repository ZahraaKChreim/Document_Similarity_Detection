from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import preprocess
import getSimilarity

def get_webpage_content(url):

    #######################################################
    ################ Driver Initialization ################
    #######################################################

    #print("Driver Initialization ...")
    driver = webdriver.Chrome('chromedriver')
    #print("Driver Initialization Done")
    #print("-------------------------------------------------------------------------------------------------")

    #######################################################
    ################# Getting the website #################
    #######################################################

    #print("Getting the Website ...")
    driver.get(url)
    #print("Getting the Website Done")
    #print("-------------------------------------------------------------------------------------------------")

    #######################################################
    ########### Getting the Website/Driver Title ##########
    #######################################################

    # print("Getting the Website/Driver Title ...")
    website_title = (driver.title).lower()
    # print("Website/Driver Title: ", website_title)
    # print("-------------------------------------------------------------------------------------------------")


    #######################################################
    ############### Getting the Page's Title ##############
    #######################################################

    #print("Getting the Page's Title ...")
    ## page_title = first h1 element
    try:
        first_h1_element = driver.find_element_by_xpath("//h1")
        page_title = (first_h1_element.text).lower()
        #print("Page Title: ",page_title)
    except NoSuchElementException:
        page_title = ""
        #print("NoSuchElementException - no <h1> element - no Page Title")
        pass
    #print("Getting the Page's Title Done")
    #print("-------------------------------------------------------------------------------------------------")

    #######################################################
    ############# Getting the Page's SubTitles ############
    #######################################################

    # print("Getting the Page's SubTitles ...")
    # h16_elements = driver.find_elements_by_xpath("//h1/*[1] | //h2/*[1] | //h3/*[1] | //h4/*[1]")
    # h16_elements = h16_elements[1:]
    # list_of_subtitles = []
    # for subtitle in h16_elements:
    #     if subtitle.text:
    #         list_of_subtitles.append((subtitle.text).lower())
            #print("Tag: ",subtitle.tag_name,"Text: ",subtitle.text)
    # #print("list_of_subtitles length: ",len(list_of_subtitles))        
    # print("Getting the Page's SubTitles Done ...")
    # print("-------------------------------------------------------------------------------------------------")


    #######################################################
    ##### Getting the Page's Non Empty Text Paragraphs ####
    #######################################################

    #print("Getting the Page's Non Empty Text Paragraphs ...")
    list_of_paragraphs = driver.find_elements_by_xpath("//p")
    #print("list_of_paragraphs length: ",len(list_of_paragraphs))
    list_of_text_paragraphs = []
    for paragraph in list_of_paragraphs:
        if paragraph.text:
            list_of_text_paragraphs.append(paragraph.text)
            #print("Tag: ",paragraph.tag_name," - Text: ",paragraph.text)
            #print("#################################")
    #print("list_of_text_paragraphs length: ",len(list_of_text_paragraphs))
    #text_paragraphs_single_string = ' '.join(str(paragraph) for paragraph in list_of_text_paragraphs)
    #print("Getting the Page's Non Empty Text Paragraphs Done ...")
    #print("-------------------------------------------------------------------------------------------------")


    #######################################################
    ############ Getting all the Page's Links #############
    #######################################################

    # print("Getting all the Page's Links ...")
    # list_of_links_a = driver.find_elements_by_tag_name("a")
    # print("list_of_links_a length: ",len(list_of_links_a))
    # list_of_urls = []
    # for link in list_of_links_a:
    #     try:
    #         # parent = link.find_element_by_xpath("..")
    #         # print("Parent: ",parent.tag_name, " - Tag: ",link.tag_name, " - Text: ",link.text, " - URL: ",link.get_attribute('href'))
    #         print("Tag: ",link.tag_name, " - Text: ",link.text, " - URL: ",link.get_attribute('href'))
    #         if link.get_attribute('href'):
    #             list_of_urls.append(link.get_attribute('href'))
    #     except StaleElementReferenceException:
    #         print("StaleElementReferenceException")
    #         break
    #     print("#################################")
    # print("Getting all the Page's Links Done ...")
    # print("-------------------------------------------------------------------------------------------------")

    #######################################################
    ######### Getting some of the Page's Links ###########$
    #######################################################

    #print("Getting some of the Page's Links ...")
    # list_of_links_a = driver.find_elements_by_xpath('//p/a | //ul/li/*/a | //ul/li/a | //ol/li/a')
    # list_of_urls = []
    # for link in list_of_links_a:
    #     try:
    #         if link.get_attribute('href') and link.get_attribute('href').startswith("http") and link.text:
    #             #parent = link.find_element_by_xpath("..")
    #             list_of_urls.append(link.get_attribute('href'))
    #             #print("Parent: ",parent.tag_name, " - Tag: ",link.tag_name, " - Text: ",link.text, " - URL: ",link.get_attribute('href'))
    #             #print("#################################")
    #     except StaleElementReferenceException:
    #         #print("StaleElementReferenceException")
    #         pass
    #print("list_of_urls length: ",len(list_of_urls))
    #print("Getting some of the Page's Links Done ...")
    #print("-------------------------------------------------------------------------------------------------")

    driver.close()

    #return website_title, page_title, list_of_subtitles, list_of_text_paragraphs, list_of_urls
    #return page_title, list_of_text_paragraphs, text_paragraphs_single_string
    return list_of_text_paragraphs
    #return website_title, page_title, list_of_subtitles, list_of_urls

#######################################################
########## Check Similarity of 2 websites  ############
#######################################################

def check_2_websites_similarity(url1, url2):

    print("-------------------------------------------------------------------------------------------------")
    print("Get Webpage 1 Content ...")
    print("-------------------------------------------------------------------------------------------------")
    #url1_website_title, url1_page_title, url1_list_of_subtitles, url1_list_of_text_paragraphs = get_webpage_content(url1)
    list_of_urls1 = get_webpage_content(url1)
    print("-------------------------------------------------------------------------------------------------")
    print("Get Webpage 1 Content Done")
    print("-------------------------------------------------------------------------------------------------")

    print('\n' * 2)

    print("-------------------------------------------------------------------------------------------------")
    print("Get Webpage 2 Content ...")
    #url2_website_title, url2_page_title, url2_list_of_subtitles, url2_list_of_text_paragraphs = get_webpage_content(url2)
    list_of_urls2 = get_webpage_content(url2)
    print("Get Webpage 2 Content Done")
    print("-------------------------------------------------------------------------------------------------")

    # url1_text_paragraphs_single_string = ' '.join(str(paragraph) for paragraph in url1_list_of_text_paragraphs)
    # url2_text_paragraphs_single_string = ' '.join(str(paragraph) for paragraph in url2_list_of_text_paragraphs)

    #######################################################
    ####### Check Similarity of websites titles  ##########
    #######################################################

    # print("Websites Titles:")
    # websites_titles_cosine = get_cosine_similarity_of_two_strings(url1_website_title, url2_website_title)
    # websites_titles_jaccard = get_jaccard_similarity_of_two_strings(url1_website_title, url2_website_title)
    # print("-------------------------------------------------------------------------------------------------")

    # print("Pages Titles:")
    # pages_titles_cosine = get_cosine_similarity_of_two_strings(url1_page_title, url2_page_title)
    # pages_titles_jaccard = get_jaccard_similarity_of_two_strings(url1_page_title, url2_page_title)
    # print("-------------------------------------------------------------------------------------------------")

    # print("Pages Subtitles:")
    # subtitles_cosine = get_cosine_similarity_of_two_lists_of_strings(url1_list_of_subtitles, url2_list_of_subtitles)
    # subtitles_jaccard = get_jaccard_similarity_of_two_lists_of_strings(url1_list_of_subtitles, url2_list_of_subtitles)
    # print("-------------------------------------------------------------------------------------------------")

    # print("Pages Text Paragraphs as Lists:")
    # list_text_paragraphs_cosine = get_cosine_similarity_of_two_lists_of_strings(url1_list_of_text_paragraphs, url2_list_of_text_paragraphs)
    # list_text_paragraphs_jaccard = get_jaccard_similarity_of_two_lists_of_strings(url1_list_of_text_paragraphs, url2_list_of_text_paragraphs)
    # print("-------------------------------------------------------------------------------------------------")

    # print("Pages Text Paragraphs as single string:")
    # single_string_text_paragraphs_cosine = get_cosine_similarity_of_two_strings(url1_text_paragraphs_single_string, url2_text_paragraphs_single_string)
    # single_string_text_paragraphs_jaccard = get_jaccard_similarity_of_two_strings(url1_text_paragraphs_single_string, url2_text_paragraphs_single_string)
    # print("-------------------------------------------------------------------------------------------------")

    print("Pages List of URLs:")
    list_of_urls_matching_rate = get_similarity_of_two_lists_of_urls(list_of_urls1, list_of_urls2)
    print("-------------------------------------------------------------------------------------------------")

    # return websites_titles_cosine, pages_titles_cosine, subtitles_cosine, list_text_paragraphs_cosine, single_string_text_paragraphs_cosine, websites_titles_jaccard, pages_titles_jaccard, subtitles_jaccard, list_text_paragraphs_jaccard, single_string_text_paragraphs_jaccard
    return list_of_urls_matching_rate

def get_cosine_similarity_of_two_strings(string1, string2):

    syntactically_preprocessed_string1 = preprocess.get_syntactically_preprocessed_string(string1)
    syntactically_preprocessed_string2 = preprocess.get_syntactically_preprocessed_string(string2)
    
    return getSimilarity.get_cosine_of_2_sentences(syntactically_preprocessed_string1, syntactically_preprocessed_string2)

    semantically_preprocessed_string1 = preprocess.get_semantically_preprocessed_string(string1)
    semantically_preprocessed_string2 = preprocess.get_semantically_preprocessed_string(string2)
    
    return getSimilarity.get_cosine_of_2_sentences(semantically_preprocessed_string1, semantically_preprocessed_string2)

def get_cosine_similarity_of_two_lists_of_strings(list_of_strings1, list_of_strings2):

    syntactically_preprocessed_list_of_strings1 = preprocess.get_syntactically_preprocessed_list_of_strings(list_of_strings1)
    syntactically_preprocessed_list_of_strings2 = preprocess.get_syntactically_preprocessed_list_of_strings(list_of_strings2)

    return getSimilarity.get_average_cosine_of_2_lists_of_sentences(syntactically_preprocessed_list_of_strings1, syntactically_preprocessed_list_of_strings2)

    semantically_preprocessed_list_of_strings1 = preprocess.get_semantically_preprocessed_list_of_strings(list_of_strings1)
    semantically_preprocessed_list_of_strings2 = preprocess.get_semantically_preprocessed_list_of_strings(list_of_strings2)

    return getSimilarity.get_average_cosine_of_2_lists_of_sentences(semantically_preprocessed_list_of_strings1, semantically_preprocessed_list_of_strings2)

def get_jaccard_similarity_of_two_strings(string1, string2):

    syntactically_preprocessed_string1 = preprocess.get_syntactically_preprocessed_string(string1)
    syntactically_preprocessed_string2 = preprocess.get_syntactically_preprocessed_string(string2)
    
    return getSimilarity.get_jaccard_of_two_sentences(syntactically_preprocessed_string1, syntactically_preprocessed_string2)

    semantically_preprocessed_string1 = preprocess.get_semantically_preprocessed_string(string1)
    semantically_preprocessed_string2 = preprocess.get_semantically_preprocessed_string(string2)
    
    return getSimilarity.get_jaccard_of_two_sentences(semantically_preprocessed_string1, semantically_preprocessed_string2)

def get_jaccard_similarity_of_two_lists_of_strings(list_of_strings1, list_of_strings2):

    syntactically_preprocessed_list_of_strings1 = preprocess.get_syntactically_preprocessed_list_of_strings(list_of_strings1)
    syntactically_preprocessed_list_of_strings2 = preprocess.get_syntactically_preprocessed_list_of_strings(list_of_strings2)

    return getSimilarity.get_average_jaccard_of_two_lists_of_sentences(syntactically_preprocessed_list_of_strings1, syntactically_preprocessed_list_of_strings2)

    semantically_preprocessed_list_of_strings1 = preprocess.get_semantically_preprocessed_list_of_strings(list_of_strings1)
    semantically_preprocessed_list_of_strings2 = preprocess.get_semantically_preprocessed_list_of_strings(list_of_strings2)

    return getSimilarity.get_average_jaccard_of_two_lists_of_sentences(semantically_preprocessed_list_of_strings1, semantically_preprocessed_list_of_strings2)

def get_similarity_of_two_lists_of_urls(list_of_urls1,list_of_urls2):

    intersection = list(set(list_of_urls1) & set(list_of_urls2))
    sim1_2 = len(intersection) / (len(list_of_urls2))
    sim2_1 = len(intersection) / (len(list_of_urls1))
    # union = list(set(list_of_urls1) | set(list_of_urls2))
    # return intersection / union
    return  (sim1_2 + sim2_1)/2


#######################################################
######################## test  ########################
#######################################################

# url1 = "https://en.wikipedia.org/wiki/Galata"
# url2 = "https://www.wikiwand.com/en/Galata"

# url1 = "https://medium.com/@ashukumar27/similarity-functions-in-python-aa6dfe721035"
# url2 = "https://dataaspirant.com/five-most-popular-similarity-measures-implementation-in-python/"

# websites_titles_cosine, pages_titles_cosine, subtitles_cosine, list_text_paragraphs_cosine, single_string_text_paragraphs_cosine, websites_titles_jaccard, pages_titles_jaccard, subtitles_jaccard, list_text_paragraphs_jaccard, single_string_text_paragraphs_jaccard = check_2_websites_similarity(url1,url2)
# print("websites_titles: cosine = ", websites_titles_cosine, " - jaccard = ", websites_titles_jaccard)
# print("pages_titles: cosine = ", pages_titles_cosine, " - jaccard = ", pages_titles_jaccard)
# print("subtitles: cosine = ", subtitles_cosine, " - jaccard = ", subtitles_jaccard)
# print("list_text_paragraphs: cosine = ", list_text_paragraphs_cosine, " - jaccard = ", list_text_paragraphs_jaccard)
# print("single_string_text_paragraphs: cosine = ", single_string_text_paragraphs_cosine, " - jaccard = ", single_string_text_paragraphs_jaccard)

# list_of_urls_matching_rate = check_2_websites_similarity(url1,url2)
# print("list_of_urls: matching rate = ", list_of_urls_matching_rate)