import math
import re
from collections import Counter
from graph_of_words import GraphOfWords
import grakel
from grakel.graph_kernels import GraphletSampling

# Weights for the Final Similarity calculation between two websites
p_w = 0.025
p_t = 0.075
p_s = 0.075
p_u = 0.025
p_c = 0.4
p_g = 0.4

# def weights():
#     return

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

def get_similarity_record1_record2(record1, record2):

    url1 = record1.get("url")
    url2 = record2.get("url")
    
    website_titles_sim = get_cosine_of_2_sentences(record1.get("website_title"), record2.get("website_title"))
    page_titles_sim = get_cosine_of_2_sentences(record1.get("page_title"), record2.get("page_title"))

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
    urls_sim = get_jaccard_of_two_lists_of_sentences(list_of_urls1, list_of_urls2)

    syntactically_preprocessed_body_text1 = record1.get("synt_proc_body")
    syntactically_preprocessed_body_text2 = record2.get("synt_proc_body")

    semantically_preprocessed_paragraph1 = record1.get("sem_proc_body")
    semantically_preprocessed_paragraph2 = record2.get("sem_proc_body")
    semantically_preprocessed_paragraph_as_list_of_sentences1 = semantically_preprocessed_paragraph1.split("___")
    semantically_preprocessed_paragraph_as_list_of_sentences2 = semantically_preprocessed_paragraph2.split("___")

    cosine_similarity = get_cosine_of_2_sentences(syntactically_preprocessed_body_text1, syntactically_preprocessed_body_text2)

    graph1 = GraphOfWords(semantically_preprocessed_paragraph_as_list_of_sentences1)
    g1 = graph1.graph
    graph2 = GraphOfWords(semantically_preprocessed_paragraph_as_list_of_sentences2)
    g2 = graph2.graph

    if len(g1.edges)==0 or len(g2.edges)==0:
        graphlet_sim = 0
    
    else:

        """graph Kernel graph_from_networkx"""
        graphs = grakel.graph_from_networkx([g1, g2])
        
        try:
            graphlet_kernel = GraphletSampling(normalize=True, sampling={"n_samples":300})
            graphlet_value = graphlet_kernel.fit_transform(graphs)
            graphlet_sim = graphlet_value[0][1]
        except Exception as e:
            print('Graphlet Sampling Kernel Exception: '+ str(e))
            print(url1)
            print(url2)
            graphlet_sim = 0
    
    final_similarity_score = p_w*website_titles_sim + p_t*page_titles_sim + p_s*subtitles_sim + p_u*urls_sim + p_c*cosine_similarity + p_g*graphlet_sim
    return final_similarity_score
