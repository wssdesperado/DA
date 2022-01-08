from sklearn.cluster import AgglomerativeClustering
import json
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn import metrics
from sklearn import decomposition
from sklearn import preprocessing
STATES_FILE_CLEAN = '../dataset/States_Daily_clean.json'
US_FILE_CLEAN = '../dataset/US_Daily_clean.json'

# hierarchical  clustering  method: ward
def cluster():
    with open(US_FILE_CLEAN) as f:
        json_data_states = json.load(f)
        inIcuCurrently_death_array = []
        positive_negative_array = []
        positive_array = []
        negative_array = []
        death_array = []
        death_bin_array = []
        i = 0
        for row in json_data_states:
                inIcuCurrently_death_array.append([row['inIcuCurrently'],row['death']])
                positive_array.append(row['positive'])
                positive_negative_array.append([row['onVentilatorCumulative'], row['death']])
                negative_array.append(row['negative'])
                death_array.append(row['death'])
                #death_bin_array.append(row['death_bin'])
                i = i + 1
    inIcuCurrently_death_array = np.array(inIcuCurrently_death_array)
    positive_negative_array = np.array(positive_negative_array)
    cls = AgglomerativeClustering(n_clusters=3,linkage='ward')
    cluster_group = cls.fit(inIcuCurrently_death_array)
    plt.figure(figsize=(10, 7))
    dend = shc.dendrogram(shc.linkage(inIcuCurrently_death_array, method='ward'))
    plt.title(' inIcuCurrently_death dendograms')
    plt.show()

    #show scatter diagram

    cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
    cluster_labels = cluster.fit_predict(inIcuCurrently_death_array)

    plt.figure(figsize=(10, 7))
    plt.scatter(inIcuCurrently_death_array[:,0], inIcuCurrently_death_array[:,1], c=cluster.labels_, cmap='rainbow')
    plt.title('inIcuCurrently_death dendograms')
    plt.show()

    #evaluate
    silhouette_avg = silhouette_score(inIcuCurrently_death_array, cluster_labels)
    print("The average silhouette_score is :", silhouette_avg)

# #k-means
# myData=pd.concat([pd.DataFrame(positive_array),pd.DataFrame(negative_array),pd.DataFrame(death_array),pd.DataFrame(death_bin_array)],axis=1, keys=['postive','negative', 'death','death_bin'])
# myData = pd.DataFrame(myData)
# x = myData.values # returns a numpy array
# min_max_scaler = preprocessing.MinMaxScaler()
# x_scaled = min_max_scaler.fit_transform(x)
# normalizedDataFrame = pd.DataFrame(x_scaled)
# k = 3
# kmeans = KMeans(n_clusters=k)
# cluster_labels = kmeans.fit_predict(myData)
# print(myData)
# # Determine if the clustering is good
# silhouette_avg = silhouette_score(normalizedDataFrame, cluster_labels)
# print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)
#
# centroids = kmeans.cluster_centers_
# # print(cluster_labels)
# # print(centroids)
# # print(pd.crosstab(cluster_labels, positive_array))
# # print(pd.crosstab(cluster_labels, negative_array))
# pca2D = decomposition.PCA(2)
#
# # Turn the data into two columns with PCA
# pca2D = pca2D.fit(normalizedDataFrame)
# plot_columns = pca2D.transform(normalizedDataFrame)
# plt.scatter(x = plot_columns[:,0], y = plot_columns[:,1], c=cluster.labels_,cmap='rainbow')
# # for i in range(k):
# #     plt.annotate('中心'+str(i + 1),(centroids[i,0],centroids[i,1]))
#
# plt.show()

def main():
    cluster()

if __name__ == '__main__':
    main()
