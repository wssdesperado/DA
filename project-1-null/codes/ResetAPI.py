import requests
state_list =['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia',
			'Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan'
			'Minnesota','Mississippi','Missouri','MontanaNebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York',
			'North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota',
			'Tennessee','Texas','Utah','Vermont','Virginia','Washington','West virginia','Wisconsin','Wyoming','District of Columbia']

def get_data():
    for state in state_list:
        url = "https://webhooks.mongodb-stitch.com/api/client/v2.0/app/covid-19-qppza/service/REST-API/incoming_webhook/us_only?state="+state+"&min_date=2020-05-01T00:00:00.000Z&max_date=2021-06-01T00:00:00.000Z"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        with open('../dataset/MongoDataset/'+state+".txt",'w') as f:
            f.write(response.text)
            f.close()
if __name__ == '__main__':
    get_data()