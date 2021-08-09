from nltk.tokenize import word_tokenize, sent_tokenize
from preprocess import preprocess_sentence_for_graph

class Graph_from_Text:

    def __init__(self, text:str):

        self.text = text
        self.graph = self.create_graph()

    def create_graph(self):
        edges = []
        for sentence in sent_tokenize(self.text):
            sentence = preprocess_sentence_for_graph(sentence)
            words = word_tokenize(sentence)
            for i in range(len(words)-1):
                edges.append((words[i],words[i+1]))
        return edges

if __name__ ==  '__main__':
    
    from time import time
    str = "hello guys, how are you doing today? I'm so good today, what about you. are you coming tomorrow?"

    t = time()
    edges = []
    for sentence in sent_tokenize(str):
        sentence = preprocess_sentence_for_graph(sentence)
        words = word_tokenize(sentence)
        for i in range(len(words)-1):
            edges.append((words[i],words[i+1]))

    x = time() - t
    print(x)
    print(edges)