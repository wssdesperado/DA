import csv
import pandas as pd
import numpy as np
from pandas import DataFrame
import sys


def main():
    # show all columns
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    np.set_printoptions(threshold=sys.maxsize)
    # this ration is accumaulate
    vaccinationsRatio = []
    with open('./modified.csv', 'r', encoding='utf-8') as f:
        f_reader = csv.reader(f)
        rows = [row for row in f_reader]

        result = []
        count = 0
        for row in rows:
            if count == 0:
                result.append(row)
            if (count > 0):
                if (row[8] != '0' and row[8] != '0.0'):
                    result.append(row)
                    vaccinationsRatio.append(float(row[8]))
            count = 1
    vaccinationsRatio = np.array(vaccinationsRatio)
    vaccination = [(vaccinationsRatio[i + 1] - vaccinationsRatio[i]) for i in range(len(vaccinationsRatio) - 1)]
    vaccination = [(i > 0) * i for i in vaccination]
    df = DataFrame(vaccination)

    # bin
    names = range(1, 4)
    bins = [-1, 0.001, 0.0023, 0.068]
    label = pd.cut(vaccination, bins, labels=names)
    label = list(label)

    with open('./labeled.csv', 'a+', encoding='utf-8', newline='') as d:
        d_writer = csv.writer(d)
        i = 0
        result[0].append('willingness')
        d_writer.writerow(result[0])
        for row in result[1:-2]:
            row.append(label[i])
            i += 1
            d_writer.writerow(row)


if __name__ == '__main__':
    main()
