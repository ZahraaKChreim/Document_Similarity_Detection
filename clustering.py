import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn.cluster import KMeans

def read_data(filename):
    data = pd.read_csv(filename)
    #data = data[['id1','id2','similarity']]
    #data = data.groupby(['id1','id2'])
    #data.columns = ['similarity']
    #print(data[:10])
    #return data

    # from scipy.spatial.distance import squareform, pdist
    # data = pd.DataFrame(squareform(pdist(data.iloc[:, 1:])), columns=data.id1.unique(), index=data.id1.unique())
    # print(data)
    from scipy.spatial import distance_matrix
    pd.DataFrame(distance_matrix(data.similarity, data.similarity), index=data.id1, columns=data.id2)

def to_matrix(data):
    
    ids = []
    for index, row in data.iterrows():
        #print(row['id1'], row['id2'], row['similarity'])
        if not ids.__contains__(row['id1']):
            ids.append(row['id1'])
        if not ids.__contains__(row['id2']):
            ids.append(row['id2'])

    matrix = np.zeros((len(ids), len(ids)))
    for index, row in data.iterrows():
        matrix[str(row['id1'])][str(row['id2'])] = row['similarity']

    print(matrix)

def show_data(data):
    plt.scatter(data['id1'], data['similarity'])
    plt.xlabel = (data['id1'], data['id2'])
    plt.ylabel = data['similarity']
    plt.show()

def cluster_data(data):
    clusters = data.copy()
    kMeans = KMeans(10)
    clusters['cluster_predict'] = kMeans.fit_predict(clusters)
    return clusters

def main(filename):

    data = read_data(filename)
    #to_matrix(data[:10])
    #X = data.values
    # X = data(['id1', 'id2', 'similarity'])
    # import scipy.cluster.hierarchy as sch
    # # dendrogram = sch.dendrogram(sch.linkage(X, method  = "ward"))
    # # plt.title('Dendrogram')
    # # plt.xlabel('Customers')
    # # plt.ylabel('Euclidean distances')
    # # plt.show()
    # from sklearn.cluster import AgglomerativeClustering 
    # hc = AgglomerativeClustering(n_clusters = 3, affinity = 'euclidean', linkage ='ward')
    # y_hc=hc.fit_predict(X)
    # plt.scatter(X[y_hc==0, 0], X[y_hc==0, 1], s=100, c='red', label ='Cluster 1')
    # plt.scatter(X[y_hc==1, 0], X[y_hc==1, 1], s=100, c='blue', label ='Cluster 2')
    # plt.scatter(X[y_hc==2, 0], X[y_hc==2, 1], s=100, c='green', label ='Cluster 3')
    # plt.title('Clusters of Customers (Hierarchical Clustering Model)')
    # plt.xlabel('Annual Income(k$)')
    # plt.ylabel('Spending Score(1-100')
    # plt.show()




if __name__ ==  '__main__':

    filename = 'byzantines_data.csv'
    main(filename)