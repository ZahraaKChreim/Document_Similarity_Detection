import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.construction import array
from pandas.io.parsers import TextFileReader
import seaborn as sns
sns.set()
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform
import scipy.cluster.hierarchy as hcl
from sklearn.metrics import pairwise_distances

id1s = []
id2s = []

def read_data(filename):
    data = pd.read_csv(filename)
    data = data[['id1','id2','similarity']]
    #data = data[['similarity']]
    return data

def to_matrix(data: TextFileReader):
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

    
    return pairwise

def manual_agglomerative_clustering(data):
    #matrix = to_matrix(data)
    similarity_column_data = data['similarity'].values
    initial_clusters = {k: [] for k in range(1, len(similarity_column_data)+1)}
    
    i = 1
    for sim in similarity_column_data:
        initial_clusters[i].append(sim)
        i += 1

    similarity_column_data = similarity_column_data.reshape(-1, 1)

    distance_matrix = pairwise_distances(similarity_column_data, Y=None, metric='euclidean')
    # print(matrix)
    # print(distance_matrix.__index__)

    from scipy.cluster.hierarchy import dendrogram, linkage
    from scipy.cluster import hierarchy as hier
    #condensed_dist_matrix = squareform(distance_matrix)
    Z = linkage(distance_matrix, method='centroid', metric='euclidean')
    #d = dendrogram(Z)

    idx = hier.fcluster(Z,0.5*distance_matrix.max(), 'distance')
    #print(idx)
    
    ids = []
    for id in idx:
        if id not in ids:
            ids.append(id)
    nb_clusters = len(ids)
    clusters = {k: [] for k in range(1, nb_clusters+1)}
    for index, id in enumerate(idx):
        clusters[id].append(similarity_column_data[index])

    print(clusters)

    # min_value = np.inf
    # for i in range(len(distance_matrix)):
    #     for j in range(i):
    #         if( distance_matrix[i][j] < min_value):
    #             min_value = distance_matrix[i][j]
    #             min_i = i
    #             min_j = j

    # for i in range(len(distance_matrix)):
    #     if( i > min_i  and i < min_j ):
    #         distance_matrix[i][min_i] = min(distance_matrix[i][min_i],distance_matrix[min_j][i])

    #     elif( i > min_j ):
    #         distance_matrix[i][min_i] = min(distance_matrix[i][min_i],distance_matrix[i][min_j])

    # for j in range(len(distance_matrix)):
    #     if( j < min_i ):
    #         distance_matrix[min_i][j] = min(distance_matrix[min_i][j],distance_matrix[min_j][j])

    # #remove one of the old clusters data from the distance matrix
    # distance_matrix = np.delete(distance_matrix, min_j, axis=1)
    # distance_matrix = np.delete(distance_matrix, min_j, axis=0)

    # print(distance_matrix)

    # A = []
    # A[min_i] = A[min_i] + A[min_j] 
    # A.pop(min_j)

    # from scipy.cluster.hierarchy import dendrogram, linkage
    # from scipy.cluster import hierarchy as hier
    # from scipy.spatial import distance as ssd
    # Z = linkage(ssd.pdist(similarity_column_data), method="average")

    # fig, ax = plt.subplots(nrows=4)
    # ax[2].set_title("pdist")
    # Z = linkage(ssd.pdist(similarity_column_data), method="average")
    # hier.dendrogram(Z, ax=ax[2])
    # plt.show()
    #print(pairwise_distance_matrix)

    # dst_matrix = pd.DataFrame(
    #     pairwise_distance_matrix,
    #     columns = initial_clusters.keys(),
    #     index = initial_clusters.keys()
    # )

    # print(dst_matrix)

# def to_matrix_using_pivot(data):
#     data_piv = data.pivot("id2", "id1", "similarity").fillna(0)
#     piv_arr = data_piv.values
#     dist_mat = piv_arr + np.transpose(piv_arr)
#     print(dist_mat)

def dbscan_cluster_data(X):

    """Precomputed distance matrix in DBSCAN"""

    from sklearn.cluster import DBSCAN

    db = DBSCAN(metric='precomputed').fit(X)
    # core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    # core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)
    print(labels)

    # #############################################################################
    # Plot result

    # Black removed and is used for noise instead.
    # unique_labels = set(labels)
    # colors = [plt.cm.Spectral(each)
    #         for each in np.linspace(0, 1, len(unique_labels))]
    # for k, col in zip(unique_labels, colors):
    #     if k == -1:
    #         # Black used for noise.
    #         col = [0, 0, 0, 1]

    #     class_member_mask = (labels == k)

    #     xy = X[class_member_mask & core_samples_mask]
    #     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
    #             markeredgecolor='k', markersize=14)

    #     xy = X[class_member_mask & ~core_samples_mask]
    #     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
    #             markeredgecolor='k', markersize=6)

    # plt.title('Estimated number of clusters: %d' % n_clusters_)
    # plt.show()

    # nb_clusters = len(Counter(clustering.labels_))
    
    # cluster_map = pd.DataFrame()
    # cluster_map['data_index'] = pairwise_distance_matrix.index.values
    # cluster_map['cluster'] = clustering.labels_

    # cluster1 = cluster_map[cluster_map.cluster == -1]
    # cluster2 = cluster_map[cluster_map.cluster == 0]
    # cluster3 = cluster_map[cluster_map.cluster == 1]

    # cluster1_ids = cluster1['data_index'].index
    # cluster2_ids = cluster2['data_index'].index
    # cluster3_ids = cluster3['data_index'].index

    # return cluster1_ids, cluster2_ids, cluster3_ids

def cluster_data(data):
    
    

    from sklearn.cluster import AgglomerativeClustering
    # cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
    # cluster.fit(data)
    #print(cluster.labels_)

    # plt.figure(figsize =(6, 6))
    # plt.scatter(data['id1'], data['id2'],
    #             c = cluster.fit_predict(data), cmap ='rainbow')
    # plt.show()

    # j = np.where(cluster.labels_ == 0)
    # for a in j:
    #     print(data.__getitem__(a))

    #plt.scatter(id1s, cluster.labels_, s=200, cmap='gray')

    # plt.figure(figsize=(10, 7))  
    # plt.scatter(data['id1'], data['id2'], data['similarity'], c=cluster.labels_) 
    #plt.show()


def main(filename):
    data = read_data(filename)
    # data_similarity = data['similarity']
    # plt.hist(data_similarity, len(data_similarity)) 
    # plt.title("histogram") 
    # plt.show()
    #manual_agglomerative_clustering(data)

    pairwise_distance_matrix = to_matrix(data)
    dbscan_cluster_data(pairwise_distance_matrix)
    print(pairwise_distance_matrix)

    # cluster1_ids, cluster2_ids, cluster3_ids = dbscan_cluster_data(pairwise_distance_matrix)
    # similarities = []
    # for index in cluster3_ids:
    #     similarities.append(data.at[index, 'similarity'])
    # for sim in similarities:
    #     print(sim)
    
    # plt.bar(np.arange(len(similarities)), similarities)
    # plt.show()

    # clusters = hcl.linkage(squareform(pairwise_distance_matrix))
    # print(len(clusters))
    #cluster_data(pairwise_distance_matrix)
    #print(pairwise_distance_matrix)
    
    # import scipy.cluster.hierarchy as sch
    # dendrogram = sch.dendrogram(sch.linkage(data, method  = "ward"))
    # plt.title('Dendrogram')
    # plt.xlabel('Customers')
    # plt.ylabel('Euclidean distances')
    # plt.show()

    # from sklearn.cluster import AgglomerativeClustering 
    # hc = AgglomerativeClustering(n_clusters = 3, affinity = 'euclidean', linkage ='ward')
    # y_hc=hc.fit_predict(pairwise_distance_matrix)
    # plt.scatter(pairwise_distance_matrix[y_hc==0, 0], pairwise_distance_matrix[y_hc==0, 1], s=100, c='red', label ='Cluster 1')
    # plt.scatter(pairwise_distance_matrix[y_hc==1, 0], pairwise_distance_matrix[y_hc==1, 1], s=100, c='blue', label ='Cluster 2')
    # plt.scatter(pairwise_distance_matrix[y_hc==2, 0], pairwise_distance_matrix[y_hc==2, 1], s=100, c='green', label ='Cluster 3')
    # plt.title('Clusters of Customers (Hierarchical Clustering Model)')
    # plt.xlabel('Annual Income(k$)')
    # plt.ylabel('Spending Score(1-100')
    # plt.show()

    # linkage_matrix = hcl.linkage(squareform(pairwise_distance_matrix, method='single', metric='euclidean'))
    # print(linkage_matrix)

    

    




if __name__ ==  '__main__':

    filename = 'byzantines_data.csv'
    main(filename)