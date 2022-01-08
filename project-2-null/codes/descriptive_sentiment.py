#############################
# Data analytics for twitter sentiments dataset
# box link: https://georgetown.app.box.com/folder/0
# The dataset this code use needs to download from box link
# Dataset:
# 'dataset/tweetid_userid_keyword_sentiments_emotions_United States.csv' for 'wholeData'
# 'dataset/reshaped_sentiments_data'  for 'subData'
# Picture Save:
# Histogram and KMeans scatter Pictures will saved in '.../picture' in two separate folders
#############################

from tweet_data import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
import datetime
from dateutil.relativedelta import relativedelta
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn import decomposition
from collections import Counter


# Binning strategy
def bin(myData):
    print('\nBinning strategy start...')
    # bin the 'valence_intensity' attribute for 5 parts
    # very negative<negative<neutral or mixed<positive<very positive
    names = range(1, 6)
    valence = [0, 0.3, 0.48, 0.52, 0.7, 1]
    myData['sentimentGroups'] = pd.cut(myData[intensity_keys[0]], valence, labels=names)

    # bin the four emotion attributes for 4 parts
    # have no relationship --> have  many relationships
    emotion = [0, 0.3, 0.5, 0.7, 1]
    names = range(1, 5)
    emotionList = intensity_keys[1:]
    binGroupName = ['fearGroups', 'angerGroups', 'happinessGroups', 'sadnessGroups']
    for emo, binName in zip(emotionList, binGroupName):
        myData[binName] = pd.cut(myData[emo], emotion, labels=names)
    # Check the data to see the new column ####
    print("New column of data after bin (first 5 rows):")
    print(myData[:5])

    # print("\n Bin Counts\n")
    # print(myData['sentimentGroups'].value_counts())
    # print(myData['fearGroups'].value_counts())
    # print(myData['angerGroups'].value_counts())
    # print(myData['happinessGroups'].value_counts())
    # print(myData['sadnessGroups'].value_counts())


# KMeans
def K_Means(myData,PIOT):
    # KMeans
    print('\nKMeans start...')
    k = 4
    sentiFrame = pd.concat(
        [myData['sentimentGroups'], myData['fearGroups'], myData['angerGroups'],
         myData['happinessGroups'], myData['sadnessGroups']],
        axis=1, keys=['valence', 'fear', 'anger', 'happiness', 'sadness'])
    # sentiFrame = pd.concat(
    #     [myData['valence_intensity'], myData['fear_intensity'], myData['anger_intensity'],
    #      myData['happiness_intensity'], myData['sadness_intensity']],
    #     axis=1, keys=['valence', 'fear', 'anger', 'happiness', 'sadness'])
    sentiment = pd.DataFrame(sentiFrame.values)  # returns a numpy array
    kmeans = KMeans(n_clusters=k)
    # save the label of cluster
    cluster_labels = kmeans.fit_predict(sentiment)
    print('The first 20 labels:')
    print(cluster_labels[0:20])
    # exit()
    # Determine if the clustering is good
    silhouette_avg = silhouette_score(sentiment, cluster_labels)
    print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)
    # Get the centers of each cluster
    centroids = kmeans.cluster_centers_
    print('label length:', len(cluster_labels))
    print(myData.values.shape)
    print('center:',centroids)

    # PCA
    # Plot the result of KMeans using PCA
    # convert the high dimensional data to 2 dimensions
    pca2D = decomposition.PCA(2)
    # Turn the data into two columns with PCA
    pca2D = pca2D.fit(sentiment)
    plot_columns = pca2D.transform(sentiment)
    # This shows how good the PCA performs on this dataset
    print(pca2D.explained_variance_)

    # Plot
    # Plot using a scatter plot and shade by cluster label
    time = myData['tweet_timestamp'].values
    datetime = time[0]
    plt.figure()
    name = '../picture/k-means/sentiment_scatter_plot' + datetime[:7] + '.png'
    plt.scatter(x=plot_columns[:, 0], y=plot_columns[:, 1], c=cluster_labels)
    plt.title(datetime[:7] + ' Sentiment scatter plot using PCA')
    # Save plot
    plt.savefig(name)
    # plot if necessary
    if PIOT:
        plt.show()
    # Clear plot
    plt.clf()
    print('KMeans finished！')


# plot histogram
def showHist(myData,flag,PLOT):
    # show the distribution of sentiment
    print('\nBegin to save Distribution pictures')
    count=1
    plt.figure(figsize=(20, 10), dpi=60)
    for var in intensity_keys:
        plt.subplot(2, 3, count)
        # Basic plotting - histogram of looped Group1 values
        myData[var].hist()
        plt.title("Distribution of "+ var)
        count+=1
    if flag=='wholeData':
        plt.savefig('../picture/histogram/Distribution_Sentiment(whole).png')
    elif flag=='subData':
        time = myData['tweet_timestamp'].values
        datetime = time[0]
        name='../picture/histogram/Distribution_Sentiment'+datetime[:7]+'.png'
        plt.savefig(name)
    if PLOT:
        plt.show()
    print('Saved all successfully!')
    # Clear plot
    plt.clf()


def LOF(myData):
    # Local outlier Factor
    for intendity in intensity_keys:
        l = myData[intendity].values.reshape((-1, 1))
        clf = LocalOutlierFactor(n_neighbors=3)
        result=clf.fit_predict(l)
        # LOF -1 is outlier
        print(intendity,': ',Counter(result))
        print("LOF outlier scores")
        print(clf.negative_outlier_factor_)


# read each file data by month (iterate by using a variable called monthStr)
def readSubData(totalMonth):
    monthStr = '2020-01'  # starting point
    print('Start reading...')
    count = 0
    while count < totalMonth:
        print('\n',monthStr,':')
        # the directory of each sub-data file
        sub_dir = '../dataset/reshaped_sentiments_data/sentiment-'+monthStr+'.csv'
        # read this file
        myData = pd.read_csv(sub_dir, encoding="latin1")
        print('Information:')
        print(myData.describe())
        # check outlier
        LOF(myData)
        # show show the distribution of sentiment
        showHist(myData,flag,PLOT)

        # randomly choose 40000 data if the size of data this month is too large
        if len(myData)>40000:
            myData=myData.sample(n=40000, replace=True)
        bin(myData)
        K_Means(myData, PLOT)

        # go to the next month
        splitTime = datetime.datetime.strptime(monthStr, "%Y-%m")
        splitTime += relativedelta(months=+1)
        monthStr = splitTime.strftime('%Y-%m')
        count+=1
    print('Finished!')


if __name__ == '__main__':
    # Parameters
    flag = 'subData'  # 'wholeData' or 'subData'
    PLOT = True  # False (not show pictures) or True (show all pictures)
    totalMonth = 20  # total range[0,20], data file range from 2020-01 to 2021-08

    # READ DATA
    # read original data 'dataset/tweetid_userid_keyword_sentiments_emotions_United States.csv'
    if flag=='wholeData':
        myData = pd.read_csv(FILE_NAME, encoding="latin1")
        pd.set_option('display.max_columns', None)

        # Show information
        print("Data Summary using info method")
        print(myData.info())
        # Show mean,median(the row of 50%),and standard deviation etc.
        print("\nData summary using describe method (stats about each column")
        print(myData.describe())
        # check outlier data
        # LOF(myData)
        # Show the histogram of sentiment value
        showHist(myData,flag,PLOT)
    # read data by month 'dataset/reshaped_sentiments_data'
    elif flag=='subData':
        readSubData(totalMonth)
