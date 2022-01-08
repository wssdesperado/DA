import shutil
import pandas as pd
import csv
import os
import numpy as np
from sklearn.neighbors import LocalOutlierFactor


def preprocess():
    file = pd.read_csv('results.csv', engine="python")
    csv_file = open('./modified.csv', 'a', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(("state", "date", "testPositivityRatio", "caseDensity", "contactTracerCapacityRatio", "infectionRate", "infectionRateCI90", "icuCapacityRatio", "vaccinationsInitiatedRatio", "vaccinationsCompletedRatio", "cases", "deaths", "positiveTests", "negativeTests", "contactTracers", "hospitalBeds capacity", "hospitalBeds currentUsageTotal", "hospitalBeds currentUsageCovid", "icuBeds capacity", "icuBeds currentUsageTotal", "icuBeds currentUsageCovid", "newCases", "newDeaths", "vaccinesAdministeredDemographics", "vaccinationsInitiatedDemographics", "vaccinesDistributed", "vaccinationsInitiated", "vaccinationsCompleted", "vaccinesAdministered", "overall", "caseDensity", "cdcTransmissionLevel"))

    df = file.values.tolist()

    # reformat the raw data -- each attribute is written in one column
    for i in df:
        i[2] = i[2].strip('()').split(", ")
        i[3] = i[3].strip('()').split(", ")
        i[4] = i[4].strip('()').split(", ")
        for j in range(len(i[2])):
            if i[2][j] == "None":
                i[2][j] = 0
            else:
                i[2][j] = float(i[2][j])
        for k in range(len(i[3])):
            if i[3][k] == "None":
                i[3][k] = 0
            else:
                i[3][k] = float(i[3][k])
        csv_writer.writerow((i[0], i[1], i[2][0], i[2][1], i[2][2], i[2][3], i[2][4], i[2][5], i[2][6], i[2][7], i[3][0], i[3][1], i[3][2], i[3][3], i[3][4], i[3][5], i[3][6], i[3][7], i[3][8], i[3][9], i[3][10], i[3][11], i[3][12], i[3][13], i[3][14], i[3][15], i[3][16], i[3][17], i[3][18], i[4][0], i[4][1], i[5]))


def lof(neighbors=3):
    data = pd.read_csv('modified.csv')
    columns = data.columns.values.tolist()

    # calculate the LOF for every attributes except for state and date
    for column in columns:
        if column == 'state' or column == 'date':
            continue
        l = data[column].values.reshape(-1, 1)
        clf = LocalOutlierFactor(n_neighbors=neighbors)
        clf.fit_predict(l)
        print("*************** attribute: {} ***************".format(column))
        print("LOF -1 is outlier")
        print(clf.fit_predict(l))
        print("LOF outlier scores")
        print(clf.negative_outlier_factor_)


def separate_dataset():
    # separate the dataset by states
    with open("./modified.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        state = next(reader)[0]
    csv_file = open("./modified.csv", "r")
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    os.mkdir("./results/")
    file = open("./results/" + str(state) + ".csv", "a+", newline='')
    for row in csv_reader:
        if row[0] == state:
            writer = csv.writer(file)
            writer.writerow(row)
        else:
            state = row[0]
            file.close()
            file = open("./results/" + str(state) + ".csv", "a+", newline='')
            writer = csv.writer(file)
            writer.writerow(row)


def data_cleaning():
    files = ""
    for _, _, files in os.walk("./results/"):
        pass

    if not os.path.exists("./cleaned/"):
        os.mkdir("./cleaned/")

    for file in files:
        columns = []
        for i in range(1, 32):
            with open("./results/" + file, 'r+') as f:
                reader = csv.reader(f)
                temp = [row[i] for row in reader]
                columns.append(temp)

        count = 0
        for column in columns:
            if count < 1:
                column.append("mean")
                column.append("median")
                column.append("std")
                count += 1
                continue

            # replace the outliers with the mean of its two neighbors
            sum = 0
            for j in range(0, len(column)):
                column[j] = float(column[j])
                if j != len(column) - 1 and j != 0:
                    if column[j - 1] != 0 and column[j + 1] != '0' and column[j] == 0:
                        column[j] = (float(column[j - 1]) + float(column[j + 1])) / 2
                sum += float(column[j])
            mean = sum / len(column)
            column.append(mean)
            ndarray = np.array(column)
            median = np.median(ndarray)
            sd = np.std(ndarray)
            column.append(median)
            column.append(sd)

        # write the result into new files
        with open("./cleaned/" + file, 'a+', newline='') as fff:
            writer = csv.writer(fff)
            writer.writerow("s")
        data = pd.read_csv("./cleaned/" + file)
        data['date'] = columns[0]
        data['testPositivityRatio'] = columns[1]
        data['caseDensity'] = columns[2]
        data['contactTracerCapacityRatio'] = columns[3]
        data['infectionRate'] = columns[4]
        data['infectionRateCI90'] = columns[5]
        data['icuCapacityRatio'] = columns[6]
        data['vaccinationsInitiatedRatio'] = columns[7]
        data['vaccinationsCompletedRatio'] = columns[8]
        data['cases'] = columns[9]
        data['deaths'] = columns[10]
        data['positiveTests'] = columns[11]
        data['negativeTests'] = columns[12]
        data['contactTracers'] = columns[13]
        data['hospitalBeds capacity'] = columns[14]
        data['hospitalBeds currentUsageTotal'] = columns[15]
        data['hospitalBeds currentUsageCovid'] = columns[16]
        data['icuBeds capacity'] = columns[17]
        data['icuBeds currentUsageTotal'] = columns[18]
        data['icuBeds currentUsageCovid'] = columns[19]
        data['newCases'] = columns[20]
        data['newDeaths'] = columns[21]
        data['vaccinesAdministeredDemographics'] = columns[22]
        data['vaccinationsInitiatedDemographics'] = columns[23]
        data['vaccinesDistributed'] = columns[24]
        data['vaccinationsInitiated'] = columns[25]
        data['vaccinationsCompleted'] = columns[26]
        data['vaccinesAdministered'] = columns[27]
        data['overall'] = columns[28]
        data['caseDensity'] = columns[29]
        data['cdcTransmissionLevel'] = columns[30]
        data.to_csv(r"./cleaned/" + file, mode='a', index=False)

        f1 = open("./cleaned/" + file, 'r')
        f1_reader = csv.reader(f1)
        rows = [row for row in f1_reader]
        f1.close()
        if not os.path.exists("./clean/"):
            os.mkdir("./clean/")
        f2 = open("./clean/" + file, 'a+', newline='')
        f2_writer = csv.writer(f2)
        flag = 0
        for row in rows:
            if flag == 0:
                flag += 1
                continue
            del row[0]
            f2_writer.writerow(row)
        f2.close()

    shutil.rmtree("./cleaned")
