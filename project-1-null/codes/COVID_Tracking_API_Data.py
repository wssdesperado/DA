#define urls
url1 = "https://covidtracking.com/api/states/daily"      #States_Daily
url2 = "https://covidtracking.com/api/states"            #States_Current
url3 = "https://covidtracking.com/api/states/info"       #States_Info
url4 = "http://covidtracking.com/api/us"                 #US_Current
url5 = "https://covidtracking.com/api/us/daily"          #US_Daily

states_keys = ['date', 'state', 'positive', 'probableCases', 'negative', 'pending', 'totalTestResultsSource',
        'hospitalizedCurrently', 'hospitalizedCumulative', 'inIcuCurrently', 'hospitalizedCumulative',
        'inIcuCurrently', 'inIcuCumulative','onVentilatorCurrently', 'onVentilatorCumulative', 'recovered',
        'lastUpdateEt', 'dateModified','checkTimeEt','death', 'hospitalized', 'hospitalizedDischarged',
        'dateChecked', 'totalTestsViral','positiveTestsViral', 'negativeTestsViral','deathConfirmed',
        'deathProbable', 'totalTestEncountersViral', 'totalTestsPeopleViral', 'totalTestsAntibody',
         'totalTestsPeopleAntibody','positiveTestsPeopleAntibody','negativeTestsPeopleAntibody',
        'totalTestsPeopleAntigen', 'positiveTestsPeopleAntigen', 'totalTestsAntigen', 'positiveTestsAntigen', 'fips',
        'positiveIncrease','negativeIncrease', 'total', 'totalTestResultsIncrease', 'posNeg', 'dataQualityGrade',
        'deathIncrease', 'hospitalizedIncrease', 'hash', 'commercialScore','negativeRegularScore',
        'negativeScore', 'positiveScore', 'score', 'grade']
states_numberdata_keys = ['positive','probableCases','negative','pending','totalTestResults','hospitalizedCurrently',
                   'hospitalizedCumulative','inIcuCurrently','inIcuCumulative','onVentilatorCurrently','onVentilatorCumulative',
                   'recovered','death','hospitalized','hospitalizedDischarged','totalTestsViral','positiveTestsViral',
                   'negativeTestsViral','deathConfirmed','deathProbable','totalTestEncountersViral','totalTestsPeopleViral',
                   'totalTestsAntibody','totalTestsPeopleAntibody','positiveTestsPeopleAntibody','negativeTestsPeopleAntibody',
                   'totalTestsPeopleAntigen','positiveTestsPeopleAntigen','totalTestsAntigen','positiveTestsAntigen',
                   'fips','total','posNeg','negativeRegularScore','negativeScore','positiveScore','score','grade']
US_keys = ['date', 'states', 'positive', 'negative', 'pending',
        'hospitalizedCurrently', 'hospitalizedCumulative', 'inIcuCurrently', 'hospitalizedCumulative',
        'inIcuCurrently', 'inIcuCumulative','onVentilatorCurrently', 'onVentilatorCumulative', 'dateChecked',
        'death',  'hospitalized', 'totalTestResults','lastModified', 'recovered','total', 'posNeg','deathIncrease',
        'hospitalizedIncrease', 'negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease',
         'hash']
US_numberdata_keys = ['date', 'states', 'positive', 'negative', 'pending',
        'hospitalizedCurrently', 'hospitalizedCumulative', 'inIcuCurrently', 'hospitalizedCumulative',
        'inIcuCurrently', 'inIcuCumulative','onVentilatorCurrently', 'onVentilatorCumulative',
        'death',  'hospitalized', 'totalTestResults','recovered','total', 'posNeg','deathIncrease',
        'hospitalizedIncrease', 'negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease',
         ]