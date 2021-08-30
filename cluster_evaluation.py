import numpy as np
from pandas.core.frame import DataFrame
from pandas.io.parsers import TextFileReader
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
import graph_cluster
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.metrics import adjusted_rand_score, rand_score, adjusted_mutual_info_score, normalized_mutual_info_score, mutual_info_score
from sklearn.metrics import homogeneity_score, completeness_score, v_measure_score, fowlkes_mallows_score

id1s = []
id2s = []

threshold = 0.8
distance_th = 1 - threshold

def read_data(filename):
    data = pd.read_csv(filename)
    data = data[['id1','id2','similarity']]
    #data = data[['similarity']]
    return data

def get_pairwise_similarity_matrix(data: TextFileReader):
    #summary = data.groupby(['id1', 'id2']).size().unstack().fillna(0)
    
    data_id1 = data['id1']
    data_id2 = data['id2']
    for id1 in data_id1:
        if not id1s.__contains__(id1):
            id1s.append(id1)

    for id2 in data_id2:
        if not id2s.__contains__(id2):
            id2s.append(id2)

    for id in id1s:
        if id not in id2s:
            id2s.append(id)

    for id in id2s:
        if id not in id1s:
            id1s.append(id)

    id2s.sort()
    id1s.sort()

    pairwise = pd.DataFrame(
        #squareform(pdist(summary)),
        0,
        columns = id1s,
        index = id2s
    )

    for index, row in data.iterrows():
        if row['similarity'] > 1:
            pairwise.loc[row['id1'], row['id2']] = 1
            pairwise.loc[row['id2'], row['id1']] = 1
        else:
            pairwise.loc[row['id1'], row['id2']] = row['similarity']
            pairwise.loc[row['id2'], row['id1']] = row['similarity']

    for id in id1s:
        pairwise.loc[id, id] = 1
    
    return pairwise

def cluster_agglomerative(pairwise_distance_matrix: DataFrame):
   
    clustering = AgglomerativeClustering(n_clusters=None, affinity='precomputed', compute_full_tree=True, linkage='single', distance_threshold=distance_th, compute_distances=False)
    clustering.fit(pairwise_distance_matrix)
    nb_clusters = clustering.n_clusters_
    labels = clustering.labels_
    
    clusters = [None] * nb_clusters
    for i in range(nb_clusters):
        clusters[i] = []

    for id, cluster_label in enumerate(labels):
        clusters[cluster_label].append(id1s[id])

    score_AGclustering_s = silhouette_score(pairwise_distance_matrix, labels, metric='precomputed')
    score_AGclustering_c = calinski_harabasz_score(pairwise_distance_matrix, labels)
    score_AGclustering_d = davies_bouldin_score(pairwise_distance_matrix, labels)
    print('Agglomerative Silhouette Score: %.4f' % score_AGclustering_s)
    print('Agglomerative Calinski Harabasz Score: %.4f' % score_AGclustering_c)
    print('Agglomerative Davies Bouldin Score: %.4f' % score_AGclustering_d)
    print("Agglomerative nb of clusters", len(clusters))

    """
    The Silhouette Coefficient is calculated using the mean intra-cluster distance (a)
    and the mean nearest-cluster distance (b) for each sample
    The best value is 1 and the worst value is -1. Values near 0 indicate overlapping clusters.
    The silhouette analysis measures how well an observation is clustered and it estimates the average distance 
    between clusters. 
    """

    """
    calinski_harabasz_score
    It is also known as the Variance Ratio Criterion.
    The score is defined as ratio between the within-cluster dispersion and the between-cluster dispersion.
    """

    """
    Davies-Bouldin score
    The score is defined as the average similarity measure of each cluster with its most similar cluster, where similarity is the ratio of within-cluster distances to between-cluster distances.
    Thus, clusters which are farther apart and less dispersed will result in a better score.
    The minimum score is zero, with lower values indicating better clustering.
    """

    return clusters, labels

def cluster_dbscan(pairwise_distance_matrix: DataFrame):
    clustering = DBSCAN(eps=distance_th, metric='precomputed', min_samples=5)
    clustering.fit(pairwise_distance_matrix)
    labels = clustering.labels_
    # https://www.datanovia.com/en/lessons/cluster-validation-statistics-must-know-methods/
    score_AGclustering_s = silhouette_score(pairwise_distance_matrix, labels, metric='precomputed')
    score_AGclustering_c = calinski_harabasz_score(pairwise_distance_matrix, labels)
    score_AGclustering_d = davies_bouldin_score(pairwise_distance_matrix, labels)
    print('DBSCAN Silhouette Score: %.4f' % score_AGclustering_s)
    print('DBSCAN Calinski Harabasz Score: %.4f' % score_AGclustering_c)
    print('DBSCAN Davies Bouldin Score: %.4f' % score_AGclustering_d)
    
    return labels
 
def main():
    filename = 'CSVs/crusades_data.csv'
    data = read_data(filename)
    pairwise_similarity_matrix = get_pairwise_similarity_matrix(data)
    pairwise_distance_matrix = 1 - pairwise_similarity_matrix

    agglomerative_clusters, agglomerative_clusters_labels = cluster_agglomerative(pairwise_distance_matrix)

    graph_clusters = graph_cluster.graph_clustering(filename, threshold)
    print('Graph nb of clusters', len(graph_clusters))

    #dbscan_clusters_labels = cluster_dbscan(pairwise_distance_matrix)

    graph_clusters_labels = [None] * len(id1s)
    for cluster_index, cluster in enumerate(graph_clusters):
        for id in cluster:
            index = id1s.index(id)
            graph_clusters_labels[index] = cluster_index

    score_AGclustering_s = silhouette_score(pairwise_distance_matrix, graph_clusters_labels, metric='precomputed')
    score_AGclustering_c = calinski_harabasz_score(pairwise_distance_matrix, graph_clusters_labels)
    score_AGclustering_d = davies_bouldin_score(pairwise_distance_matrix, graph_clusters_labels)
    print('Graph Silhouette Score: %.4f' % score_AGclustering_s)
    print('Graph Calinski Harabasz Score: %.4f' % score_AGclustering_c)
    print('Graph Davies Bouldin Score: %.4f' % score_AGclustering_d)


    # print("Compare Agglomerative and Graph Clustering:")
    # print("adjusted_rand_score", adjusted_rand_score(agglomerative_clusters_labels, graph_clusters_labels))
    # print("rand_score", rand_score(agglomerative_clusters_labels, graph_clusters_labels))


    # """
    # adjusted_rand_score
    # Given the knowledge of the ground truth class assignments labels_true and our clustering algorithm assignments of
    # the same samples labels_pred, the (adjusted or unadjusted) Rand index is a function that measures the similarity 
    # of the two assignments, ignoring permutations
    # """ 
    # print("adjusted_mutual_info_score", adjusted_mutual_info_score(agglomerative_clusters_labels, graph_clusters_labels))
    # print("normalized_mutual_info_score", normalized_mutual_info_score(agglomerative_clusters_labels, graph_clusters_labels))
    # print("mutual_info_score", mutual_info_score(agglomerative_clusters_labels, graph_clusters_labels))

    # """
    # homogeneity: each cluster contains only members of a single class.
    # completeness: all members of a given class are assigned to the same cluster.
    # Their harmonic mean is called V-measure
    # """
    # print("homogeneity_score", homogeneity_score(agglomerative_clusters_labels, graph_clusters_labels))
    # print("completeness_score", completeness_score(agglomerative_clusters_labels, graph_clusters_labels))
    # print("v_measure_score", v_measure_score(agglomerative_clusters_labels, graph_clusters_labels))

    # print("fowlkes_mallows_score", fowlkes_mallows_score(agglomerative_clusters_labels, graph_clusters_labels))

    # print("f1_hungarian", f1_hungarian(f_matrix(graph_clusters_labels, agglomerative_clusters_labels)))

    # print(normalize(contingency_matrix(labels_pred=agglomerative_clusters_labels, labels_true=graph_clusters_labels), norm='l1', axis=1))
    # print(normalize(contingency_matrix(labels_pred=graph_clusters_labels, labels_true=agglomerative_clusters_labels), norm='l1', axis=1))

    
    
from sklearn.metrics.cluster import contingency_matrix
from sklearn.preprocessing import normalize
from munkres import Munkres
# https://stackoverflow.com/questions/54915736/calculating-cluster-accuracy
def f_matrix(labels_pred, labels_true):
    # Calculate F1 matrix
    cont_mat = contingency_matrix(labels_pred=labels_pred, labels_true=labels_true)
    precision = normalize(cont_mat, norm='l1', axis=0)
    recall = normalize(cont_mat, norm='l1', axis=1)
    som = precision + recall
    f1 =  np.round(np.divide((2 * recall * precision), som, out=np.zeros_like(som), where=som!=0), 3)
    return f1

def f1_hungarian(f1):
    m = Munkres()
    inverse = 1 - f1
    indices = m.compute(inverse.tolist())
    fscore = sum([f1[i] for i in indices])/len(indices)
    return fscore
    

if __name__ ==  '__main__':
    main()