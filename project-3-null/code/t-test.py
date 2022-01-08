# Load the libraries
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from collections import Counter

# Load the dataset
df = pd.read_csv("../dataset/day_emotion.csv")

# Have a look at the dataset
df.info()
#df.head()
#delete all spaces in csv headers
df.columns = df.columns.to_series().apply(lambda x: x.strip())
df1 = df["happiness"]
df2 = df["fear"]
df3 = df["anger"]
df4 = df["sadness"]

def t_test(attribute1, attribute2):
    result = stats.ttest_ind(attribute1,attribute2)
    print(result)
    #Detect variance difference
    result = stats.levene(attribute1, attribute2)
    print(result)
    #Uneven variance, T' test
    result = stats.ttest_ind(attribute1,attribute2, equal_var = False)
    print(result)
# # # Plot histogram for num
# # df2["happiness"].plot.hist()
# # df2["sadness"].plot.hist()
#
#
# import scipy.stats as stats
# stats.ttest_ind(df2.loc[df2.Gender=='0'].Writing, df2.loc[df2.Gender=='1'].Writing)
# plt.show()

def main():
    print("--------happiness with fear------------")
    t_test(df1,df2)
    print("--------happiness with anger------------")
    t_test(df1, df3)
    print("--------happiness with sadness------------")
    t_test(df1, df4)
    print("--------fear with anger------------")
    t_test(df2, df3)
    print("--------fear with sadness------------")
    t_test(df2, df4)
    print("--------anger with sadness------------")
    t_test(df3, df4)


main()