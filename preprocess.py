import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet
from unidecode import unidecode
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize


#######################################################
###### Syntactic String Preprocessing: Lowercase ######
########### no ASCII characters, Punctucation #########
#######################################################

def get_syntactically_preprocessed_sentence(sentence):

    # Convert input sentence to lower case.
    sentence = sentence.lower().replace("/","").replace("\\","").replace('"',"").replace("''","").replace("`","").replace("'s"," is").replace("'m"," am").replace("'ll"," will").replace("'re"," are").replace("n't"," not")

    # Remove non-ascii characters
    sentence = unidecode(sentence)

    # Collecting a list of punctuations form string class
    stopset = list(string.punctuation)
    # (Noise Removal) Remove stop words and punctuations from string.
    # word_tokenize is used to tokenize the input sentence in word tokens.
    sentence = " ".join([i for i in word_tokenize(sentence) if i not in stopset])

    sentence = sentence.replace('"',"").replace("''","").replace("`","").replace("'s"," is").replace("-","").replace(".","")

    return sentence


#######################################################
###### Syntactic List of Sentences Preprocessing ######
#######################################################

def get_syntactically_preprocessed_paragraph(paragraph):
    preprocessed_paragraph = ""
    for sentence in sent_tokenize(paragraph):
        preprocessed_paragraph += get_syntactically_preprocessed_sentence(sentence)
    return preprocessed_paragraph

#######################################################
############ Define POS tags for Lemmatizer ###########
#######################################################

def get_wordnet_pos(word):

    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

#######################################################
###### Semantic String Preprocessing: Lowercase #######
#### no ASCII characters, Punctucation, Stopwords #####
#######################################################

def get_semantically_preprocessed_sentence(sentence):

    # Convert input sentence to lower case.
    sentence = sentence.lower().replace("/","").replace("\\","").replace('"',"").replace("''","").replace("`","").replace("'s"," is").replace("'m"," am").replace("'ll"," will").replace("'re"," are").replace("n't"," not")

    # Remove non-ascii characters
    sentence = unidecode(sentence)

    # Collecting a list of stop words from nltk and punctuation form string class and create single array
    stopset = stopwords.words('english') + list(string.punctuation)
    # - ['no', 'nor', 'not', 'only']
    # (Noise Removal) Remove stop words and punctuations from string.
    # word_tokenize is used to tokenize the input sentence in word tokens.
    sentence = " ".join([i for i in word_tokenize(sentence) if i not in stopset])

    # Lemmatization with WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    sentence = " ".join(lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in word_tokenize(sentence))
    sentence = sentence.replace('"',"").replace("''","").replace("`","").replace("'s"," is").replace("-","").replace(".","")


    # Lemmatization with Spacy Lemmatizer
    # nlp = spacy.load('en_core_web_sm')
    # Create a Doc object
    # doc = nlp(u''+sentence)
    # Create list of tokens from given string
    # tokens = []
    # for token in doc:
    #     tokens.append(token)    
    # sentence = " ".join([token.lemma_ for token in doc])

    return sentence

#######################################################
###### Semantic List of Sentences Preprocessing #######
#######################################################

# def get_semantically_preprocessed_list_of_strings(list_of_sentences):
#     # input: list of paragraphs
#     # output: list of all preprocessed sentences, item_list = preprocessed sentence
#     new_list_of_sentences = []
#     for paragraph in list_of_sentences:
#         #sentences = sent_tokenize(paragraph)
#         sentences = paragraph.split('.')
#         for sentence in sentences:
#             new_list_of_sentences.append(get_semantically_preprocessed_sentence(sentence))
#     return new_list_of_sentences

def get_semantically_preprocessed_paragraph(paragraph):
    preprocessed_paragraph_list_of_sentences = []
    for sentence in sent_tokenize(paragraph):
        preprocessed_sentence = get_semantically_preprocessed_sentence(sentence)
        preprocessed_paragraph_list_of_sentences.append(preprocessed_sentence)
    return preprocessed_paragraph_list_of_sentences

# def get_semantically_preprocessed_paragraph_return_as_list(paragraph):
#     # input: one paragraph
#     # output: list of all preprocessed sentences in the paragraph, item_list = preprocessed sentence
#     new_list_of_sentences = []
#     sentences = sent_tokenize(paragraph)
#     for sentence in sentences:
#             new_list_of_sentences.append(get_semantically_preprocessed_string(sentence))
#     return new_list_of_sentences


def preprocess_sentence_for_graph(sentence):

    from nltk.stem.wordnet import WordNetLemmatizer # to download corpora: python -m    nltk.downloader all
    lemmatizer = WordNetLemmatizer() # create a lemmatizer object

    sentence = sentence.lower().replace("/","").replace("\\","").replace('"',"").replace("''","").replace("`","").replace("'s"," is").replace("'m"," am").replace("'ll"," will").replace("'re"," are").replace("n't"," not")

    sentence = unidecode(sentence)

    stopset = stopwords.words('english') + list(string.punctuation)
    sentence = " ".join([i for i in word_tokenize(sentence) if i not in stopset])

    sentence = " ".join(lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in word_tokenize(sentence))
    sentence = sentence.replace('"',"").replace("''","").replace("`","").replace("'s"," is").replace("-","").replace(".","")

    return sentence