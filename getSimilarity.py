import math
import re
from collections import Counter
import database_handler
import preprocess
from graph_of_words import GraphOfWords, show_graph, vertex_edge_overlap, graph_similarity
import networkx as nx

# Weights for the Final Similarity calculation between two websites
p_w = 0.04
p_t = 0.1
p_s = 0.05
p_u = 0.01
p_c = 0.8
p_g = 0.0

WORD = re.compile(r"\w+")

def get_vector_from_text(text):
    words = WORD.findall(text)
    return Counter(words)

def get_list_of_vectors_from_list_of_texts(list_of_texts):
    list_of_vectors = []
    for text in list_of_texts:
         list_of_vectors.append(get_vector_from_text(text))
    return list_of_vectors

def cosine(v1, v2):
    from sklearn.metrics.pairwise import cosine_similarity
    return cosine_similarity(v1, v2)

def get_cosine_of_2_vectors(vector1, vector2):
    intersection = set(vector1.keys()) & set(vector2.keys())
    numerator = sum([vector1[x] * vector2[x] for x in intersection])

    sum1 = sum([vector1[x] ** 2 for x in list(vector1.keys())])
    sum2 = sum([vector2[x] ** 2 for x in list(vector2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def get_cosine_of_2_sentences(sentence1, sentence2):
    return get_cosine_of_2_vectors(get_vector_from_text(sentence1),get_vector_from_text(sentence2))


def get_jaccard_of_two_sentences(sentence1,sentence2):   
    set_of_words_of_sentence1 = set(sentence1.split(' '))
    set_of_words_of_sentence2 = set(sentence2.split(' '))
    intersection_cardinality = len(set.intersection(*[set_of_words_of_sentence1, set_of_words_of_sentence2]))
    union_cardinality = len(set.union(*[set_of_words_of_sentence1, set_of_words_of_sentence2]))
    if union_cardinality == 0:
        return 0
    return intersection_cardinality/float(union_cardinality)

def get_jaccard_of_two_lists_of_sentences(list_of_sentences1,list_of_sentences2):
    
    intersection_cardinality = len(set.intersection(set(list_of_sentences1), set(list_of_sentences2)))
    union_cardinality = len(set.union(set(list_of_sentences1), set(list_of_sentences2)))
    if union_cardinality == 0:
        return 0
    jaccard = intersection_cardinality/float(union_cardinality)
    return jaccard

# def get_similarity_url1_url2(url1, url2):

#     db = database_handler.databaseHandler()
#     print("MySQL connection is opened")

#     url1_results = db.select_from_db_by_url(url1)
#     url2_results = db.select_from_db_by_url(url2)

#     if db.con.is_connected():
#         db.con.close()
#         print("MySQL connection is closed")

#     website_titles_sim = get_cosine_of_2_sentences(url1_results.get("website_title"), url2_results.get("website_title"))
#     page_titles_sim = get_cosine_of_2_sentences(url1_results.get("page_title"), url2_results.get("page_title"))

#     subtitles1 = url1_results.get("subtitles")
#     subtitles2 = url2_results.get("subtitles")
#     urls1 = url1_results.get("urls")
#     urls2 = url2_results.get("urls")

#     if subtitles1 == '':
#         list_of_subtitles1 = []
#     else:
#         list_of_subtitles1 = subtitles1.split("___")
#     if subtitles2 == '':
#         list_of_subtitles2 = []
#     else:
#         list_of_subtitles2 = subtitles2.split("___")

#     if urls1 == '':
#         list_of_subtitles1 = []
#     else:
#         list_of_urls1 = urls1.split("___")
#     if urls2 == '':
#         list_of_subtitles2 = []
#     else:
#         list_of_urls2 = urls2.split("___")

#     subtitles_sim = get_jaccard_of_two_lists_of_sentences(list_of_subtitles1, list_of_subtitles2)
#     urls_sim = get_jaccard_of_two_lists_of_sentences(list_of_urls1, list_of_urls2)

#     syntactically_preprocessed_body_text1 = url1_results.get("synt_proc_body")
#     syntactically_preprocessed_body_text2 = url2_results.get("synt_proc_body")
#     semantically_preprocessed_paragraph1 = url1_results.get("sem_proc_body")
#     semantically_preprocessed_paragraph2 = url2_results.get("sem_proc_body")

#     if semantically_preprocessed_paragraph1 == '':
#         semantically_preprocessed_paragraph_as_list_of_sentences1 = []
#     else:
#         semantically_preprocessed_paragraph_as_list_of_sentences1 = semantically_preprocessed_paragraph1.split("___")

#     if semantically_preprocessed_paragraph2 == '':
#         semantically_preprocessed_paragraph_as_list_of_sentences2 = []
#     else:
#         semantically_preprocessed_paragraph_as_list_of_sentences2 = semantically_preprocessed_paragraph2.split("___")

#     cosine_similarity = get_cosine_of_2_sentences(syntactically_preprocessed_body_text1, syntactically_preprocessed_body_text2)

#     # Graph Representation
#     graph1 = GraphOfWords(window_size=5)
#     graph1.build_graph(semantically_preprocessed_paragraph_as_list_of_sentences1, workers=4)
#     g1 = graph1.graph

#     graph2 = GraphOfWords(window_size=5)
#     graph2.build_graph(semantically_preprocessed_paragraph_as_list_of_sentences2, workers=4)
#     g2 = graph2.graph  

#     veo_val, veo_sim = vertex_edge_overlap(g1, g2)

#     final_similarity_score = p_w*website_titles_sim + p_t*page_titles_sim + p_s*subtitles_sim + p_u*urls_sim + p_c*cosine_similarity + p_g*veo_sim
#     return final_similarity_score

def get_similarity_record1_record2(record1, record2):

    # url1 = record1.get("url")
    # url2 = record2.get("url")
    # print(url1)
    # print(url2)
    # print("-----------------------------")
    
    website_titles_sim = get_cosine_of_2_sentences(record1.get("website_title"), record2.get("website_title"))
    # print("Website Titles:", record1.get("website_title"), record2.get("website_title"))
    # print("website_titles_sim:", website_titles_sim, '\n--------------------------------------')

    page_titles_sim = get_cosine_of_2_sentences(record1.get("page_title"), record2.get("page_title"))
    # print("Page Titles:", record1.get("page_title"), record2.get("page_title"))
    # print("page_titles_sim:", page_titles_sim, '\n--------------------------------------')

    subtitles1 = record1.get("subtitles")
    subtitles2 = record2.get("subtitles")
    urls1 = record1.get("urls")
    urls2 = record2.get("urls")

    if subtitles1 == '':
        list_of_subtitles1 = []
    else:
        list_of_subtitles1 = subtitles1.split("___")
    if subtitles2 == '':
        list_of_subtitles2 = []
    else:
        list_of_subtitles2 = subtitles2.split("___")

    if urls1 == '':
        list_of_urls1 = []
    else:
        list_of_urls1 = urls1.split("___")
    if urls2 == '':
        list_of_urls2 = []
    else:
        list_of_urls2 = urls2.split("___")

    subtitles_sim = get_jaccard_of_two_lists_of_sentences(list_of_subtitles1, list_of_subtitles2)
    # print("SubTitles:", list_of_subtitles1, "\n", list_of_subtitles2)
    # print("subtitles_sim:", subtitles_sim, '\n--------------------------------------')

    urls_sim = get_jaccard_of_two_lists_of_sentences(list_of_urls1, list_of_urls2)
    # print("URLs:", list_of_urls1, "\n", list_of_urls2)
    # print("urls_sim:", urls_sim, '\n--------------------------------------')

    syntactically_preprocessed_body_text1 = record1.get("synt_proc_body")
    syntactically_preprocessed_body_text2 = record2.get("synt_proc_body")

    semantically_preprocessed_paragraph1 = record1.get("sem_proc_body")
    semantically_preprocessed_paragraph2 = record2.get("sem_proc_body")

    if semantically_preprocessed_paragraph1 == '':
        semantically_preprocessed_paragraph_as_list_of_sentences1 = []
    else:
        semantically_preprocessed_paragraph_as_list_of_sentences1 = semantically_preprocessed_paragraph1.split("___")

    if semantically_preprocessed_paragraph2 == '':
        semantically_preprocessed_paragraph_as_list_of_sentences2 = []
    else:
        semantically_preprocessed_paragraph_as_list_of_sentences2 = semantically_preprocessed_paragraph2.split("___")

    cosine_similarity = get_cosine_of_2_sentences(syntactically_preprocessed_body_text1, syntactically_preprocessed_body_text2)
    # print("Cosine:", syntactically_preprocessed_body_text1, "\n", syntactically_preprocessed_body_text2)
    # print("cosine_similarity:", cosine_similarity, '\n--------------------------------------')

    sem_body1 = "".join(sen for sen in semantically_preprocessed_paragraph_as_list_of_sentences1)
    sem_body2 = "".join(sen for sen in semantically_preprocessed_paragraph_as_list_of_sentences2)
    graph_cosine_similarity = get_cosine_of_2_sentences(sem_body1, sem_body2)
    #print("graph_cosine_similarity:", graph_cosine_similarity)

    # Graph Representation
    graph1 = GraphOfWords(window_size=4)
    graph1.build_graph(semantically_preprocessed_paragraph_as_list_of_sentences1)
    g1 = graph1.graph
    #edges1 = g1.edges()
    #print(g1.nodes(),"\n######################")
    #print(g1.edges(),"\n######################")
    #show_graph(graph1)

    graph2 = GraphOfWords(window_size=4)
    graph2.build_graph(semantically_preprocessed_paragraph_as_list_of_sentences2)
    g2 = graph2.graph  
    #edges2 = g2.edges()
    #print(g2.nodes(),"\n######################")
    #print(g2.edges())
    #show_graph(graph2)

    #veo_val, veo_sim = vertex_edge_overlap(g1, g2)
    #sim = graph_similarity(g1, g2)
    #graph_sim = get_jaccard_of_two_lists_of_sentences(edges1, edges2)
    #print("Graph:", semantically_preprocessed_paragraph_as_list_of_sentences1, "\n", semantically_preprocessed_paragraph_as_list_of_sentences2)
    #print("veo_sim:", veo_sim)


    #final_similarity_score = p_w*website_titles_sim + p_t*page_titles_sim + p_s*subtitles_sim + p_u*urls_sim + p_c*cosine_similarity + p_g*veo_sim

    final_similarity_score = p_w*website_titles_sim + p_t*page_titles_sim + p_s*subtitles_sim + p_u*urls_sim + p_c*cosine_similarity
    
    return final_similarity_score