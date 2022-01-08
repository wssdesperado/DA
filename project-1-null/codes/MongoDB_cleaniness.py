import json
state_list =['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida',
			'Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Louisiana','Maine','Maryland','Massachusetts','Mississippi','Nevada','New Hampshire','New Jersey','New Mexico','New York',
			'North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota',
			'Tennessee','Utah','Vermont','Washington','Wisconsin','Wyoming','District of Columbia']
attributes_list = ['confirmed','deaths','confirmed_daily','deaths_daily']       # attributes needed for judgement
filename = ['MongoDB_1','MongoDB_2','MongoDB_3']
def clean():
    dict = {}
    for i in attributes_list:
        dict[i] = 0
    dict['total'] = 0
    for state in state_list:
        f = open('../dataset/MongoDataset/'+state+'.txt','r')
        w = open('../dataset/cleaned_data.txt','a')
        data = json.load(f)
        for temp in data:
            flag = 0
            dict['total'] += 1
            if temp['confirmed'] < temp['confirmed_daily']: # judge whether the information is valid
                dict['confirmed'] += 1
                dict['confirmed_daily'] += 1
                continue
            if temp['deaths'] < temp['deaths_daily']:
                dict['deaths'] += 1
                dict['death_daily'] += 1
                continue
            for attributes in attributes_list:
                if temp[attributes] < 0 :
                    dict[attributes] += 1
                    flag = 1
                    break
            if flag :                                       # use flag to remove invalid information
                continue
            json.dump(temp,w)

    print(dict)
    f.close()
    w.close()
if __name__ == '__main__':
        clean()