import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os

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
        last_index = len(data['id2']) - 1
        if data['id2'][last_index] not in self.all_pages:
            self.all_pages.append(data['id2'][last_index])
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
    
    reduction_percentage = get_final_results(clusters)
    return format(reduction_percentage,".2f")
    #return clusters

def get_before_after(filename, threshold):
    g = Graph_of_pages(filename, threshold)
    clusters = g.get_clusters()
    individual_pages = g.individual_pages
    for individual_page in individual_pages:
        clusters.append([individual_page])
    
    before, after = get_final_results_before_after(clusters)
    return before, after

def get_final_results_before_after(clusters):
    reduced_pages = 0
    initial_number = 0

    for cluster in clusters:
        initial_number += len(cluster)
        reduced_pages += (len(cluster) -1 )
    
    new_nb_of_pages = initial_number - reduced_pages
    return initial_number, new_nb_of_pages

def graph_clustering(filename, threshold):
    g = Graph_of_pages(filename, threshold)
    clusters = g.get_clusters()
    individual_pages = g.individual_pages
    for individual_page in individual_pages:
        clusters.append([individual_page])
    return clusters


def get_final_results(clusters):
    reduced_pages = 0
    initial_number = 0

    for cluster in clusters:
        initial_number += len(cluster)
        reduced_pages += (len(cluster) -1 )
    
    #new_nb_of_pages = initial_number - reduced_pages
    reduction_percentage = ( reduced_pages / initial_number ) * 100
    return reduction_percentage

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

def general_cluster_data():

    print("Function cluster_data Started... ")
    #list_of_thresholds = [0.7, 0.725, 0.75, 0.775, 0.8, 0.825, 0.85, 0.875, 0.9]

    list_of_queries = []

    reduction_for_threshold_7 = []
    reduction_for_threshold_725 = []
    reduction_for_threshold_75 = []
    reduction_for_threshold_775 = []
    reduction_for_threshold_8 = []
    reduction_for_threshold_825 = []
    reduction_for_threshold_85 = []
    reduction_for_threshold_875 = []
    reduction_for_threshold_9 = []

    columns = ['query', '0.7', '0.725', '0.75', '0.775', '0.8', '0.825', '0.85', '0.875', '0.9']

    directory = "CSVs"
    data_files = os.listdir(directory)

    i = 1
    for file in data_files:

        filename = directory + '/' + file

        query = file.split('_')[0]
        list_of_queries.append(query)
        print("File", i, "of 150 -", query)
        i += 1

        reduction_for_threshold_7.append(get_final_clusters(filename, 0.7))
        reduction_for_threshold_725.append(get_final_clusters(filename, 0.725))
        reduction_for_threshold_75.append(get_final_clusters(filename, 0.75))
        reduction_for_threshold_775.append(get_final_clusters(filename, 0.775))
        reduction_for_threshold_8.append(get_final_clusters(filename, 0.8))
        reduction_for_threshold_825.append(get_final_clusters(filename, 0.825))
        reduction_for_threshold_85.append(get_final_clusters(filename, 0.85))
        reduction_for_threshold_875.append(get_final_clusters(filename, 0.875))
        reduction_for_threshold_9.append(get_final_clusters(filename, 0.9))

    data = {
        'query':list_of_queries,
        '0.7': reduction_for_threshold_7,
        '0.725': reduction_for_threshold_725, 
        '0.75': reduction_for_threshold_75, 
        '0.775': reduction_for_threshold_775, 
        '0.8': reduction_for_threshold_8, 
        '0.825': reduction_for_threshold_825, 
        '0.85': reduction_for_threshold_85, 
        '0.875': reduction_for_threshold_875, 
        '0.9': reduction_for_threshold_9
    }

    df = pd.DataFrame(data, columns= columns)
    file_name = "general_results.csv"
    file_name = r''+file_name
    df.to_csv (file_name, index = True, header=True, encoding='utf8')

    print("Function cluster_data Done")

def cluster_data():

    print("Function cluster_data Started... ")
    #list_of_thresholds = [0.6, 0.63, 0.67, 0.7, 0.71, 0.74, 0.77, 0.8, 0.87, 0.9]

    list_of_queries = []

    reduction_for_threshold_6 = []
    reduction_for_threshold_63 = []
    reduction_for_threshold_67 = []
    reduction_for_threshold_7 = []
    reduction_for_threshold_71 = []
    reduction_for_threshold_74 = []
    reduction_for_threshold_77 = []
    reduction_for_threshold_8 = []
    reduction_for_threshold_87 = []
    reduction_for_threshold_9 = []

    columns = ['query', '0.6', '0.63', '0.67', '0.7', '0.71', '0.74', '0.77', '0.8', '0.87', '0.9']

    directory = "CSVs"
    data_files = os.listdir(directory)

    i = 1
    for file in data_files:

        filename = directory + '/' + file

        query = file.split('_')[0]
        list_of_queries.append(query)
        print("File", i, "of 150 -", query)
        i += 1
        
        reduction_for_threshold_6.append(get_final_clusters(filename, 0.6))
        reduction_for_threshold_63.append(get_final_clusters(filename, 0.63))
        reduction_for_threshold_67.append(get_final_clusters(filename, 0.67))
        reduction_for_threshold_7.append(get_final_clusters(filename, 0.7))
        reduction_for_threshold_71.append(get_final_clusters(filename, 0.71))
        reduction_for_threshold_74.append(get_final_clusters(filename, 0.74))
        reduction_for_threshold_77.append(get_final_clusters(filename, 0.77))
        reduction_for_threshold_8.append(get_final_clusters(filename, 0.8))
        reduction_for_threshold_87.append(get_final_clusters(filename, 0.87))
        reduction_for_threshold_9.append(get_final_clusters(filename, 0.9))

    data = {
        'query':list_of_queries,
        '0.6': reduction_for_threshold_6,
        '0.63': reduction_for_threshold_63, 
        '0.67': reduction_for_threshold_67, 
        '0.7': reduction_for_threshold_7, 
        '0.71': reduction_for_threshold_71, 
        '0.74': reduction_for_threshold_74, 
        '0.77': reduction_for_threshold_77, 
        '0.8': reduction_for_threshold_8, 
        '0.87': reduction_for_threshold_87, 
        '0.9': reduction_for_threshold_9
    }

    df = pd.DataFrame(data, columns= columns)
    file_name = "results.csv"
    file_name = r''+file_name
    df.to_csv (file_name, index = True, header=True, encoding='utf8')

    print("Function cluster_data Done")


def cluster_data_before_after(threshold):

    print("Function cluster_data Started... ")

    list_of_queries = []

    numbers_before = []
    numbers_after = []
    reduction = []

    columns = ['query', 'before', 'after', 'reduction']

    directory = "CSVs"
    data_files = os.listdir(directory)

    i = 1
    for file in data_files:

        filename = directory + '/' + file

        query = file.split('_')[0]
        list_of_queries.append(query)
        print("File", i, "of 150 -", query)
        i += 1

        before, after = get_before_after(filename, threshold)
        numbers_before.append(before)
        numbers_after.append(after)
        reduced_pages = before - after
        reduction.append(( reduced_pages / before ) * 100)

    data = {
        'query':list_of_queries,
        'before': numbers_before,
        'after': numbers_after,
        'reduction' : reduction
    }

    df = pd.DataFrame(data, columns= columns)
    file_name = "before_after_results.csv"
    file_name = r'' + str(threshold) + "_" + file_name
    df.to_csv (file_name, index = True, header=True, encoding='utf8')

    print("Function cluster_data Done")


if __name__ ==  '__main__':

    cluster_data_before_after(0.8)
    cluster_data_before_after(0.9)
