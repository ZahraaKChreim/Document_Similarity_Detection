# https://gitlab.com/vi.le/graphofwords/-/tree/master

from itertools import tee
from nltk.tokenize import word_tokenize
import networkx as nx
import matplotlib.pyplot as plt
import typing
import numpy as np

class GraphOfWords:
    """
    Represent a graph of words object

    Args:
        window_size (int, optional): The size of window
        language (str, optional): The language of the text
    """

    #######################################################
    ######################## init  ########################
    #######################################################

    def __init__(self, window_size=4):

        self.window_size = window_size
        self.graph = nx.DiGraph()

    #######################################################
    ####################### window  #######################
    #######################################################
    
    def __window(self, iterable: typing.Iterable) -> typing.Iterable:
        """
        Create a sliding window

        Args:
            iterable (Iterbale): Predicted values

        Returns:
            typing.Iterable: The windows
        """

        iters = tee(iterable, self.window_size)
        for i in range(1, self.window_size):
            for each in iters[i:]:
                next(each, None)
        return list(zip(*iters))

    #######################################################
    ################## Analyse Sentence  ##################
    #######################################################
    
    def analyse_sentence(self, sentence: str) -> list:
        
        """
        Treat a single sentence with a sliding window connecting words in a
        graph Return a list of edges insteads, then the graph will be created
        from this graph

        Args:
            sentence (str): The sentence to process

        Returns:
            list: The graph edges.

        """
        edges = []

        words = word_tokenize(sentence)
        word_windows = self.__window(words)

        for idx_word_window, word_window in enumerate(word_windows, start=0):
            for idx, outer_word in enumerate(word_window):
                for idx_inner, inner_word in enumerate(word_window[idx + 1 :], start=2):
                    edge = (outer_word, inner_word)
                    if edge not in edges:
                        edges.append(
                            edge
                        )
        return edges

    #######################################################
    #################### Build Graph  #####################
    #######################################################
    
    def build_graph(self, text: str, workers: int = 1):
        
        """
        Build the graph itself

        Args:
            text (str): list of sentences
            workers (int, optional): Number of cores to use
        """
        #print("Build Graph...")

        sentences = text

        edges = []
        for sentence in sentences:
            edges += self.analyse_sentence(sentence)
        
        self.graph.add_edges_from(edges)

def show_graph(g: GraphOfWords):
    graph = g.graph
    pos = nx.spring_layout(graph, k=10)  # For better example looking
    nx.draw(graph, pos, with_labels=True)
    nx.draw_networkx_labels(graph, pos)
    plt.show()


def vertex_edge_overlap(g1,g2):
    # Code from: https://github.com/peterewills/NetComp/blob/master/netcomp/distance/exact.py
    # graphs not necessary same number of vertices !!
    
    # Getting sets of vertices & edges
    V1,V2 = [set(G.nodes()) for G in [g1,g2]]
    E1,E2 = [set(G.edges()) for G in [g1,g2]]

    V_overlap = len(V1|V2)
    E_overlap = len(E1|E2)

    denominator = len(V1)+len(V2)+len(E1)+len(E2)
    if denominator == 0:
        vertex_edge_overlap_value = 0
    else:
        vertex_edge_overlap_value = (V_overlap + E_overlap) / denominator

    # Similarity Value from Vertex_Edge Overlap Value
    if vertex_edge_overlap_value == 0:
        return 0, 0
        
    vertex_edge_sim = np.abs(1-vertex_edge_overlap_value)/vertex_edge_overlap_value
    if vertex_edge_sim > 1:
        vertex_edge_sim = 1 / vertex_edge_sim

    return vertex_edge_overlap_value, vertex_edge_sim