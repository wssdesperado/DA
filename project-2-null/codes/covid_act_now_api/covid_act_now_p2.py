from preprocess import *
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn import metrics


def gmm_cluster_dataset():
    files = ""
    l1 = []
    l2 = []
    total_quality_score = 0

    # get the files under the path
    for _, _, files in os.walk("./results/"):
        pass

    # Combine the data of two features into a two-dimensional array
    for file in files:
        l1_temp = []
        l2_temp = []
        data = pd.read_csv('./clean/' + file)
        l = data["vaccinesAdministered"].values
        y = data["icuCapacityRatio"].values

        length = l.size
        for i in range(length):
            if l[i] == 0:
                continue
            l1.append(l[i])
            l2.append(y[i])
            l1_temp.append(l[i])
            l2_temp.append(y[i])

        # calculate the quality score for each subset of the dataset
        l3_temp = np.array(list(zip(l1_temp, l2_temp)))
        gmm_temp = GaussianMixture(n_components=4).fit(l3_temp)
        labels_temp = gmm_temp.predict(l3_temp)
        quality_score = metrics.silhouette_score(l3_temp, labels_temp, metric='euclidean')
        total_quality_score += quality_score

    # GMM analyses the whole dataset
    d_2 = np.array(list(zip(l1, l2)))
    gmm = GaussianMixture(n_components=4).fit(d_2)
    labels = gmm.predict(d_2)
    plt.scatter(d_2[:, 1], d_2[:, 0], c=labels, s=40, cmap='viridis')
    print("The average quality score of the whole dataset is {}".format(total_quality_score / len(files)))
    plt.savefig('GMM_result.png')
    shutil.rmtree("./results")


def main():

    # preprocess the dataset to be more easily analyse
    preprocess()

    # use LOF to find outliers
    lof(3)

    # Separate the database according to different states
    separate_dataset()

    # data cleaning
    data_cleaning()

    # implement GMM cluster
    gmm_cluster_dataset()


if __name__ == '__main__':
    main()
