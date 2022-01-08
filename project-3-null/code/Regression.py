import csv
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
def combine_data(path1,path2,path):
    # combine emotion data and vaccination information
    Emotion = pd.read_csv(path1,sep=',')
    Increases = pd.read_csv(path2,sep=',')
    with open(path, 'w') as f:
        temp = 0
        csv_write = csv.writer(f)
        csv_write.writerow(['changes','anger','fear','happiness','no specific emotion','sadness'])
        for i in range(len(Emotion)):
            for j in range(len(Increases)):
                if Increases['date'][j] == Emotion['time'][i] :
                    # use time attribute as a key
                    data = [Increases['newIncreaseDoes'][j]-temp,Emotion['anger'][i],Emotion['fear'][i],Emotion['happiness '][i],Emotion['no specific emotion'][i],Emotion['sadness'][i]]
                    temp = Increases['newIncreaseDoes'][j]
                    csv_write.writerow(data)
def regression(path):
    Mydata = pd.read_csv(path,sep=',')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows',None)
    np.set_printoptions(threshold=np.inf)
    print(Mydata.describe())

    # model
    model = LinearRegression()

    # transfer data into dataframe
    Data = DataFrame(Mydata)

    # split data into train and test data
    X_train, X_test, Y_train, Y_test = train_test_split(Data.values[:, 1:], Data.changes, train_size=0.8,
                                                        test_size=0.2)
    # Training
    model.fit(X_train, Y_train)

    a = model.intercept_
    b = model.coef_

    print("Regression line : Y = ", round(a, 2), "+", round(b[0], 2), "* anger + ", round(b[1], 2), "* fear + ",
          round(b[2], 2), "* happiness + ",round(b[2], 2), "* no specific + ",round(b[3], 2),'*sadness')
    # predict
    Y_pred = model.predict(X_test)
    # show predication
    plt.plot(range(len(Y_pred)), Y_pred, 'red', linewidth=2.5, label="predict data")
    # show test data
    plt.plot(range(len(Y_test)), Y_test, 'green', label="test data")
    # attribute
    plt.xlabel('X_value')
    plt.ylabel('Number of changes')
    plt.legend(loc=2)
    plt.show()

def main():
    combine_data('../dataset/day_emotion2.csv','../dataset/usa_data.csv','../dataset/Emotion-Vaccine.csv')
    regression('../dataset/Emotion-Vaccine.csv')
if __name__ == '__main__':
    main()