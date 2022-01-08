#############################
# Calculate the number and proportion of tweets of each sentiment in a day
# box link: https://georgetown.app.box.com/folder/0
# The dataset this code use needs to download from box link
# Using Dataset:
# '../dataset/reshaped_sentiments_data'
# Save New data:
# ../dataset/day_emotion.csv     (the proportion of each sentiment per day)
# ../dataset/day_emotion2.csv    (the total number of each sentiment per day)
#############################

import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import csv


# Calculate the percentage of tweets of each emotion in a day
def saveEmotionCount(totalMonth,type='number'):
    # save data in a new day-emotion.csv
    field_order = ['time','anger', 'fear', 'happiness ','no specific emotion','sadness']
    if type == 'number':
        newDataDir='../dataset/day_emotion2.csv'
    elif type == 'proportion':
        newDataDir = '../dataset/day_emotion.csv'
    with open(newDataDir, 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, field_order)
        writer.writeheader()

        # READ MONTH
        # starting point
        monthStr = '2021-01'
        print('Start reading...')
        count = 0
        while count < totalMonth:
            # the first day of the next month
            stopStr = datetime.datetime.strptime(monthStr, "%Y-%m")
            stopStr += relativedelta(months=+1)

            # read each month data
            print(monthStr)
            # the directory of each sub-data file
            sub_dir = '../dataset/reshaped_sentiments_data/sentiment-'+monthStr+'.csv'
            myData = pd.read_csv(sub_dir, encoding="latin1")

            # READ DAY
            # count per day
            dayStr=monthStr+'-01'
            # start from 2021-01-15
            if monthStr == '2021-01':
                dayStr = monthStr + '-15'

            dayTime=datetime.datetime.strptime(dayStr, "%Y-%m-%d")
            while dayTime!=stopStr:
                # pick up the last column "emotion"
                tempData = myData[myData['tweet_timestamp'].str.startswith(dayStr)]
                cnt=tempData.groupby("emotion")["emotion"].count()
                length=len(tempData)
                # calculate the total number of each sentiment
                if type=='number':
                    writer.writerow(dict(zip(field_order, [dayStr, cnt["anger"] , cnt["fear"] ,
                                                           cnt["happiness"] ,
                                                           cnt["no specific emotion"] , cnt["sadness"] ])))
                # calculate the proportion of each sentiment
                elif type=='proportion':
                    writer.writerow(dict(zip(field_order, [dayStr, cnt["anger"]/length, cnt["fear"]/length,
                                                               cnt["happiness"]/length,
                                                               cnt["no specific emotion"]/length, cnt["sadness"]/length])))
                # go to the next day
                dayTime = datetime.datetime.strptime(dayStr, "%Y-%m-%d")
                dayTime =dayTime+ relativedelta(days=+1)
                dayStr = dayTime.strftime('%Y-%m-%d')
            # go to the next month
            splitTime = datetime.datetime.strptime(monthStr, "%Y-%m")
            splitTime += relativedelta(months=+1)
            monthStr = splitTime.strftime('%Y-%m')
            count+=1
    print('Finished!')


if __name__ == '__main__':
    totalMonth = 8
    # save the number of tweets dominated by each sentiment each day
    saveEmotionCount(totalMonth,type='number')
    # save the proportion of tweets dominated by each sentiment each day
    saveEmotionCount(totalMonth, type='proportion')
