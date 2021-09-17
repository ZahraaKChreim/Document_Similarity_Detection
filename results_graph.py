import matplotlib.pyplot as plt
 

def cluster_evaluation(): 
    x = [0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.87, 0.9]


    y1 = [0.2994, 0.2990, 0.2990, 0.2990, 0.2757, 0.2757, 0.2757, 0.2757, 0.1887, 0.1887, 0.1887, 0.1817, 0.1817, 0.1817, 0.0773, 0.0698, 0.0633, 0.0379, 0.0318, 0.0191, 0.0187, 0.0033, 0.0068]
    plt.plot(x, y1, label = "Silhouette Coefficient")
    
    y2 = [0.1316, 0.1268, 0.1268, 0.1268, 0.1269, 0.1269, 0.1269, 0.1269, 0.1443, 0.1443, 0.1443, 0.1459, 0.1459, 0.1459, 0.1995, 0.2352, 0.2439, 0.2837, 0.3182, 0.3431, 0.3456, 0.2278, 0.1223]
    plt.plot(x, y2, label = "Davies Bouldin Score")

    y3 = [0.0026, 0.0372, 0.0372, 0.0372, 0.0685, 0.0685, 0.0685, 0.0685, 0.0863, 0.0863, 0.0863, 0.1050, 0.1050, 0.1050, 0.0969, 0.0954, 0.0933, 0.0913, 0.0813, 0.0752, 0.0801, 0.3272, 0.9992]
    plt.plot(x, y3, label = "Calinski Harabasz Score")

    plt.axvline(x=0.67, color='red', linestyle='--')
    
    # naming the x axis
    plt.xlabel('Similarity Threshold')
    # naming the y axis
    plt.ylabel('Score Value')
    # giving a title to my graph
    plt.title('Clustering Evaluation')
    
    # show a legend on the plot
    plt.legend()
    
    # function to show the plot
    plt.show()

def pages_reduction():
    # x-coordinates of x sides of bars
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # ys of bars
    y = [71.8, 68, 61.2, 54.6, 51.1, 40.3, 27.5, 13.5, 1.1, 0.6]
    
    # labels for bars
    tick_label = ['0.6', '0.63', '0.67', '0.7', '0.71', '0.74', '0.77', '0.8', '0.87', '0.9']

    width = 0.5
    
    # plotting a bar chart
    ax = plt.bar(x, y, tick_label = tick_label,
            width = width, color = ['green'])
    

    # naming the x-axis
    plt.xlabel('Similarity Threshold')
    # naming the y-axis
    plt.ylabel('Reduction Percentage')
    # plot title
    plt.title('Pages Reduction')


    for p in ax:
        height = p.get_height()
        plt.text(x=p.get_x() + p.get_width() / 2, y=height+.10,
            s="{}%".format(height),
            ha='center')
    # function to show the plot
    plt.show()

def external_clustering():
    
    # ys of bars
    y = [1, 1, 1, 1, 1, 1, 1, 1]
    
    # labels for bars
    x = ["ARI", "RI", "AMIS", "NMIS", "FMS", "HM", "CM", "VM"]

    plt.plot(x, y)
    

    # naming the x-axis
    plt.xlabel('Metric')
    # naming the y-axis
    plt.ylabel('Value')
    # plot title
    plt.title('External Cluster Validation Metrics')

    # function to show the plot
    plt.show()

if __name__ ==  '__main__':
    external_clustering()