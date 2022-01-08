# COSC-587-P2

Added some cheatsheets for you to use.

### COVID_ACT_NOW_API

The codes are under "./codes/covid_act_now_api"

##### files
* covid_act_now_p2.py: the main function
* preprocess.py: functions to preprocess the raw dataset
* results.csv: the result from project one, has to be under the same path with the other two python files

##### outputs
* modified.csv: the preprocessed dataset of project 1
* clean/: the subsets of the dataset separated by states
* GMM_result.png: the result of GMM clustering result
* console: the result of LOF, the average score of clusters using Silhouette

##### about the code
* the neighbor of LOF is set to 3
* the components of GMM is set to 4
* "results.csv" is required

##### how to run
**python3 covid_act_now_p2.py**

### Process_for_mongodb.py

 The code will clean the data from /dataset/MongoDataset/ which is the data we collected in project 1. 
 It will generate a new CSV file called mongodb.csv as a new cleaned data in ./dataset/. All the rest part such as 
 histogram, cluster runs Process_for_mongodb.py
 
 ##### files
* Process_for_mongodb.py: the main function
* all the txt files in ./dataset/MongoDataset/

##### outputs 
* mongodb.csv : the preprocessed dataset of project 1
* Console : 
  * histograms and correlation : the program will print the histograms and correlations for mongodb dataset(which also show in the report)
  * Score: the result of LOF, the average score of clusters using Calinski Harabasz Score
  * Cluster : the result of DBSCAN clustering 
 
##### about the code
* the neighbor of LOF is set to 5, 50 , 100
* the eps of DBSCAN is set to 0.5, min_samples = 100 
* all the txt files in ./dataset/MongoDataset/ is required

##### how to run
**python3 Process_for_mongodb.py**

### LDA.py

The code will use LDA method to process States_info.json

 ##### files
* LDA.py: the main function
* States_info.json: textual data

##### outputs 
* ./dataset/LDA_resulsts.csv : the most relevant topic for each documents
* console:
  * Topics : each topic's key words
  * coherence score : the score of the result of LDA
  * distribution : distribution of each topic  

##### about the code
* num_topics = 5

##### how to run
**python3 LDA.py**
 
### Covid_Tracking_Project_API
*Please first unzip 'States_Daily.json.zip' in dataset folder, because this file is too large so I can't upload it.
* All py files are in Covid Tracking Project folder
* Please run the file by the sequence: preprocessing_covid_tracking.py, descriptive_covid_tracking.py then hierarchical _cluster.py.
*  preprocessing_covid_tracking.py contains the data clean of States_Daily.json and US_Daily.json, it generated two files States_Daily_clean.json and US_Daily_clean.json
*  descriptive_covid_tracking.py contains basic statistical analysis ,LOF and bin.
*  hierarchical_cluster.py contains hierarchical_cluster and k-means(which has been annotated because it not perform well)

### reprocessing_sentiment.py
* Find whether there is a null value in the complete data set. Since there is no missing data in the data set, there is no other processing of the null value. 
* Delete those rows in the data whose sentiment value is out of range. 
* Divide the original entire data by month and get 20 relatively small data sets.

You can obtain the original data through the box link : https://georgetown.app.box.com/folder/0. 

Download the 'tweetid_userid_keyword_sentiments_emotions_United States.zip'

Unzip before running the code

Put them into ../dataset/tweetid_userid_keyword_sentiments_emotions_United States.csv

##### Suggestion: 
Due to the extremely long running time of the deleted part, we spent more than 30 hours running theis code to clean up and divide the entire original data set. Therefore, we do not recommend you to obtain divided data by running this code. 
No new variables are added to this dataset, just divided them into 20 small parts. Data download from this box link is the same as the result you run this code.

##### how to run
**python3 reprocessing_sentiment.py**


### descriptive_sentiment.py
This code will read the monthly data in a loop, if you feel the running time is too long, you can choose to reduce the amount of data according to the parameter recommendations 

* show information of data (mean,median,std,etc.)
* Use LOF to check outlier data
* show histogram of sentiment value
* Binning strategy
* k-mean sclustering and PCA

Download the 'tweetid_userid_keyword_sentiments_emotions_United States.zip' and 'reshaped_sentiments_data.zip' from box link: https://georgetown.app.box.com/folder/0. 

Unzip before running the code

put 'reshaped_sentiments_data.zip' into ../dataset/reshaped_sentiments_data/*

##### how to run
**python3 descriptive_sentiment.py**

##### parameter recommendations:
* You can change the parameters at the top of the main (code line 184-186)
Flag=’wholeData’   run the original dataset 
Flag=’subData’   run data by month
* If you feel there are too many pictures shown while running this code, change PLOT=False
* If you just want to see the result in one month (look roughly at what the code does), change  Flag=’subData’ and totalMonth=1 (or the number you want, up to 20)
