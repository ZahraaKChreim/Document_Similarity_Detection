from represent_document import get_webpage_content
import getSimilarity

def get_titles_similarity(url1, url2):
    website_title1, page_title1, list_of_subtitles1, list_of_urls1 = get_webpage_content(url1)
    website_title2, page_title2, list_of_subtitles2, list_of_urls2 = get_webpage_content(url2)

    website_titles_sim = getSimilarity.get_cosine_of_2_sentences(website_title1, website_title2)
    page_titles_sim = getSimilarity.get_cosine_of_2_sentences(page_title1, page_title2)
    subtitles_sim = getSimilarity.get_jaccard_of_two_lists_of_sentences(list_of_subtitles1, list_of_subtitles2)
    urls_sim = getSimilarity.get_jaccard_of_two_lists_of_sentences(list_of_urls1, list_of_urls2)

    return website_titles_sim, page_titles_sim, subtitles_sim, urls_sim

# url1 = "https://www.webmd.com/drugs/2/index"
# url2 = "https://www.webmd.com/drugs/2/alpha/a/"

# url1 = "https://www.emedicinehealth.com/anise/vitamins-supplements.htm"
# url2 = "https://www.rxlist.com/anise/supplements.htm"

# url3 = "https://en.wikipedia.org/wiki/Galata"
# url4 = "https://www.wikiwand.com/en/Galata"

url1 = "https://www.livius.org/articles/misc/byzantine-empire/"
url2 = "https://www.newadvent.org/cathen/03096a.htm"

website_titles_sim1, page_titles_sim1, subtitles_sim1, urls_sim1 = get_titles_similarity(url1, url2)
#website_titles_sim2, page_titles_sim2, subtitles_sim2, urls_sim2 = get_titles_similarity(url3, url4)

print("website_title:", website_titles_sim1, " - page_title", page_titles_sim1, " - subtitles:", subtitles_sim1, " - URLs:", urls_sim1)
#print("website_title:", website_titles_sim2, " - page_title", page_titles_sim2, " - subtitles:", subtitles_sim2, " - URLs:", urls_sim2)