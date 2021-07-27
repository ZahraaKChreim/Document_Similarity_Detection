# https://math.stackexchange.com/questions/2087801/how-to-measure-the-similarity-between-two-graph-networks
# https://github.com/peterewills/NetComp/blob/master/netcomp/distance/exact.py

from graph_of_words import GraphOfWords
from document import get_webpage_content
import preprocess
import numpy as np
import getSimilarity

from selenium import webdriver

def vertex_edge_overlap(g1,g2):
    # Code from: https://github.com/peterewills/NetComp/blob/master/netcomp/distance/exact.py
    # graphs not necessary same number of vertices !!
    
    # Getting sets of vertices & edges
    V1,V2 = [set(G.nodes()) for G in [g1,g2]]
    E1,E2 = [set(G.edges()) for G in [g1,g2]]

    V_overlap = len(V1|V2)
    E_overlap = len(E1|E2)
    vertex_edge_overlap_value = (V_overlap + E_overlap) / (len(V1)+len(V2)+len(E1)+len(E2))

    # Similarity Value from Vertex_Edge Overlap Value
    vertex_edge_sim = np.abs(1-vertex_edge_overlap_value)/vertex_edge_overlap_value
    if vertex_edge_sim > 1:
        vertex_edge_sim = 1 / vertex_edge_sim

    return vertex_edge_overlap_value, vertex_edge_sim


def get_similarities(driver, url1, url2):

    # results to return in dictionary
    results = {}

    results['url1'] = url1
    results['url2'] = url2

    # get websites content
    website_title1, page_title1, list_of_subtitles1, list_of_urls1, body_text1 = get_webpage_content(driver, url1)
    website_title2, page_title2, list_of_subtitles2, list_of_urls2, body_text2 = get_webpage_content(driver, url2) 

    #get website titles, page titles, subtitles, and URLs similarity
    website_titles_sim = getSimilarity.get_cosine_of_2_sentences(website_title1, website_title2)
    page_titles_sim = getSimilarity.get_cosine_of_2_sentences(page_title1, page_title2)
    subtitles_sim = getSimilarity.get_jaccard_of_two_lists_of_sentences(list_of_subtitles1, list_of_subtitles2)
    urls_sim = getSimilarity.get_jaccard_of_two_lists_of_sentences(list_of_urls1, list_of_urls2)

    results['website_titles_sim'] = website_titles_sim
    results['page_titles_sim'] = page_titles_sim
    results['subtitles_sim'] = subtitles_sim
    results['urls_sim'] = urls_sim

    # Syntactic & Semantic Preprocessing
    syntactically_preprocessed_body_text1 = preprocess.get_syntactically_preprocessed_paragraph(body_text1)
    syntactically_preprocessed_body_text2 = preprocess.get_syntactically_preprocessed_paragraph(body_text2)

    semantically_preprocessed_paragraph1, semantically_preprocessed_paragraph_as_list_of_sentences1 = preprocess.get_semantically_preprocessed_paragraph(body_text1)
    semantically_preprocessed_paragraph2, semantically_preprocessed_paragraph_as_list_of_sentences2 = preprocess.get_semantically_preprocessed_paragraph(body_text2)

    # Get Cosine similarities for both: Syntactic & Semantic Preprocessing
    cosine_similarity_syntactic_preprocessing = getSimilarity.get_cosine_of_2_sentences(syntactically_preprocessed_body_text1, syntactically_preprocessed_body_text2)
    cosine_similarity_semantic_preprocessing  = getSimilarity.get_cosine_of_2_sentences(semantically_preprocessed_paragraph1, semantically_preprocessed_paragraph2)

    results['cosine_similarity_syntactic_preprocessing'] = cosine_similarity_syntactic_preprocessing
    results['cosine_similarity_semantic_preprocessing'] = cosine_similarity_semantic_preprocessing

    # Graph Representation
    graph1 = GraphOfWords(window_size=4)
    graph1.build_graph(semantically_preprocessed_paragraph_as_list_of_sentences1, workers=4)
    g1 = graph1.graph

    graph2 = GraphOfWords(window_size=4)
    graph2.build_graph(semantically_preprocessed_paragraph_as_list_of_sentences2, workers=4)
    g2 = graph2.graph  

    veo_val, veo_sim = vertex_edge_overlap(g1, g2)
    results['veo_val']=veo_val
    results['veo_sim']=veo_sim

    p_w = 0
    p_t = 0
    p_s = 0
    p_u = 0
    p_c = 0
    p_g = 0
    final_sim = p_w*website_titles_sim + p_t*page_titles_sim + p_s*subtitles_sim + p_u*urls_sim + p_c*cosine_similarity_syntactic_preprocessing + p_g*veo_sim
    return results

def main():

    urls = (["https://www.webmd.com/drugs/2/index","https://www.webmd.com/drugs/2/alpha/a/"],
            ["https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters#:~:text=Most%20people%20who%20get%20COVID,facility%20by%20telephone%20first.","https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters#:~:text=The%20coronavirus%20disease%20(COVID,19%20hotline%20for%20assistance."],
            ["https://www.bbc.co.uk/news/health-51665497","https://www.bbc.com/news/health-51665497"],
            ["http://teacher.scholastic.com/paperairplane/airplane.htm","https://www.scholastic.com/teachers/articles/teaching-content/what-makes-paper-airplanes-fly/"],
            ["https://www.emedicinehealth.com/anise/vitamins-supplements.htm","https://www.rxlist.com/anise/supplements.htm"],
            ["https://medium.com/@ashukumar27/similarity-functions-in-python-aa6dfe721035","https://dataaspirant.com/five-most-popular-similarity-measures-implementation-in-python/"],
            ["https://www.geeksforgeeks.org/python-word-embedding-using-word2vec/","https://towardsdatascience.com/word2vec-from-scratch-with-numpy-8786ddd49e72"],
            ["https://www.newadvent.org/cathen/03096a.htm", "https://www.livius.org/articles/misc/byzantine-empire/"],
            ["https://www.encyclopedia.com/history/modern-europe/turkish-and-ottoman-history/ottoman-empire", "https://www.jstor.org/stable/j.ctt1b67wfz"],
            ["https://www.amacad.org/publication/ottoman-experience", "https://www.encyclopedia.com/history/modern-europe/turkish-and-ottoman-history/ottoman-empire"],
            ["https://www.socialwatch.org/node/18372", "https://blogs.lse.ac.uk/mec/2019/10/24/lebanons-revolution-makes-its-own-rules/"],
            ["https://www.ancient.eu/Byzantine_Empire/", "https://www.thebritishacademy.ac.uk/blog/what-is-byzantine-studies/"],
            ["https://www.ushistory.org/civ/3e.asp", "https://www.goaheadtours.com/travel-blog/articles/pyramids-of-giza-facts"], 
            ["https://www.cairn.info/revue-napoleonica-la-revue-2013-1-page-88.htm", "https://www.euronews.com/2021/02/13/french-and-russian-soldiers-who-fought-in-napoleon-s-18-12-campaign-are-finally-buried"],
            ["https://www.thebalancesmb.com/simple-ways-make-money-online-2531879", "https://www.lifehack.org/articles/money/5-real-ways-actually-make-money-online.html"],
            ["https://opensource.com/resources/python", "https://www.infoworld.com/article/3204016/what-is-python-powerful-intuitive-programming.html"],
            ["https://www.metmuseum.org/toah/hd/grot/hd_grot.htm", "https://www.amacad.org/publication/ottoman-experience"],
            ["https://courses.lumenlearning.com/waymaker-psychology/chapter/reading-parts-of-the-brain/", "https://www.news-medical.net/health/The-Anatomy-of-the-Human-Brain.aspx"],
            ["https://www.oracle.com/internet-of-things/what-is-iot/","https://www.oracle.com/in/internet-of-things/what-is-iot/"],
            ["https://www.thoughtco.com/anatomy-of-the-stomach-373482", "https://www.nursingtimes.net/clinical-archive/gastroenterology/gastrointestinal-tract-2-the-structure-and-function-of-the-stomach-24-06-2019/"],
            ["https://courses.lumenlearning.com/boundless-worldhistory/chapter/the-ottoman-empire/", "https://www.laits.utexas.edu/cairo/history/ottoman/ottoman.html"],
            ["https://en.wikivoyage.org/wiki/Istanbul","https://wikitravel.org/en/Istanbul"],
            ["https://en.wikivoyage.org/wiki/Turkey","https://wikitravel.org/en/Turkey"],
            ["https://courses.lumenlearning.com/atd-tcc-worldciv2/chapter/ottoman-empire/","https://en.wikipedia.org/wiki/History_of_the_Ottoman_Empire"],
            ["https://en.citizendium.org/wiki/Crusades","https://en.wikipedia.org/wiki/Crusades"],
            ["https://en.wikipedia.org/wiki/Crusades","https://chem.libretexts.org/Courses/Lumen_Learning/Book%3A_Western_Civilization_I_(Lumen)/15%3A_Week_13%3A_The_Crusades_and_The_Late_Middle_Ages/15.2%3A_Reading%3A_The_Crusades"],
            ["https://en.wikipedia.org/wiki/Decline_of_Buddhism_in_the_Indian_subcontinent","https://en.wikipedia.org/wiki/History_of_Buddhism_in_India"],
            ["https://en.wikipedia.org/wiki/Galata","https://www.wikiwand.com/en/Galata"],
            ["https://en.wikipedia.org/wiki/Ottoman_Empire","https://en.wikipedia.org/wiki/History_of_the_Ottoman_Empire"]
        )

    driver = webdriver.Chrome('chromedriver')

    i = 1
    for urls_pair in urls:
        results_file = open("graph_similarity_results.txt", "a")
        print("Pair number", i)

        url1 = urls_pair[0]
        url2 = urls_pair[1]
        results = get_similarities(driver, url1, url2)

        results_file.write("url1: "+ results['url1'] + "\n")
        results_file.write("url2: "+ results['url2'] + "\n")

        results_file.write("website_titles_sim: "+ str(results['website_titles_sim']) + "\n")
        results_file.write("page_titles_sim: "+ str(results['page_titles_sim']) + "\n")
        results_file.write("subtitles_sim: "+ str(results['subtitles_sim']) + "\n")
        results_file.write("urls_sim: "+ str(results['urls_sim']) + "\n")

        results_file.write("cosine_similarity_syntactic_preprocessing: " + str(results['cosine_similarity_syntactic_preprocessing']) + "\n")
        results_file.write("cosine_similarity_semantic_preprocessing: "+ str(results['cosine_similarity_semantic_preprocessing']) + "\n")
        
        results_file.write("veo_sim: "+ str(results['veo_sim']) + "\n")
        
        results_file.write("\n######################################################################\n\n")

        print("Pair number", i, "done")
        print("######################################################################")
        i += 1
        results_file.close()
    
    driver.close()

def f(args, wt_sim, t_sim, st_sim, u_sim, c_sim, g_sim):
    p_w, p_t, p_s, p_u, p_c, p_g = args
    final_sim = p_w*wt_sim + p_t*t_sim + p_s*st_sim + p_u*u_sim + p_c*c_sim + p_g*g_sim
    return final_sim

if __name__ ==  '__main__':
    #main()
    print("Hello")
    