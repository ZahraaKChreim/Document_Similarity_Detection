import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.io.parsers import TextFileReader
import seaborn as sns
sns.set()
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform
import scipy.cluster.hierarchy as hcl
id1s = []
id2s = []
def read_data(filename):
    data = pd.read_csv(filename)
    data = data[['id1','id2','similarity']]
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
        pairwise.loc[row['id1'], row['id2']] = row['similarity']
        pairwise.loc[row['id2'], row['id1']] = row['similarity']

    
    return 1 - pairwise

# def to_matrix_using_pivot(data):
#     data_piv = data.pivot("id2", "id1", "similarity").fillna(0)
#     piv_arr = data_piv.values
#     dist_mat = piv_arr + np.transpose(piv_arr)
#     print(dist_mat)

def cluster_data(data):
    # from sklearn.cluster import AgglomerativeClustering
    # cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
    # cluster.fit(data)
    print(data[5699])
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

    pairwise_distance_matrix = to_matrix(data)
    #print(pairwise_distance_matrix)

    cluster_data(pairwise_distance_matrix)

    

    # clusters = hcl.linkage(squareform(pairwise_distance_matrix))
    # print(len(clusters))
    #cluster_data(pairwise_distance_matrix)
    #print(pairwise_distance_matrix)
    
    # import scipy.cluster.hierarchy as sch
    # dendrogram = sch.dendrogram(sch.linkage(pairwise_distance_matrix, method  = "ward"))
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