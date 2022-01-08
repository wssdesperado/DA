import os
import csv


def generate_data():
    dictionary = {}
    file_list = os.listdir('./clean')
    for file in file_list:
        print(file)
        with open('./clean/' + file, 'r', encoding='utf-8') as f:
            f_reader = csv.reader(f)
            rows = [row for row in f_reader]
        rows = rows[1:]
        rows = rows[:-3]
        for i in range(1, len(rows) - 1):
            if rows[i][26] == '0.0':
                if rows[i - 1][26] != '0.0':
                    rows[i][26] = int((float(rows[i - 1][26]) + float(rows[i + 1][26])) / 2)

        for row in rows:
            if row[0] not in dictionary.keys():
                dictionary[row[0]] = int(float(row[26]))
            else:
                dictionary[row[0]] += int(float(row[26]))

    with open('temp.csv', 'a', encoding='utf-8', newline='') as d:
        d_writer = csv.writer(d)
        for date in dictionary.keys():
            d_writer.writerow((date, dictionary[date]))

    with open('../dataset/usa_data.csv', 'a+', encoding='utf-8', newline='') as f:
        with open('temp.csv', 'r', encoding='utf-8',) as e:
            e_reader = csv.reader(e)
            rows = [row for row in e_reader]
        f_writer = csv.writer(f)
        f_writer.writerow(("date", "vaccinationsCompleted", "newIncreaseDoes"))
        for i in range(1, len(rows) - 42):
            rows[i].append(abs(int(float(rows[i][1]) - float(rows[i - 1][1]))))
            f_writer.writerow((rows[i][0], rows[i][1], rows[i][2]))

    os.remove('./temp.csv')

def main():
    generate_data()
if __name__ == '__main__':
    main()
