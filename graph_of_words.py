# https://gitlab.com/vi.le/graphofwords/-/tree/master

from itertools import tee
from nltk.tokenize import word_tokenize
import networkx as nx
import matplotlib.pyplot as plt
import multiprocessing as mp
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

    def __init__(self, window_size=10):

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
        seen_words = []

        words = word_tokenize(sentence)
        word_windows = self.__window(words)

        for idx_word_window, word_window in enumerate(word_windows, start=0):
            for idx, outer_word in enumerate(word_window):
                for idx_inner, inner_word in enumerate(word_window[idx + 1 :], start=2):
                    word_id = "{0}_{1}_{2}".format(
                        outer_word, inner_word, (idx_inner + idx_word_window + idx)
                    )
                    if word_id not in seen_words:
                        edges.append(
                            (outer_word, inner_word, self.window_size - idx_inner + 2)
                        )
                        seen_words.append(word_id)
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

        pool = mp.Pool(processes=workers)
        edges = pool.map(self.analyse_sentence, sentences)
        pool.close()
        pool.join()
        edges = [edge for sublist in edges for edge in sublist]
        
        weighted_edges = {}
        initial_weights = []
        final_edges = []
        node_labels = {}
        edge_labels = {}

        for edge in edges:
            edge_name = edge[0]+'_'+edge[1]
            edge_value = edge[2]
            initial_weights.append((edge_name,edge_value))
        
        for edge in initial_weights:
            if edge[0] in weighted_edges.keys():
                weighted_edges[edge[0]] = weighted_edges[edge[0]] + edge[1]
            else:
                weighted_edges[edge[0]] = edge[1]

        for node1_node2, weight in weighted_edges.items():
            nodes = node1_node2.split("_")
            node1 = nodes[0]
            node2 = nodes[1]
            if node1 not in node_labels:
                node_labels[node1] = node1
            if node2 not in node_labels:
                node_labels[node2] = node2
            edge = (node1, node2, weight)

            edge_label = (node1, node2)
            if edge_label not in edge_labels:
                edge_labels[edge_label] = edge_label
            final_edges.append(edge)


        self.graph.add_weighted_edges_from(final_edges)


def show_graph(g: GraphOfWords):
    graph = g.graph
    pos = nx.spring_layout(graph, k=10)  # For better example looking
    nx.draw(graph, pos, with_labels=True)
    nx.draw_networkx_labels(graph, pos)
    plt.show()

def show_graph_with_edge_labels(g: GraphOfWords):
    G = g.graph
    pos = nx.spring_layout(G, k=10)  # For better example looking
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_labels(G, pos)
    #labels = {(n1,n2):n1+'-'+n2+':'+str(weight) for n1, n2, weight in G.edges(data="weight")}
    labels = {(n1,n2):str(weight) for n1, n2, weight in G.edges(data="weight")}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=.66)
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