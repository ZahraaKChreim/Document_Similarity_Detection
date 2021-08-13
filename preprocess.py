import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet
from unidecode import unidecode
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize

import spacy
nlp = spacy.load('fr_core_news_md')
french_stopwords = nltk.corpus.stopwords.words('french')

from snowballstemmer import stemmer
ar_stemmer = stemmer("arabic")
from qalsadi import lemmatizer
ar_lemmer = lemmatizer.Lemmatizer()

"""
    ENGLISH
"""

def get_syntactically_preprocessed_sentence(sentence):

    # Convert input sentence to lower case.
    sentence = sentence.lower().replace("/","").replace("\\","").replace('"',"").replace("''","").replace("`","").replace("'s"," is").replace("'m"," am").replace("'ll"," will").replace("'re"," are").replace("n't"," not")

    # Remove non-ascii characters
    sentence = unidecode(sentence)

    # Remove all Digits
    sentence = ''.join([i for i in sentence if not i.isdigit()])

    # Collecting a list of punctuations form string class
    stopset = list(string.punctuation)
    # (Noise Removal) Remove stop words and punctuations from string.
    # word_tokenize is used to tokenize the input sentence in word tokens.
    sentence = " ".join([i for i in word_tokenize(sentence) if i not in stopset])

    sentence = sentence.replace('"',"").replace("''","").replace("`","").replace("'s"," is").replace("-","").replace(".","").replace("'","")

    return sentence


def get_syntactically_preprocessed_paragraph(paragraph):
    preprocessed_paragraph = ""
    for sentence in sent_tokenize(paragraph):
        preprocessed_paragraph = preprocessed_paragraph + " " + get_syntactically_preprocessed_sentence(sentence)
    return preprocessed_paragraph


def get_wordnet_pos(word):

    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def get_semantically_preprocessed_sentence(sentence):

    # Convert input sentence to lower case.
    sentence = sentence.lower().replace("/","").replace("\\","").replace('"',"").replace("''","").replace("`","")

    # Remove non-ascii characters
    sentence = unidecode(sentence)

    # Remove all Digits
    sentence = ''.join([i for i in sentence if not i.isdigit()])

    # Collecting a list of stop words from nltk and punctuation form string class and create single array
    stopset = stopwords.words('english') + list(string.punctuation)
    #stopset = list(string.punctuation)
    # - ['no', 'nor', 'not', 'only']
    # (Noise Removal) Remove stop words and punctuations from string.
    # word_tokenize is used to tokenize the input sentence in word tokens.
    sentence = " ".join([i for i in word_tokenize(sentence) if i not in stopset])

    # Lemmatization with WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    sentence = " ".join(lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in word_tokenize(sentence))
    sentence = sentence.replace('"',"").replace("''","").replace("`","").replace("-","").replace(".","").replace("'","")

    return sentence


def get_semantically_preprocessed_paragraph(paragraph):
    preprocessed_paragraph = []
    paragraph = paragraph.replace("'s"," is").replace("'m"," am").replace("'ll"," will").replace("'re"," are").replace("n't"," not")
    paragraph = paragraph.replace("\n", "").replace("   ", "").replace("  ", "")

    punctuations = list(string.punctuation)
    punctuations.remove('.')
    for punctuation in punctuations:
        paragraph.replace(punctuation, "")
    
    for sentence in sent_tokenize(paragraph):
        preprocessed_sentence = get_semantically_preprocessed_sentence(sentence)
        preprocessed_paragraph.append(preprocessed_sentence)
    
    return preprocessed_paragraph

"""
    FRENCH
"""

def get_semantically_preprocessed_french_paragraph(paragraph):
    preprocessed_paragraph = []
    paragraph = paragraph.replace("\n", "").replace("   ", "").replace("  ", "")
    punctuations = list(string.punctuation)
    punctuations.remove('.')
    for punctuation in punctuations:
        paragraph.replace(punctuation, "")

    for sentence in sent_tokenize(paragraph):
        preprocessed_sentence = get_semantically_preprocessed_french_sentence(sentence)
        preprocessed_paragraph.append(preprocessed_sentence)
    
    return preprocessed_paragraph

def get_semantically_preprocessed_french_sentence(sentence):
    # https://newbedev.com/lemmatize-french-text

    sentence = sentence.lower().replace("/","").replace("\\","").replace('"',"").replace("''","").replace("`","").replace("-", " ")
    sentence = unidecode(sentence)
    sentence = ''.join([i for i in sentence if not i.isdigit()])

    stopset = french_stopwords + list(string.punctuation)
    sentence = " ".join([i for i in word_tokenize(sentence) if i not in stopset])

    sentence = nlp(u"" + sentence)

    lemmatized_sentence = " ".join(word.lemma_ for word in sentence)

    sentence = lemmatized_sentence.replace('"',"").replace("''","").replace("`","").replace("-","").replace(".","").replace("'","")
    
    return sentence

def get_syntactically_preprocessed_french_paragraph(paragraph):
    paragraph = paragraph.replace("-", " ").replace("\n", " ").replace("   ", " ").replace("  ", " ")
    preprocessed_paragraph = ""
    for sentence in sent_tokenize(paragraph):
        preprocessed_paragraph = preprocessed_paragraph + " " + get_syntactically_preprocessed_french_sentence(sentence)
    return preprocessed_paragraph

def get_syntactically_preprocessed_french_sentence(sentence):

    sentence = sentence.lower().replace("/","").replace("\\","").replace('"',"").replace("''","").replace("`","")
    sentence = unidecode(sentence)
    sentence = ''.join([i for i in sentence if not i.isdigit()])

    stopset = list(string.punctuation)
    sentence = " ".join([i for i in word_tokenize(sentence) if i not in stopset])

    sentence = sentence.replace('"',"").replace("''","").replace("`","").replace("-","").replace(".","").replace("'","")

    return sentence

"""
    ARABIC
"""

def get_semantically_preprocessed_arabic_paragraph(paragraph):
    preprocessed_paragraph = []
    paragraph = paragraph.replace("\n", "").replace("   ", "").replace("  ", "")
    punctuations = list(string.punctuation)
    punctuations.remove('.')
    for punctuation in punctuations:
        paragraph.replace(punctuation, "")

    for sentence in sent_tokenize(paragraph):
        preprocessed_sentence = get_semantically_preprocessed_arabic_sentence(u""+sentence)
        preprocessed_paragraph.append(preprocessed_sentence)
    
    return preprocessed_paragraph

def get_semantically_preprocessed_arabic_sentence(sentence):

    sentence = sentence.replace("/","").replace("\\","").replace('"',"").replace("''","").replace("`","").replace("-", " ")
    
    sentence = ''.join([i for i in sentence if not i.isdigit()])

    stopset = list(string.punctuation)
    sentence = " ".join([i for i in word_tokenize(sentence) if i not in stopset])

    words = []
    for word in word_tokenize(sentence):
        lemma = ar_lemmer.lemmatize(word, get_wordnet_pos(word))
        if lemma[1] != "stopword":
            lem = ar_stemmer.stemWord(lemma[0])
            words.append(lem)
    sentence = " ".join(word for word in words)

    sentence = sentence.replace('"',"").replace("''","").replace("`","").replace("-","").replace(".","").replace("'","")
    
    return sentence

def get_syntactically_preprocessed_arabic_paragraph(paragraph):
    paragraph = paragraph.replace("-", " ").replace("\n", " ").replace("   ", " ").replace("  ", " ")
    preprocessed_paragraph = ""
    for sentence in sent_tokenize(paragraph):
        preprocessed_paragraph = preprocessed_paragraph + " " + get_syntactically_preprocessed_arabic_sentence(sentence)
    return preprocessed_paragraph

def get_syntactically_preprocessed_arabic_sentence(sentence):

    sentence = sentence.replace("/","").replace("\\","").replace('"',"").replace("''","").replace("`","")
    sentence = ''.join([i for i in sentence if not i.isdigit()])

    stopset = list(string.punctuation)
    sentence = " ".join([i for i in word_tokenize(sentence) if i not in stopset])

    sentence = sentence.replace('"',"").replace("''","").replace("`","").replace("-","").replace(".","").replace("'","")

    return sentence


    
