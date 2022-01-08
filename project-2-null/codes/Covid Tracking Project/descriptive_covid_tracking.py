import json
import sys
import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
#show whole line
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
np.set_printoptions(threshold=sys.maxsize)

STATES_FILE_CLEAN = '../dataset/States_Daily_clean.json'
US_FILE_CLEAN  = '../dataset/US_Daily_clean.json'
US_FILE_BIN  = '../dataset/US_Daily_bin.json'
def compute(Filename):
    json_data = pd.read_json(Filename)
    print(json_data.info())
    print(json_data.describe())




#####
# Local Outlier Factor
def LOF(k,FILENAME):
    with open(FILENAME) as f:
        json_data_states = json.load(f)
        positive_array = []
        negative_array = []
        death_array = []
        for row in json_data_states:
            positive_array.append(row['positive'])
            negative_array.append(row['negative'])
            death_array.append(row['death'])
    positive_array = np.array(positive_array)
    negative_array = np.array(negative_array)
    death_array = np.array(death_array)
    lp = positive_array.reshape((-1, 1))
    clf = LocalOutlierFactor(n_neighbors=k)
    print ("LOF -1 is outlier")
    print (clf.fit_predict(lp))
    print ("LOF outlier scores")
    print (clf.negative_outlier_factor_)
    ln = positive_array.reshape((-1, 1))
    clf = LocalOutlierFactor(n_neighbors=20)
    print("LOF -1 is outlier")
    print(clf.fit_predict(ln))
    print("LOF outlier scores")
    print(clf.negative_outlier_factor_)
    ld = positive_array.reshape((-1, 1))
    clf = LocalOutlierFactor(n_neighbors=20)
    print("LOF -1 is outlier")
    print(clf.fit_predict(ld))
    print("LOF outlier scores")
    print(clf.negative_outlier_factor_)

with open(US_FILE_CLEAN) as f:
    json_data_US = json.load(f)
    death_array = []
    i = 0
    for row in json_data_US:
            death_array.append(row['death'])
            i = i + 1
death_array = np.array(death_array)

#bin
def bin(array):
    names = range(1, 4)
    bins1 = [-1, 10000, 150000, 6000000]
    death_array = pd.cut(array, bins1, labels=names)
    death_bin = []
    json_text = []
    with open(US_FILE_CLEAN) as f:
        json_data_US = json.load(f)
        i = 0
        count_1 = 0
        count_2 = 0
        count_3 = 0
        for json_data in json_data_US:
            if (i < len(death_array)): json_data["death_bin"] = death_array[i]
            if death_array[i] == 1: count_1 = count_1 + 1
            if death_array[i] == 2: count_2 = count_2 + 2
            if death_array[i] == 3: count_3 = count_3 + 3
            i = i + 1
            json_text.append(json_data)
    with open(US_FILE_BIN, 'w') as f2:
        json.dump(json_text, f2, ensure_ascii=False)
    print(death_array)
    # Check the data to see the new column
    print("\n New column of data:")
    print(death_array[:10])
    sum = count_1 + count_2 + count_3
    print('count1:', count_1, 'percent of count1', count_1 / sum)
    print('count2:', count_2, 'percent of count2', count_2 / sum)
    print('count3:', count_3, 'percent of count3', count_3 / sum)

def main():
     compute(STATES_FILE_CLEAN)
     compute(US_FILE_CLEAN)
     bin(death_array)
     LOF(20,STATES_FILE_CLEAN)
     LOF(2,STATES_FILE_CLEAN)
     LOF(35,STATES_FILE_CLEAN)
     LOF(20, US_FILE_CLEAN)
     LOF(2, US_FILE_CLEAN)
     LOF(35, US_FILE_CLEAN)

if __name__ == '__main__':
     main()