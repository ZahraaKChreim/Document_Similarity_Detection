import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

class Graph_of_pages:

    def __init__(self, filename, threshold):

        self.graph = nx.Graph()
        data = pd.read_csv(filename)
        data = data[['id1','id2','similarity']]
        edges = []
        for row in data.iterrows():
            if row[1]['similarity'] >= threshold:
                edges.append((int(row[1]['id1']), int(row[1]['id2']), row[1]['similarity']))
        self.graph.add_weighted_edges_from(edges)

    def get_clusters(self):
        G = self.graph
        graph_connected_components = nx.connected_components(G)
        clusters = [G.subgraph(connected_component).copy() for connected_component in graph_connected_components]
        return clusters

def show_graph(G):
    pos = nx.spring_layout(G, k=10)
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_labels(G, pos)
    labels = {(n1,n2):str(weight) for n1, n2, weight in G.edges(data="weight")}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=.66)
    plt.show()


if __name__ ==  '__main__':

    filename = 'CSVs/live in canada_data.csv'
    threshold = 0.7
    g = Graph_of_pages(filename, threshold)
    clusters = g.get_clusters()
    for cluster in clusters:
        #show_graph(cluster)
        print(len(cluster.nodes), cluster.nodes)
        print("--------------------------------------------------------")