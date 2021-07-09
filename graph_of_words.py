# https://gitlab.com/vi.le/graphofwords/-/tree/master

from itertools import tee
from nltk.tokenize import sent_tokenize, word_tokenize
import networkx as nx
import matplotlib.pyplot as plt
import multiprocessing as mp
import typing
from functools import reduce


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
        #self.graph.add_edges_from(edges)
        #print("Build Graph Done...")

        #print("set_node_attributes:")
        nx.set_node_attributes(self.graph, node_labels, 'node_labels')

        #print("set_edge_attributes:")
        nx.set_edge_attributes(self.graph, edge_labels, 'edge_labels')

        # return weighted_edges, final_edges, node_labels
        # return node_labels, edge_labels
        # return node_labels


def getMCS(graph_of_words1: GraphOfWords, graph_of_words2: GraphOfWords):
    g1 = graph_of_words1.graph
    g2 = graph_of_words2.graph

    matching_graph=nx.Graph()

    if g1.number_of_nodes() > g2.number_of_nodes():
        for n1,n2 in g1.edges():
            if g2.has_edge(n1, n2):
                weight1 = g1.get_edge_data(n1, n2, default=0)['weight']
                weight2 = g2.get_edge_data(n1, n2, default=0)['weight']
                # match_weight = num_sim(weight1, weight2)
                match_weight = (weight1 + weight2)/2
                matching_graph.add_edge(n1, n2, weight=match_weight)
    else:
        for n1,n2 in g2.edges():
            if g1.has_edge(n1, n2):
                weight1 = g1.get_edge_data(n1, n2, default=0)['weight']
                weight2 = g2.get_edge_data(n1, n2, default=0)['weight']
                # match_weight = num_sim(weight1, weight2)
                match_weight = (weight1 + weight2)/2
                matching_graph.add_edge(n1, n2, weight=match_weight)

    all_common_subgraphs = nx.connected_components(matching_graph)

    # all_common_subgraphs_copy = nx.connected_components(matching_graph)
    # count = 0
    # for common_subgraph in all_common_subgraphs_copy:
    #     count = count + 1
    #     print('subgraph')
    #     subgraph = nx.induced_subgraph(matching_graph, common_subgraph)
    #     show_graph_with_edge_labels(subgraph)
    # print(count)

    maximum_common_subgraph = max(all_common_subgraphs, key=len)
    return nx.induced_subgraph(matching_graph, maximum_common_subgraph)

def getMCS_directed(graph_of_words1: GraphOfWords, graph_of_words2: GraphOfWords):
    g1 = graph_of_words1.graph
    g2 = graph_of_words2.graph

    matching_graph=nx.DiGraph()

    if g1.number_of_nodes() > g2.number_of_nodes():
        for n1,n2 in g1.edges():
            if g2.has_edge(n1, n2):
                weight1 = g1.get_edge_data(n1, n2, default=0)['weight']
                weight2 = g2.get_edge_data(n1, n2, default=0)['weight']
                # match_weight = num_sim(weight1, weight2)
                match_weight = (weight1 + weight2)/2
                matching_graph.add_edge(n1, n2, weight=match_weight)
    else:
        for n1,n2 in g2.edges():
            if g1.has_edge(n1, n2):
                weight1 = g1.get_edge_data(n1, n2, default=0)['weight']
                weight2 = g2.get_edge_data(n1, n2, default=0)['weight']
                # match_weight = num_sim(weight1, weight2)
                match_weight = (weight1 + weight2)/2
                matching_graph.add_edge(n1, n2, weight=match_weight)

    all_common_subgraphs = nx.strongly_connected_components(matching_graph)

    # all_common_subgraphs_copy = nx.connected_components(matching_graph)
    # count = 0
    # for common_subgraph in all_common_subgraphs_copy:
    #     count = count + 1
    #     print('subgraph')
    #     subgraph = nx.induced_subgraph(matching_graph, common_subgraph)
    #     show_graph_with_edge_labels(subgraph)
    # print(count)

    maximum_common_subgraph = max(all_common_subgraphs, key=len)
    return nx.induced_subgraph(matching_graph, maximum_common_subgraph)

def get_union(graph_of_words1: GraphOfWords, graph_of_words2: GraphOfWords):
    graph1 = graph_of_words1.graph
    graph2 = graph_of_words2.graph

    composite_graph = graph1.copy()

    for n1,n2,w in graph2.edges(data=True):
        weight2 = w['weight']
        if composite_graph.has_edge(n1, n2):
            weight1 = composite_graph.get_edge_data(n1, n2, default=0)['weight']   
            composite_weight = weight1 if weight1 > weight2 else weight2
            composite_graph.add_edge(n1, n2, weight=composite_weight)
        else:
            composite_graph.add_edge(n1, n2, weight=weight2)

    return composite_graph


def num_sim(n1, n2):
  """ calculates a similarity score between 2 numbers """
  return 1 - abs(n1 - n2) / (n1 + n2)


def get_edge_weight_similarity_score_mcs(max_common_subgraph):
    nb_edges = max_common_subgraph.number_of_edges()
    sum = 0
    for n1, n2, w in max_common_subgraph.edges(data=True):
        sum = sum + w['weight']
    similarity_score = sum / nb_edges
    return similarity_score

def two_graphs_similarity_score(graph_of_words1: GraphOfWords, graph_of_words2: GraphOfWords):

    graph1 = graph_of_words1.graph
    graph2 = graph_of_words1.graph

    mcs_graph = getMCS(graph1,graph2)
    sim_edges_weights = get_edge_weight_similarity_score_mcs(mcs_graph)
    print('sim_edges_weights:',sim_edges_weights)

    union = nx.compose(graph1, graph2)

    nb_nodes1 = graph1.number_of_nodes()
    nb_nodes2 = graph2.number_of_nodes() 
    mcs_nb_nodes = mcs_graph.number_of_nodes()
    union_nb_nodes = union.number_of_nodes()
    sim_score_nodes = mcs_nb_nodes / union_nb_nodes
    sim_nodes_1 = 1 - abs(mcs_nb_nodes - nb_nodes1) / nb_nodes1
    sim_nodes_2 = 1 - abs(mcs_nb_nodes - nb_nodes2) / nb_nodes2
    print('nodes1:', nb_nodes1,'nodes2:', nb_nodes2, 'mcs_nb_nodes:', mcs_nb_nodes, 'union_nb_nodes:', union_nb_nodes)
    print('sim_score_nodes:',sim_score_nodes)
    print('sim_nodes_1:',sim_nodes_1)
    print('sim_nodes_2:',sim_nodes_2)

    nb_edges1 = graph1.number_of_edges()
    nb_edges2 = graph2.number_of_edges()
    mcs_nb_edges = mcs_graph.number_of_edges()
    union_nb_edges = union.number_of_edges()
    sim_score_edges = mcs_nb_edges / union_nb_edges
    sim_edges_1 = 1 - abs(mcs_nb_edges - nb_edges1) / nb_edges1
    sim_edges_2 = 1 - abs(mcs_nb_edges - nb_edges2) / nb_edges2
    print('edges1:', nb_edges1,'edges2:', nb_edges2, 'mcs_nb_edges:', mcs_nb_edges, 'union_nb_edges:', union_nb_edges)
    print('sim_score_edges:',sim_score_edges)
    print('sim_edges_1:',sim_edges_1)
    print('sim_edges_2:',sim_edges_2)


def get_graph_sum_weights(g: GraphOfWords):
    graph = g.graph
    sum = 0
    for n1, n2, w in graph.edges(data=True):
        sum = sum + w['weight']
    return sum


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

def graphs_similarity_value_based_on_edges_values(edges1, edges2):

    edges_1_2 = [edges1, edges2]
    all_edges = reduce(set.union, map(set, map(dict.keys, edges_1_2)))
    penalty = 0

    for edge in all_edges:
        if edge in edges1.keys() and edge in edges2.keys():
            penalty += abs(edges1.get(edge) - edges2.get(edge)) / max(edges1.get(edge), edges2.get(edge))
        else:
            penalty += 1

    return 1 - penalty / len(all_edges)

