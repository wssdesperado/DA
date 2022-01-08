import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
from sklego.metrics import p_percent_score
from sklearn.metrics import roc_curve, auc
import warnings
def draw_roc_auc(y_pred,y_test):
    lw = 2
    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(10, 6))
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.title("ROC curve of SVM")
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Postive Rate')
    plt.ylabel('True Postive Rate')
    plt.show()

def validate_fairness(Mydata,model):
    for i in range(len(Mydata['hospitalBeds capacity'])):
        Mydata['hospitalBeds capacity'][i] = 0 if Mydata['hospitalBeds capacity'][i] <= Mydata['hospitalBeds capacity'].mean() else 1
    # transfer 'hospitalBeds capacity' feature into a binary feature
    X_train, X_test, Y_train, Y_test = train_test_split(
        Mydata[['hospitalBeds capacity', 'hospitalBeds currentUsageTotal', 'hospitalBeds currentUsageCovid']],
        Mydata.willingness,test_size=0.2, random_state=2)
    svm = model.fit(X_train, Y_train)
    print('p_percent_score:', p_percent_score(sensitive_column='hospitalBeds capacity')(svm, X_train))

def SVM(path):
    warnings.filterwarnings("ignore")
    Mydata = pd.read_csv(path)

    #transfer three classes into two classes to fit SVM
    for i in range(len(Mydata.willingness)):
        Mydata.willingness[i] = 0 if Mydata.willingness[i] <= 2 else 1

    X_train, X_test, Y_train, Y_test= train_test_split(Mydata[['hospitalBeds capacity','hospitalBeds currentUsageTotal','hospitalBeds currentUsageCovid']], Mydata.willingness,
                         test_size=0.2, random_state=2)
    C_list = [0.5, 1, 3, 5, 7, 9, 11]
    gamma_list = [0.000001,0.00001, 0.0001, 0.001, 0.1, 1, 10]
    best_C, best_gamma = 2, 1
    '''
    #This part is to find the C and gamma to get the best accuracy, we comment out this part 
    # because it takes many time to run, using this part we can know when C= 3 and gamma = 0.00001,
    # the accuracy is highest.
    
    model = []
    # find the best parameter C and gamma
    Y_pred =[]
    acc_m = []
    max_acc = best_C = best_gamma = 0
    for i in range(len(C_list)):
        model.append([])
        Y_pred.append([])
        acc_m.append([])
        for j in range(len(gamma_list)):
            model[i].append(SVC(C=C_list[i],kernel='rbf',gamma=gamma_list[j]))
            svm = model[i][j].fit(X_train, Y_train)
            # Predict
            Y_pred[i].append(svm.predict(X_test))
            acc = accuracy_score(Y_test, Y_pred[i][j])
            acc_m.append(acc)
            if acc > max_acc:
                max_acc, best_C , best_gamma = acc, i, j
    print("Accuracy of different C and gamma:")
    print(acc_m)
    print(best_C,best_gamma)
    '''
    # Build model
    model_best = SVC(C=C_list[best_C],kernel='rbf',gamma = gamma_list[best_gamma])
    validate_fairness(Mydata, model_best)
    # cross validation
    num_folds = 10
    seed = 5
    scoring = 'accuracy'
    kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=True)
    cv_results = cross_val_score(model_best, X_train, Y_train, cv=kfold,
                                 scoring=scoring)
    msg = "%s: %f (%f)" % ('SVM', cv_results.mean(), cv_results.std())
    print(msg)

    svm = model_best.fit(X_train, Y_train)
    Y_pred_best = svm.predict(X_test)
    print(accuracy_score(Y_test,Y_pred_best))
    print(confusion_matrix(Y_test, Y_pred_best))
    print('Classification result report ：\n',classification_report(Y_test,Y_pred_best))



    # draw confusion matrix
    cm = confusion_matrix(Y_test, Y_pred_best)
    plt.matshow(cm, cmap=plt.cm.Blues)
    plt.colorbar()
    for x in range(len(cm)):
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')

    # draw roc curve
    draw_roc_auc(Y_pred_best, Y_test)


def main():
    SVM('../dataset/labeled.csv')
if __name__ =='__main__':
    main()
