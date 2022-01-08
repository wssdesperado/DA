#States_Daily.json
#recovered is all null, so delete this attribute
import json
import math


STATES_FILE = '../dataset/States_Daily.json'
US_FILE = '../dataset/US_Daily.json'
STATES_FILE_CLEAN = '../dataset/States_Daily_clean.json'
US_FILE_CLEAN  = '../dataset/US_Daily_clean.json'
#_____________________________________________________________________________________________________#
# 'recovered' is all null, so delete this attribute
# 'checkTimeEt' ,'commercialScore', 'dateChecked', 'dateModified', 'grade', 'hash', 'hospitalized' ,
# 'negativeIncrease', 'negativeRegularScore', 'negativeScore', 'posNeg', 'positiveScore', 'total'
# have been deprecated by the website
#_____________________________________________________________________________________________________#
keys_del_states = ['recovered', 'pending', 'checkTimeEt' ,'commercialScore', 'dateChecked', 'dateModified',
       'grade', 'hash','hospitalized', 'negativeIncrease', 'negativeRegularScore', 'negativeScore',
       'posNeg', 'positiveScore', 'total', 'lastUpdateEt', 'positiveCasesViral','deathProbable',
        'totalTestEncountersViral', 'totalTestsPeopleViral','positiveTestsAntibody','negativeTestsAntibody',
        'totalTestsAntibody','positiveTestsPeopleAntibody', 'negativeTestsPeopleAntibody', 'positiveTestsPeopleAntigen',
        'totalTestsAntigen', 'positiveTestsAntigen','fips', 'dataQualityGrade','score', 'probableCases',
        'hospitalizedCumulative', 'inIcuCurrently', 'inIcuCumulative', 'onVentilatorCurrently','onVentilatorCumulative','hospitalizedDischarged',
        'deathConfirmed', 'totalTestsPeopleAntibody', 'totalTestsPeopleAntigen', 'positiveTestsViral','negativeTestsViral']
keys_del_US = ['recovered', 'dateChecked', 'hospitalized', 'lastModified', 'posNeg','total','hash']

with open(STATES_FILE) as f:
    json_data_states = json.load(f)
with open(US_FILE) as f:
    json_data_US = json.load(f)
#compute the value of null attribute equals mean of its left two and right two values
def compute_null(FILE_NAME,attribute,json_data):
    i = 0
    left = 0
    right = 0
    while(i < len(json_data)):
        if(json_data[i][attribute] is None):
            sum = 0
            if(i > 0):left = i - 1
            countleft = 0
            if(i < len(json_data)-1):right = i + 1
            countright = 0
            while(countleft < 2):
                if(json_data[left][attribute] is not None):sum = sum + json_data[left][attribute];countleft = countleft + 1
                else:
                    if(left > 0):left = left - 1
                    else:break
            while (countright< 2):
                if (json_data[right][attribute] is not None):
                    sum = sum + json_data[right][attribute];countright = countright + 1
                else:
                    if (right < len(json_data)-1): right = right + 1;
                    else:break
            json_data[i][attribute] = math.floor(sum/(countleft + countright))
        i = i + 1
    return json_data

def data_clean(json_data_states,json_data_US,STATES_FILE,US_FILE,STATES_FILE_OUTPUT,US_FILE_OUTPUT):
    #delete the attribute we don't need or deprecated by the website or percent of null large than 0.4
    for row in json_data_states:
        for key in keys_del_states:
            del row[key]
    for row in json_data_US:
        for key in keys_del_US:
            del row[key]
    json_data_states = compute_null(STATES_FILE,'positive', json_data_states)
    json_data_states = compute_null(STATES_FILE,'negative', json_data_states)
    json_data_states = compute_null(STATES_FILE,'totalTestResults', json_data_states)
    json_data_states = compute_null(STATES_FILE,'hospitalizedCurrently', json_data_states)
    json_data_states = compute_null(STATES_FILE,'death', json_data_states)
    json_data_states = compute_null(STATES_FILE,'totalTestsViral', json_data_states)
    json_data_US = compute_null(US_FILE,'positive', json_data_US)
    json_data_US = compute_null(US_FILE,'negative', json_data_US)
    json_data_US = compute_null(US_FILE,'pending', json_data_US)
    json_data_US = compute_null(US_FILE,'totalTestResults', json_data_US)
    json_data_US = compute_null(US_FILE,'hospitalizedCurrently', json_data_US)
    json_data_US = compute_null(US_FILE,'hospitalizedCumulative', json_data_US)
    json_data_US = compute_null(US_FILE,'inIcuCurrently', json_data_US)
    json_data_US = compute_null(US_FILE,'inIcuCumulative', json_data_US)
    json_data_US = compute_null(US_FILE,'onVentilatorCurrently', json_data_US)
    json_data_US = compute_null(US_FILE,'onVentilatorCumulative', json_data_US)
    json_data_US = compute_null(US_FILE,'death', json_data_US)

    #write data after clean into file
    with open(STATES_FILE_OUTPUT,'w') as f:
        json.dump(json_data_states,f)
    with open(US_FILE_OUTPUT,'w') as f:
        json.dump(json_data_US,f)

def main():
    data_clean(json_data_states, json_data_US, STATES_FILE, US_FILE, STATES_FILE_CLEAN, US_FILE_CLEAN)

if __name__ == '__main__':
    main()


