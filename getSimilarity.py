import math
import re
from collections import Counter
from scipy import spatial

WORD = re.compile(r"\w+")

#######################################################
#################### Text to Vector ###################
#######################################################

def get_vector_from_text(text):
    words = WORD.findall(text)
    return Counter(words)

#######################################################
########### List of Texts to List of Vectors ##########
#######################################################

def get_list_of_vectors_from_list_of_texts(list_of_texts):
    list_of_vectors = []
    for text in list_of_texts:
         list_of_vectors.append(get_vector_from_text(text))
    return list_of_vectors

def cosine(v1, v2):
    from sklearn.metrics.pairwise import cosine_similarity
    return cosine_similarity(v1, v2)

#######################################################
################## Cosine of 2 Vectors ################
#######################################################

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

#######################################################
######### Average Cosine of 2 lists of Vectors ########
#######################################################

def get_average_cosine_of_2_list_of_vectors(list_of_vectors1, list_of_vectors2):
    sum_cosines = 0
    for vector1 in list_of_vectors1:
        max_cosine = 0
        for vector2 in list_of_vectors2:
            cos = get_cosine_of_2_vectors(vector1, vector2)
            if cos > max_cosine:
                max_cosine = cos        
        sum_cosines = sum_cosines + max_cosine
    avg_cosine = sum_cosines / len(list_of_vectors1)
    return avg_cosine

#######################################################
################# Cosine of 2 Sentences ###############
#######################################################

def get_cosine_of_2_sentences(sentence1, sentence2):
    return get_cosine_of_2_vectors(get_vector_from_text(sentence1),get_vector_from_text(sentence2))

#######################################################
######## Average Cosine of 2 lists of Sentences #######
#######################################################

def get_average_cosine_of_2_lists_of_sentences(list_of_sentences_1, list_of_sentences_2):
    return get_average_cosine_of_2_list_of_vectors(get_list_of_vectors_from_list_of_texts(list_of_sentences_1),get_list_of_vectors_from_list_of_texts(list_of_sentences_2))

#######################################################
################ Jaccard of 2 Sentences ###############
#######################################################

def get_jaccard_of_two_sentences(sentence1,sentence2):   
    set_of_words_of_sentence1 = set(sentence1.split(' '))
    set_of_words_of_sentence2 = set(sentence2.split(' '))
    intersection_cardinality = len(set.intersection(*[set_of_words_of_sentence1, set_of_words_of_sentence2]))
    union_cardinality = len(set.union(*[set_of_words_of_sentence1, set_of_words_of_sentence2]))
    return intersection_cardinality/float(union_cardinality)

#######################################################
####### Average Jaccard of 2 lists of Sentences #######
#######################################################

def get_average_jaccard_of_two_lists_of_sentences(list_of_sentences1,list_of_sentences2):   
    sum_jaccards = 0
    for sentence1 in list_of_sentences1:
        set_sentence1 = set(sentence1.split(' '))
        max_jaccard = 0
        for sentence2 in list_of_sentences2:
            set_sentence2 = set(sentence2.split(' '))
            intersection_cardinality = len(set.intersection(*[set_sentence1, set_sentence2]))
            union_cardinality = len(set.union(*[set_sentence1, set_sentence2]))
            jaccard = intersection_cardinality/float(union_cardinality)
            if jaccard > max_jaccard:
                max_jaccard = jaccard  
        sum_jaccards = sum_jaccards + max_jaccard
    avg_jaccard = sum_jaccards / len(list_of_sentences1)
    return avg_jaccard