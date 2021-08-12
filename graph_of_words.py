# https://gitlab.com/vi.le/graphofwords/-/tree/master

from itertools import tee
from nltk.tokenize import word_tokenize
import networkx as nx
import matplotlib.pyplot as plt
import typing
import numpy as np

class GraphOfWords:

    def __init__(self, sentences, window_size=2):

        self.window_size = window_size
        self.graph = nx.DiGraph()
        self.build_graph(sentences)
    
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
    
    def analyse_sentence(self, sentence: str) -> list:
        edges = []
        node_labels = {}
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
    
    def build_graph(self, sentences):
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

    if vertex_edge_overlap_value == 0:
        return 0, 0
        
    vertex_edge_sim = np.abs(1-vertex_edge_overlap_value)/vertex_edge_overlap_value
    if vertex_edge_sim > 1:
        vertex_edge_sim = 1 / vertex_edge_sim

    return vertex_edge_overlap_value, vertex_edge_sim

def graph_similarity(g1,g2):
    
    E1,E2 = [set(G.edges()) for G in [g1,g2]]

    E_intersection = len(E1&E2)
    E_union = len(E1|E2)

    if E_union == 0 or E_intersection == 0:
        return 0

    sim = E_intersection / E_union
    return sim


def graphs_jaccard_similarity(g1, g2):
    # graphs not necessary same number of vertices !!

    # Getting sets of vertices & edges
    V1,V2 = [set(G.nodes()) for G in [g1,g2]]
    E1,E2 = [set(G.edges()) for G in [g1,g2]]

    len_nodes_union = len(V1|V2)
    len_edges_union = len(E1|E2)
    len_edges_intersection = len(E1&E2)
    len_nodes_intersection = len(V1&V2)

    denominator = len_nodes_union + len_edges_union
    if denominator == 0:
        return 0

    # Jaccard Similarity = (sum of intersections) / (sum of unions)
    jaccard_similarity = (len_edges_intersection + len_nodes_intersection) / denominator
    return jaccard_similarity
 