import pandas as pd
from sklearn import neighbors
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.metrics import roc_curve,auc
from itertools import cycle
from sklearn.preprocessing import label_binarize
import seaborn as sns
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklego.metrics import equal_opportunity_score
import types
#parameters
num_folds = 10
seed = 5

#load data
df = pd.read_csv("../dataset/labeled.csv")
data = df[["testPositivityRatio","deaths","positiveTests","negativeTests","newDeaths"]]
target = df["willingness"]
print(data)
# #count label ratio
# count1 = 0
# count2 = 0
# count3 = 0
# for e in target:
#     if(e == 1):count1 = count1 + 1
#     if (e == 2): count2 = count2 + 1
#     if (e == 3): count3 = count3 + 1
# count = count1 + count2 + count3
# print(count1,count1/count)
# print(count2,count2/count)
# print(count3,count3/count)
# print(count)


#build model
models = []
models.append(('KNN', neighbors.KNeighborsClassifier()))
results = []
names = []
scoring = 'accuracy'
X_train, X_test, Y_train, Y_test = train_test_split(data, target, test_size=0.2)

def kfold(X_train, X_test, Y_train, Y_test):
    #kfold seperate data
    for name, model in models:
        kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=True)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold,
    scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)

    knn = neighbors.KNeighborsClassifier()
    knn.fit(X_train, Y_train)
    knn_predictions = knn.predict(X_test)
    print()
    print(accuracy_score(Y_test, knn_predictions))
    print(confusion_matrix(Y_test, knn_predictions))
    print(classification_report(Y_test, knn_predictions))


    y_pred = knn.predict(X_test)
    #confusion matrix
    cm = pd.crosstab(y_pred,Y_test)
    sns.heatmap(cm, annot = True, cmap = 'GnBu', fmt = 'd')
    plt.xlabel('Real')
    plt.ylabel('Predict')
    plt.show()
    return y_pred

#roc
def draw_roc_auc(y_pred,y_test):
    lw = 2
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(3):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_pred[:, i])
        # print(y_test[:, i])
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
    plt.title('ROC KNN multi-class')
    plt.legend(loc="lower right")
    # plt.savefig('ROC-' + title + '.png')  # save the figure to file
    plt.show()


def main():
    y_pred = kfold(X_train, X_test, Y_train, Y_test)
    y_pred = label_binarize(y_pred, classes=[1, 2, 3])
    test_y = label_binarize(Y_test, classes=[1, 2, 3])
    draw_roc_auc(y_pred, test_y)

main()





