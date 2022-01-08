#############################
# Clean and Split ‘tweetid_userid_keyword_sentiments_emotions_United States.csv’
# box link: https://georgetown.app.box.com/folder/0  (The dataset this code use needs to download from box link )
# Remove the rows of data whose values of sentiment is out of range
# Divide the whole dataset by months
#############################

from tweet_data import *
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


# Delete some rows of data whose sentiment attributes are out of range[0,1]
def removeOutOfRange(myData):
    print('original shape:', myData.shape)
    len = myData.shape[0]
    print('Start to delete data...')
    for key in intensity_keys:
        print('Searching ', key)
        indexList = myData[(myData[key] < 0.)].index.tolist()
        indexList += myData[(myData[key] > 1.)].index.tolist()
        print(indexList) # print the index of rows we need to remove
        for index in indexList:
            myData.drop(index=[index], inplace=True)
            print(index) # print the index of row we have removed
    print('Finished! Shape after deletion:', myData.shape)


# Divide the whole dataset by months
def splitData(myData,splitFlag,totalMonth):
    splitFlag = '2020-01'  # starting point
    totalMonth = 20  # 2020-01 to 2021-08
    print('Start splitting...')
    count = 0
    while count < totalMonth:
        # split data by month and save them in a new folder
        print(splitFlag)
        tempData = myData[myData['tweet_timestamp'].str.startswith(splitFlag)]
        fileName = '../dataset/reshaped_sentiments_data/sentiment-' + splitFlag + '.csv'
        tempData.to_csv(fileName)
        count += 1
        # transfer splitFlag into timestamp
        splitTime = datetime.datetime.strptime(splitFlag, "%Y-%m")
        # add one month
        splitTime += relativedelta(months=+1)
        # new splitFlag
        splitFlag = splitTime.strftime('%Y-%m')
    print('Splitting finished!')


if __name__ == '__main__':
    # Load data
    myData = pd.read_csv(FILE_NAME, encoding="latin1")
    # Show information
    print("Data Summary using info method")
    print(myData.info())

    # Count missing values (This data has no missing values)
    nullCount = myData.isnull().values.ravel().sum()
    print("Null Count:", nullCount)

    # Delete some rows of data whose sentiment attributes are out of the range[0,1]
    removeOutOfRange(myData)

    # Divide myData by month
    splitFlag = '2020-01'  # starting point
    totalMonth = 20  # 2020-01 to 2021-08
    splitData(myData,splitFlag,totalMonth)


