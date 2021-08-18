import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

class Graph_of_pages:

    def __init__(self, filename, threshold):

        self.graph = nx.Graph()
        data = pd.read_csv(filename)
        data = data[['id1','id2','similarity']]
        edges = []
        self.all_pages = []
        self.individual_pages = []
        for row in data.iterrows():
            if int(row[1]['id1']) not in self.all_pages:
                self.all_pages.append(int(row[1]['id1']))
            if row[1]['similarity'] >= threshold:
                edges.append((int(row[1]['id1']), int(row[1]['id2']), row[1]['similarity']))
        self.graph.add_weighted_edges_from(edges)
        for page in self.all_pages:
            if page not in self.graph:
                self.individual_pages.append(page)

    def get_clusters(self):
        G = self.graph
        graph_connected_components = nx.connected_components(G)
        connected_components = [G.subgraph(connected_component).copy() for connected_component in graph_connected_components]

        clusters = []
        for connected_component in connected_components:
            clusters.append(connected_component.nodes)
        return clusters

def show_graph(G):
    pos = nx.spring_layout(G, k=10)
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_labels(G, pos)
    labels = {(n1,n2):str(weight) for n1, n2, weight in G.edges(data="weight")}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=.66)
    plt.show()

def get_final_clusters(filename, threshold):
    g = Graph_of_pages(filename, threshold)
    clusters = g.get_clusters()
    individual_pages = g.individual_pages
    for individual_page in individual_pages:
        clusters.append([individual_page])
    return clusters

def main(filename, threshold):

    reduced_pages = 0
    clusters = get_final_clusters(filename, threshold)
    initial_number = 0

    for cluster in clusters:
        initial_number += len(cluster)
        reduced_pages += (len(cluster) -1 )
    
    new_nb_of_pages = initial_number - reduced_pages
    print(filename)
    print("initial_number", initial_number)
    print("reduced_pages", reduced_pages)
    print("new_nb_of_pages", new_nb_of_pages)
    print("--------------------------------------------------------")

if __name__ ==  '__main__':

    threshold = 0.75
    directory = "CSVs"
    import os
    files = os.listdir(directory)
    for file in files:
        filename = directory + '/' + file
        main(filename, threshold)
    

    