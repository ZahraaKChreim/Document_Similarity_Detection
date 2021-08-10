# https://gitlab.com/vi.le/graphofwords/-/tree/master

from itertools import tee
from nltk.tokenize import word_tokenize
import networkx as nx
import matplotlib.pyplot as plt
import typing
import numpy as np

class GraphOfWords:

    def __init__(self, window_size=4):

        self.window_size = window_size
        self.graph = nx.DiGraph()
    
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
    
    def build_graph(self, sentences: str):
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
    # Code from: https://github.com/peterewills/NetComp/blob/master/netcomp/distance/exact.py
    # graphs not necessary same number of vertices !!
    
    # Getting sets of vertices & edges
    V1,V2 = [set(G.nodes()) for G in [g1,g2]]
    E1,E2 = [set(G.edges()) for G in [g1,g2]]

    V_overlap = len(V1|V2)
    E_overlap = len(E1|E2)

    V_intersection = len(V1&V2)
    E_intersection = len(E1&E2)

    numerator = E_intersection
    denominator = E_overlap

    if numerator == 0:
        sim = 0
    else:
        sim = numerator / denominator

    return sim

def main(id1, id2):

    result1 = db.select_from_db_by_id(id1)
    result2 = db.select_from_db_by_id(id2)

    sim = getSimilarity.get_similarity_record1_record2(result1, result2)
    print("Graph Similarity:", sim)
    print("---------------------------------------------------------------------")

if __name__ ==  '__main__':

    import database_handler
    import getSimilarity
    db = database_handler.databaseHandler()
    print("---------------------------------------------------------------------")
    print("---------------------------------------------------------------------")
    print("MySQL connection is opened")

    id1 = 5701
    id2 = 5707
    main(id1, id2)

    id1 = 5707
    id2 = 5711
    main(id1, id2)

    id1 = 5756
    id2 = 5785
    main(id1, id2)

    id1 = 5759
    id2 = 5787
    main(id1, id2)

    id1 = 5759
    id2 = 5790
    main(id1, id2)

    id1 = 5700
    id2 = 5728
    main(id1, id2)

    id1 = 5701
    id2 = 5771
    main(id1, id2)

    id1 = 5700
    id2 = 5741
    main(id1, id2)

    id1 = 5700
    id2 = 5727
    main(id1, id2)

    id1 = 5700
    id2 = 5751
    main(id1, id2)

    id1 = 408
    id2 = 411
    main(id1, id2)
    

    if db.con.is_connected():
        db.con.close()
        print("MySQL connection is closed")

#     import preprocess

#     text1 = """Released by Paramount Pictures, Airplane! was a critical and commercial success, grossing $171 million worldwide against a budget of $3.5 million.[8] Its creators received the Writers Guild of America Award for Best Adapted Comedy, and nominations for the Golden Globe Award for Best Motion Picture – Musical or Comedy and for the BAFTA Award for Best Screenplay.
# In the years since its release, the film's reputation has grown substantially. Airplane! was ranked 6th on Bravo's '100 Funniest Movies'.[9] In a 2007 survey by Channel 4 in the United Kingdom, it was judged the second-greatest comedy of all time, behind Monty Python's Life of Brian.[10] In 2008, it was selected by Empire magazine as one of 'The 500 Greatest Movies of All Time' and in 2012 was voted #1 on 'The 50 Funniest Comedies Ever' poll.[11] In 2010, the film was selected for preservation in the United States National Film Registry by the Library of Congress as being "culturally, historically, or aesthetically significant".[12][13][14]"""

    
#     text1 = preprocess.get_semantically_preprocessed_paragraph(text1)

#     graph1 = GraphOfWords(window_size=4)
#     graph1.build_graph(text1)
#     g1 = graph1.graph
#     edges1 = g1.edges()
#     #show_graph(graph1)
#     #print(edges1)

#     text2 = """Released by Paramount , Airplane! was a commercial success, grossing $171 million worldwide against a budget of $3.5 million.[8] Its creators received the Writers Guild of America Award for Best Adapted Comedy, and nominations for the Golden Globe Award for Best Motion Picture – Musical or Comedy and for the BAFTA Award for Best Screenplay.
# the film's reputation has grown substantially. Airplane! was ranked 6th on Bravo's '100 Funniest Movies'.[9] In a 2007 survey by Channel 4 in the United Kingdom, it was judged the second-greatest comedy of all time, behind Monty Python's Life of Brian.[10] In 2008, it was selected by Empire magazine as one of 'The 500 Greatest Movies of All Time' and in 2012 was voted #1 on 'The 50 Funniest Comedies Ever' poll.[11] In 2010, the film was selected for preservation in the United States National Film Registry by the Library of Congress as being "culturally, historically, or aesthetically significant".[12][13][14]"""

    
#     text2 = preprocess.get_semantically_preprocessed_paragraph(text2)

#     graph2 = GraphOfWords(window_size=4)
#     graph2.build_graph(text2)
#     g2 = graph2.graph
#     edges2 = g2.edges()
#     #show_graph(graph2)
#     #print(edges2)

#     sim = graph_similarity(g1, g2)
#     print(sim)