#############################
# Use Multinomial Naive Bayes Model to classify people's willingness to vaccinate
# Hypothesis 2: The severity of the epidemic on people's willingness to vaccinate.
# Hypothesis 3: The impact of the degree of utilization of medical resources
#               on people's willingness to vaccinate.
#############################
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
import seaborn as sns
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from keras.utils.np_utils import to_categorical


# draw ROC
def draw_roc_auc(y_pred,y_test,hypothesis,title=''):
    lw = 2
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(3):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_pred[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    print("----------AUC----------")
    for i in range(3):
        print("For class {0} : AUC= {1:0.2f}".format(i,roc_auc[i]))
    plt.figure()
    colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
    for i, color in zip(range(3), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=lw,
                 label='ROC curve of class {0} (area = {1:0.2f})'
                 ''.format(i, roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC '+title+' multi-class'+'  (hypothesis '+hypothesis+')')
    plt.legend(loc="lower right")
    # plt.savefig('ROC-' + title + '.png')  # save the figure to file
    plt.show()


# Multinomial Naive Bayes on two hypotheses
def naiveBayes(xdata,ydata,hypothesis):
    # split data
    train_x, test_x, train_y, test_y = train_test_split(xdata, ydata, test_size=0.2, random_state=33)
    # Multinomial Naive Bayes Model
    modelNB=MultinomialNB()
    modelNB.fit(train_x, train_y)
    # cross validation
    scoring='accuracy'
    kfold = KFold(n_splits=10, random_state=10, shuffle=True)
    cv_results = cross_val_score(modelNB, train_x, train_y, cv=kfold,
                                 scoring=scoring)
    msg = "%f (%f)" % (cv_results.mean(), cv_results.std())
    print('After ten-fold cross validation:\n',cv_results)
    print('The mean(std) accuracy :',msg,'\n')
    # predict
    predict_y = modelNB.predict(test_x)
    # plot confusion matrix
    cm = pd.crosstab(predict_y,test_y)
    sns.heatmap(cm, annot = True, cmap = 'GnBu', fmt = 'd')
    plt.title('confusion matrix  (hypothesis '+str(hypothesis)+')')
    plt.xlabel('Real')
    plt.ylabel('Predict')
    plt.show()
    # model report
    print("the accuracy of this model on training set:{}".format(modelNB.score(train_x, train_y)))
    print("the accuracy of this model on test set:{}".format(modelNB.score(test_x, test_y)))
    names=['Class 0','Class 1','Class 2']
    print('\nModel Report:\n',metrics.classification_report(test_y, predict_y,target_names=names))
    # ROC curve
    predict_y = to_categorical(predict_y)
    test_y = to_categorical(test_y)
    draw_roc_auc(predict_y,test_y,str(hypothesis),title="Naive-Bayes")


if __name__ == '__main__':
    # load data
    myData = pd.read_csv('../dataset/labeled.csv')
    # label
    ydata = myData['willingness'].values
    ydata = pd.Categorical(ydata).codes

    # Hypothesis 2
    # The severity of the epidemic
    print("\nhypothesis 2:")
    hypothesis = 2
    # Feature
    xdata = np.stack((myData['testPositivityRatio'], myData['caseDensity'], myData['infectionRate'],
                      myData['deaths'], myData['positiveTests'], myData['negativeTests']), axis=1)
    # put into model
    naiveBayes(xdata,ydata,hypothesis)

    # Hypothesis 3
    # The degree of utilization of medical resources
    hypothesis = 3
    print("\nhypothesis 3:")
    # Feature
    xdata = np.stack((myData['hospitalBeds currentUsageCovid'], myData['icuBeds currentUsageCovid']), axis=1)
    # put into model
    naiveBayes(xdata, ydata,hypothesis)