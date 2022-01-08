############################
# Cheatsheet for binning, clustering, and anomaly detection
#
# Data set description
# https://archive.ics.uci.edu/ml/datasets/BitcoinHeistRansomwareAddressDataset
############################


# Libraries
import numpy as np, math
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.neighbors import LocalOutlierFactor
import pylab as pl
from sklearn import decomposition
from pprint import pprint
from sklearn.metrics import silhouette_samples, silhouette_score


# Additional libraries that may be helpful
#from mpl_toolkits.mplot3d import Axes3D
#from sklearn import datasets

######
# READ DATA
# Read in data directly into pandas
myData = pd.read_csv('bitcoin_ransomware.csv' , sep=',', encoding='latin1')

print("Data Summary using info method")
print(myData.info())

print("\nData summary using describe method (stats about each column")
print(myData.describe())

# In this example, we use 3 bins
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.cut.html
names = range(1,4)  #names list from 1 to 3
# or names = [1, 2, 3]
bins1=[0, 166, 332, 500]
myData['loopedGroups'] = pd.cut(myData['looped'], bins1, labels=names)

#Check the data to see the new column
print("\n New column of data:")
print(myData[:10])

######
# BINS
# Read in data directly into pandas
# Another approach for evenly spaced ranges
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html

# Compute min and max values, then add 1 to each side.
minLooped = myData["looped"].min() - 1
maxLooped = myData["looped"].max() + 1

# Create even spaced bins using min and max
n_bin = 10 # Number of bin
step = (maxLooped - minLooped) / n_bin
bins =  np.arange(minLooped, maxLooped + step, step)

# Look at new bins. This is equi-width binning
loopedBins = np.digitize(myData['looped'], bins)

# Count the number of values in each bin
loopedBinCounts = np.bincount(loopedBins)
print("\n\nLooped Bins are: \n ", loopedBins)
print("\nLooped Bin count is ", loopedBinCounts)

# Create a new variable LoopedGroups1 that groups posts into bins, e.g. < 200, 200-400, etc.
# For this example, I use the bins created above
myData['LoopedGroups1'] = np.digitize(myData['looped'], bins)
print("\nAfter loopedGroups1 is added we have:\n", myData[:10])

# Another option to see actual bins
myData['BinRanges'] = pd.cut(myData['looped'], bins)

# Print Bin Counts in different ways
print("\n Bin Counts\n");
pprint(myData['BinRanges'].value_counts())
print(myData[1:10])

#####
# NEW VARIABLE
# Create a variable called LengthPerLooped
myData['LengthPerLooped'] = myData['length'] / myData['looped']
myData['LengthPerLooped'].hist()
plt.title("Distribution of LengthPerLooped")
# plt.show()
plt.savefig('LengthPerLooped.png')
plt.clf()
print("\n New variable added:\n")
pprint(myData[:10])

######
# PLOTS
# Basic plotting - boxplot of entire dataframe
plt.style.use = 'default'
myData.boxplot()
plt.title("Box plots of all variables in data set")
plt.xticks(rotation=345)
# plt.show()
plt.savefig('boxPlot.png')
plt.clf()

# Basic plotting - histogram of entire dataframe
# Visualize basic stats & print plot to a file
print (myData)
myData.hist()
plt.title("Distribution of different variables")
# plt.show()
plt.savefig('dataHistogram.png')
plt.clf()

# Basic plotting - histogram of looped Group1 values
myData['LoopedGroups1'].hist()
plt.title("Distribution of Looped")
# plt.show()
plt.savefig('LoopedDistribution.png')
plt.clf()

# Subplots of histograms for different columns
# The following will create a collection of subplots
# that are histograms for each variable by looped group
VariableList=["looped", "length", "count"]
#print(VariableList)

for var in VariableList:  
    name="Week4_5ICA_Graph_for_"+var
    myData[var].hist(by=myData['LoopedGroups1'])
    pl.suptitle("Histograms by Looped Group for " + var)
    plt.savefig(name)
    plt.clf()
    plt.close()

#####
# PLOT CORRELATED DATA
# Plot the distribution of the length for the looped categories created.

# Get unique looped groups. Iterate through list and plot each histogram
loopedSeries = myData['LoopedGroups1'].unique()
loopedSeries.sort()

# Iterate through each looped series and generate the plot
counter = 1
for looped in loopedSeries:
    pprint(looped)
    
    # We need to select rows containing a particular looped
    queryString = "LoopedGroups1 == " + str(looped)
    loopedGroupLength = myData[['LoopedGroups1', 'length']].query(queryString)
    
    # Create histogram and label it
    loopedGroupLength['length'].hist()
    titleLabel = "Distribution of length for Looped Group " + str(looped)
    plt.title(titleLabel)
    plt.xlabel("length")
    plt.ylabel("Frequency")
    
    # Write to file
    fileName = 'looped' + str(counter) + '.png'
    plt.savefig(fileName)
    
    # Clear plot
    plt.clf()
    counter += 1

#####
# KMEANS
# Use k-means clustering on the data.

# Count missing values
nullCount = myData.isnull().values.ravel().sum()
print("\nNull Count:\n");
pprint(nullCount)

# Remove missing data (we do not have any, but still showing)
myData.dropna()
pprint(len(myData.index))

### Note - make sure that your data has only numerical values for kmeans
# If it has strings - not permitted by fit_transform()
myData['ransomware_type'] = pd.Categorical(myData['ransomware_type'])
myData['ransomware_type'] = myData['ransomware_type'].cat.codes
pprint(myData[:10])

## Fix MyData
# print(myData)
myData=pd.concat([myData['looped'], myData['length'], myData['count'], myData['LoopedGroups1'], myData['LengthPerLooped']],
                 axis=1, keys=['looped', 'length', 'count', 'LoopedGroups1','LengthPerLooped'])
x = myData.values # returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
normalizedDataFrame = pd.DataFrame(x_scaled)
pprint(normalizedDataFrame[:10])

# Create clusters (If you try 3 and then 20, you will see how different
# it looks when you attempt to fit the data.
k = 5
kmeans = KMeans(n_clusters=k)
cluster_labels = kmeans.fit_predict(normalizedDataFrame)

# Determine if the clustering is good
silhouette_avg = silhouette_score(normalizedDataFrame, cluster_labels)
print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)

centroids = kmeans.cluster_centers_
pprint(cluster_labels)
pprint(centroids)

#pprint(prediction)

# See how it fits data on different dimensions
print(pd.crosstab(cluster_labels, myData['looped']))
print(pd.crosstab(cluster_labels, myData['length']))
print(pd.crosstab(cluster_labels, myData['count']))

#####
# PCA
# Let's convert our high dimensional data to 2 dimensions
# using PCA
pca2D = decomposition.PCA(2)

# Turn the data into two columns with PCA
pca2D = pca2D.fit(normalizedDataFrame)
plot_columns = pca2D.transform(normalizedDataFrame)

# This shows how good the PCA performs on this dataset
print(pca2D.explained_variance_)

# Plot using a scatter plot and shade by cluster label
plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels)
plt.title("2-dimensional scatter plot using PCA")

# Write to file
plt.savefig("pca2D.png")

# Clear plot
plt.clf()

silhouette_avg = silhouette_score(plot_columns, cluster_labels)
print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)

#####
# Local Outlier Factor
l = myData['LengthPerLooped'].values.reshape((-1, 1))
clf = LocalOutlierFactor(n_neighbors=2)
print ("LOF -1 is outlier")
print (clf.fit_predict(l))
print ("LOF outlier scores")
print (clf.negative_outlier_factor_)

