# project-3-null

## guidence
* library :Numpy, Pandas, sklearn, sklego, matplotlib
* order: run addlabel.py,generate_usa_data.py, saveEmotionCount.py first to get needed dataset, then run others.

## addlabel.py
add a new attribute by calculating the variation of vaccinated ratio
* has to be under the same path with modified.csv
* **output:** labeled.csv
## decision_tree_and_random_forest.py
implement decision tree model and random forest model
* has to be under the same path with labeled.csv
* **output:** precision, ROC curve, confusion metrics and cross validation of decision tree and random forest

## generate_usa_data.py
generate dataset used for regression
* **output:**
../dataset/usa_data.csv     

## saveEmotionCount.py
calculated the number and proportion of tweets dominated by each sentiment each day and saved them in units of days
* **dataset:**

data comes from '../dataset/reshaped_sentiments_data', and needs to be downloaded from box link

box link: https://georgetown.app.box.com/folder/0

download 'reshaped_sentiments_data.zip', and unzip before running the code

* **output:**  two new data

../dataset/day_emotion.csv     (the proportion of each sentiment per day)

../dataset/day_emotion2.csv    (the total number of each sentiment per day)

## Regression.py
linear regression
* **dataset:** data comes from '../dataset/data_emotion2.csv' and '../dataset/usa_data.csv'
* **output:**  Regression line and coefficient of each attributes.

## SVM.py
implement SVM model
* **dataset:** data comes from '../dataset/labeled.csv'
* **output:**  P score of SVM, precision, recall, f1-score, ROC curve, confusion metrics and the accuracy of ten-fold cross validation using SVM model

## naive Bayes.py
a three-category Multinomial Naive Bayes model to divide the data into three levels of vaccination willingness.
features are chosen based on the hypothesis(2) of the severity of the epidemic and the hypothesis(3) of the utilization of medical resources.
* **dataset:** data comes from '../dataset/labeled.csv'
* **output:**  precision, recall, f1-score, ROC curve, confusion metrics and the accuracy of ten-fold cross validation using Multinomial Naive Bayes model
 

## t-test.py
use t test and t' test to test four emotions by pairs
* **dataset:** data comes from '../dataset/day_emotion.csv'
* **output:**  statistic, pvalue

## knn.py
implement knn model to test hypothesis 2
* **dataset:** data comes from '../dataset/labeled.csv'
* **output:**  precision, recall, f1-score, ROC curve, confusion metrics and the accuracy of ten-fold cross validation using knn model
 
