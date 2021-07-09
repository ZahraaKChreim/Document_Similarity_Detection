from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_webpage_content(driver, url):

    #######################################################
    ################# Getting the website #################
    #######################################################

    #print("Getting the Website ...")
    driver.get(url)
    #print("Getting the Website Done")
    #print("-------------------------------------------------------------------------------------------------")

    #######################################################
    ############### Getting the Page's Title ##############
    #######################################################

    #print("Getting the Page's Title ...")
    ## page_title = first h1 element
    try:
        first_h1_element = driver.find_element_by_xpath("//h1")
        page_title = first_h1_element.text
        #print("Page Title: ",page_title)
    except NoSuchElementException:
        page_title = ""
        print("NoSuchElementException - no <h1> element - no Page Title")
        pass
    #print("Getting the Page's Title Done")
    #print("-------------------------------------------------------------------------------------------------")


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
    text_paragraphs_single_string = ' '.join(str(paragraph) for paragraph in list_of_text_paragraphs)
    #print("Getting the Page's Non Empty Text Paragraphs Done ...")
    #print("-------------------------------------------------------------------------------------------------")

    return page_title, list_of_text_paragraphs, text_paragraphs_single_string