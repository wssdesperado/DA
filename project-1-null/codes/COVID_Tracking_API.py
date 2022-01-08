import requests
import json
import COVID_Tracking_API_Data as Data

FILE_TYPE = 'json'

#download data from api
def getData(url,FILE_NAME):
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    #write data into local file
    fileObject = open(FILE_NAME, "w")
    fileObject.write(response.text)
    fileObject.close()


def countTotalNull(FILE_NAME, keys):
    countNull = 0
    #read data from file
    with open(FILE_NAME) as f:
        json_data = json.load(f)
        #count the total number of NULL in data set
        for row in json_data:
            for key in keys:
                if row[key] is None: countNull = countNull + 1
        print('Total Null number:', countNull)

def countNumberError(FILE_NAME, keys):
    number_error = 0
    #read data from file
    with open(FILE_NAME) as f:
        json_data = json.load(f)
        # count the total number of negative data in data set, all number data shouldn't be negative
        for row in json_data:
                for key in keys:
                    if row[key] is not None:
                        if(row[key] != ''):
                            row[key] = int(row[key])
                            if row[key] < 0:
                                print(key,row[key])
                                number_error = number_error + 1
        print('number_error:', number_error)

#compute the percent of null number in each variable
def fraction(FILE_NAME,key):
    countNull = 0
    total_count = 0
    fraction = 0
    #read data from file
    with open(FILE_NAME) as f:
        json_data = json.load(f)
        #count the total number of NULL in data set
        for row in json_data:
            total_count = total_count + 1
            if row[key] is None: countNull = countNull + 1
        fraction = countNull/total_count
        print('total_count:', total_count)
        print('countNull:', countNull)
        print('fraction:', fraction)


def printInfo():
    print('---------------------states-------------------')
    countTotalNull('../dataset/States_Daily.json', Data.states_keys)
    countNumberError('../dataset/States_Daily.json', Data.states_numberdata_keys)
    print('----------positive--------')
    fraction('../dataset/States_Daily.json', 'positive')
    print('----------negative--------')
    fraction('../dataset/States_Daily.json', 'negative')
    print('----------hospitalizedCurrently--------')
    fraction('../dataset/States_Daily.json', 'hospitalizedCurrently')
    print('----------inIcuCurrently--------')
    fraction('../dataset/States_Daily.json', 'inIcuCurrently')
    print('----------recovered--------')
    fraction('../dataset/States_Daily.json', 'recovered')
    print('----------death--------')
    fraction('../dataset/States_Daily.json', 'death')
    print('---------------------US-------------------')
    countTotalNull('../dataset/US_Daily.json', Data.US_keys)
    countNumberError('../dataset/US_Daily.json', Data.US_numberdata_keys)
    print('----------positive--------')
    fraction('../dataset/US_Daily.json', 'positive')
    print('----------negative--------')
    fraction('../dataset/US_Daily.json', 'negative')
    print('----------hospitalizedCurrently--------')
    fraction('../dataset/US_Daily.json', 'hospitalizedCurrently')
    print('----------inIcuCurrently--------')
    fraction('../dataset/US_Daily.json', 'inIcuCurrently')
    print('----------recovered--------')
    fraction('../dataset/US_Daily.json', 'recovered')
    print('----------death--------')
    fraction('../dataset/US_Daily.json', 'death')




def main():
    #getData(Data.url1,FILE_NAME = 'States_Daily.json')
    #getData(Data.url3,FILE_NAME = 'States_Info.json')
    #getData(Data.url5, FILE_NAME='US_Daily.json')
    printInfo()
if __name__ == '__main__':
    main()