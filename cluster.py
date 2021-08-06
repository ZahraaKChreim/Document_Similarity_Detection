import pandas as pd
import numpy as np

def read_data(filename):
    data = pd.read_csv(filename)
    data = data[['id1','id2','similarity']]
    return data

def grouper(iterable):
    prev = None
    group = []
    for item in iterable:
        if not prev or item - prev <= 0.2:
            group.append(item)
        else:
            yield group
            group = [item]
        prev = item
    if group:
        yield group

def cluster_numbers(data):
    return dict(enumerate(grouper(data), 1))

def manual_numbers_clustering(data, number_of_clusters):
    threshold = 1 / number_of_clusters
    clusters = {0: [data[0]]}
    #print(clusters)
    #centroids = [data[0]]
    for sim in data[1:]:
        #print('sim:', sim)
        global_min_dst = np.inf
        global_min_dst_index = -1

        for cluster_index, cluster in clusters.items():
            #print('cluster', cluster_index)
            local_min_dst = np.inf
            for similarity in cluster:
                dst = abs(sim - similarity)
                #print('dst', sim, similarity, '=', dst)
                if dst < local_min_dst:
                    local_min_dst = dst
                    #print('dst < local_min_dst=', local_min_dst)
            if local_min_dst < global_min_dst:
                #print('local_min_dst=', local_min_dst, '< global_min_dst=', global_min_dst)
                global_min_dst = local_min_dst
                global_min_dst_index = cluster_index
            #print('-------------------------')
        if global_min_dst > threshold:
            #print('global_min_dst_index=', global_min_dst_index, '>', threshold)
            #print("new cluster")
            i = list(clusters.keys())[-1] + 1
            clusters[i] = [sim]
        else:
            #print('global_min_dst_index=', global_min_dst_index, '<=', threshold)
            clusters[global_min_dst_index].append(sim)
            #print("append to existing clusters")
        #print("***************************************")



        # min_dist = np.inf
        # min_dist_index = -1

        # for index, centroid in enumerate(centroids):
        #     current_dst = abs(sim - centroid)
        #     if current_dst < min_dist:
        #         min_dist = current_dst
        #         min_dist_index = index

        # if min_dist > (1 / number_of_clusters):
        #     i = list(clusters.keys())[-1] + 1
        #     clusters[i] = [sim]
        #     centroids.append(sim)
        # else:
        #     clusters[min_dist_index].append(sim)
        #     centroids[min_dist_index] = (centroids[min_dist_index] + sim) / 2

    return clusters

def main(filename):
    data = read_data(filename)
    data = data['similarity']


    distict_similarities = []

    for value in data:
        if value > 1 :
            value = 1
        if value not in distict_similarities:
            distict_similarities.append(value)

    nb_of_clusters = 10
    clusters = manual_numbers_clustering(distict_similarities, nb_of_clusters)
    
    for index, cluster in clusters.items():
        print(index, ":", len(cluster), 'record')
        print(cluster)
        print('########################################################')

    #print(len(clusters))

if __name__ ==  '__main__':

    filename = 'crusades_data.csv'
    main(filename)

    filename = 'byzantines_data.csv'
    main(filename)