#############################
#   Mongodb_dataset
#   In this program, we clean the Mongodb_dataset, transfer different txt files into
#   one csv file, and discard some useless attribute to reduce the cost for analysis and
#   cluster. We finish some basic statistical analysis and build the histogram and correlation
#   subplot,  do the dbscan cluster for coordinate attributes, and utilize lof to detect outliers
#
#############################
import csv
import json
import numpy as np
import pandas as pd
import datetime
import re
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.neighbors import LocalOutlierFactor
from pprint import pprint
state_list =['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida',
			'Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Louisiana','Maine','Maryland','Massachusetts','Mississippi','Nevada','New Hampshire','New Jersey','New Mexico','New York',
			'North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota',
			'Tennessee','Utah','Vermont','Washington','Wisconsin','Wyoming','District of Columbia']
attributes_list = ['confirmed','deaths','confirmed_daily','deaths_daily']       # attributes needed for judgement
useful_attributes = ['population','confirmed','deaths','confirmed_daily','deaths_daily']
def missing_value(data):
    # remove the data with missing values
    for key in useful_attributes:
        if key not in data.keys():
            return 1
    return 0
def clean_and_reduce_dim():
    # clean data
    loc_dict = {}
    loc_id = 1
    bad = 0
    Mydata = []
    for state in state_list:
        f = open('../dataset/MongoDataset/'+state+'.txt','r')
        data = json.load(f)
        for temp in data:
            list = []
            # if data have missing values or invalid value remove them
            if missing_value(temp):
                bad += 1
                continue
            if temp['confirmed'] < temp['confirmed_daily'] or temp['deaths'] < temp['deaths_daily']:
                bad += 1
                continue
            flag = 0
            for x in attributes_list:
                if temp[x] < 0 : flag = 1
            if flag :
                bad += 1
                continue
            if temp['combined_name'] not in loc_dict.keys():
                # transfer combined name(county and state) into continuous integer
                loc_dict[temp['combined_name']] = loc_id
                loc_id += 1
            # transfer String date information into integer to help analysis
            # Data date start from 2020-05-01, thus, each date sub that date
            temp_d = re.search(r'\d+-\d+-\d+',temp['date'])
            d = datetime.datetime.strptime(temp_d[0], '%Y-%m-%d')- datetime.datetime.strptime('2020-05-01','%Y-%m-%d')

            list.append(loc_id - 1)
            list.append(temp['loc']['coordinates'][0])
            list.append(temp['loc']['coordinates'][1])
            for attributes in useful_attributes:
                list.append(temp[attributes])
            list.append(d.days)
            Mydata.append(list)
        f.close()
    print("number of invalid or missing values: %d \n" % bad)
    with open('../dataset/mongodb.csv', 'w') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(['loc_id','coordinate-x','coordinate-y','population','confirmed','deaths','confirmed_daily','deaths_daily','date'])
        for i in range(len(Mydata)):
            csv_write.writerow(Mydata[i])
    with open('../dataset/name.txt','w') as f:
        f.write(str(loc_dict))
        f.close()
def statistical_analysis(path):
    #  statistical analysis
    myData = pd.read_csv(path,sep=',')

    # remove restrictions for print pandas
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows',None)
    np.set_printoptions(threshold=np.inf)

    print("\nData info")
    print(myData.info())
    print("\nBasic statistical information")
    print(myData.describe())

    # Histograms
    for var in ['loc_id','population','confirmed','deaths','confirmed_daily','deaths_daily','date']:
        myData[var].hist()
        plt.title("Distribution of "+ var + " variables")
        plt.show()
        plt.clf()

    #  Correlations
    for var in ['confirmed','deaths','confirmed_daily','deaths_daily']:
        myData.plot.scatter(x='date',y=var)
        plt.show()
        plt.clf()
    myData.plot.scatter(x= 'confirmed_daily', y = 'deaths_daily')
    plt.show()
    plt.clf()
    # Cluster
    X = myData[['coordinate-x','coordinate-y']]
    pred = DBSCAN(eps=0.5, min_samples=100).fit_predict(X)
    plt.scatter(X['coordinate-x'],X['coordinate-y'] , c= pred)
    plt.show()
    plt.clf()
    # Score
    score = metrics.calinski_harabasz_score(X, pred)
    print("\n calinski_harabasz_score : ")
    print(score)
    # LOF
    for k in [5,50,100] :
        LOF(k, myData, 0.01)

def LOF(k,data,percent):
    clf = LocalOutlierFactor(n_neighbors=k, algorithm='kd_tree', contamination=percent)
    clf.fit_predict(data)
    print(clf.negative_outlier_factor_)

if __name__ == '__main__':
    clean_and_reduce_dim()
    statistical_analysis('../dataset/mongodb.csv')
