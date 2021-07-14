from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def get_webpage_content(driver, url):

    driver.get(url)
    website_title = (driver.title).lower()

    ## Page_title = first h1 element
    try:
        first_h1_element = driver.find_element_by_xpath("//h1")
        page_title = (first_h1_element.text).lower()
    except NoSuchElementException:
        page_title = ""
        pass

    ## Subtitles
    h16_elements = driver.find_elements_by_xpath("//h1/*[1] | //h2/*[1] | //h3/*[1] | //h4/*[1]")
    h16_elements = h16_elements[1:]
    list_of_subtitles = []
    for subtitle in h16_elements:
        if subtitle.text:
            list_of_subtitles.append((subtitle.text).lower())

    ## Body Text Paragraphs
    list_of_paragraphs = driver.find_elements_by_xpath("//p")
    list_of_text_paragraphs = []
    for paragraph in list_of_paragraphs:
        if paragraph.text:
            list_of_text_paragraphs.append(paragraph.text)
    text_paragraphs_single_string = ' '.join(str(paragraph) for paragraph in list_of_text_paragraphs)

    ## URLs
    list_of_links_a = driver.find_elements_by_xpath('//p/a | //ul/li/*/a | //ul/li/a | //ol/li/a')
    list_of_urls = []
    for link in list_of_links_a:
        try:
            if link.get_attribute('href') and link.get_attribute('href').startswith("http") and link.text:
                list_of_urls.append(link.get_attribute('href'))
        except StaleElementReferenceException:
            pass

    return website_title, page_title, list_of_subtitles, list_of_urls, text_paragraphs_single_string