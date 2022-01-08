from itertools import cycle
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import label_binarize
from sklearn.tree import DecisionTreeClassifier


def draw_roc_auc(y_pred, y_test, title=''):
    lw = 2
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(3):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_pred[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    print("----------AUC----------")
    for i in range(3):
        print("For class {0} : AUC= {1:0.2f}".format(i, roc_auc[i]))
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
    plt.title('ROC-' + title + '-multi-class')
    plt.legend(loc="lower right")
    plt.show()


def main():
    data = pd.read_csv('./labeled.csv')
    target = data['willingness'].values
    data.drop(['state'], axis=1, inplace=True)
    data.drop(['date'], axis=1, inplace=True)
    data.drop(['willingness'], axis=1, inplace=True)

    # train decision tree
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3)
    clf = DecisionTreeClassifier()
    clf.fit(x_train, y_train)
    predict_target = clf.predict(x_test)

    # train random forest
    clff = RandomForestClassifier()
    clff.fit(x_train, y_train)
    p_t = clff.predict(x_test)

    print(sum(predict_target == y_test))

    print(metrics.classification_report(y_test, predict_target))
    print(metrics.classification_report(y_test, p_t))

    # test data
    X = x_test
    l1 = [n[17] for n in X.values]
    l2 = [n[9] for n in X.values]
    plt.scatter(l1, l2, c=predict_target)
    plt.title('DecisionTree')
    plt.show()

    X = x_test
    l1 = [n[17] for n in X.values]
    l2 = [n[9] for n in X.values]
    plt.scatter(l1, l2, c=p_t)
    plt.title('RandomForest')
    plt.show()

    # confusion matrix
    cm = pd.crosstab(predict_target, y_test)
    sns.heatmap(cm, annot=True, cmap='GnBu', fmt='d')
    plt.xlabel('Real')
    plt.ylabel('Predict')
    plt.show()

    cmm = pd.crosstab(p_t, y_test)
    sns.heatmap(cmm, annot=True, cmap='GnBu', fmt='d')
    plt.xlabel('Real')
    plt.ylabel('Predict')
    plt.show()

    # cross validation
    clf_s = cross_val_score(clf, data, target, cv=10)
    clff_s = cross_val_score(clff, data, target, cv=10)

    plt.plot(range(1, 11), clff_s, label="RandomForest")
    plt.plot(range(1, 11), clf_s, label="Decision Tree")
    plt.legend()
    plt.show()

    # ROC
    predict_target = label_binarize(predict_target, classes=[1, 2, 3])
    y_test = label_binarize(y_test, classes=[1, 2, 3])
    draw_roc_auc(predict_target, y_test, title='decisionTree')

    p_t = label_binarize(p_t, classes=[1, 2, 3])
    draw_roc_auc(p_t, y_test, title='RandomForest')


if __name__ == '__main__':
    main()
