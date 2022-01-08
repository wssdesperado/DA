#############################
# Check the level of cleanliness of the Twitter-COVID-dataset
#
# Version 1
#############################
import csv
from tweet_data import *

# count invalid number of each attributes
info_invalid = 0
intensity_out_range = 0
keyword_invalid = 0
sentiment_invalid = 0
emotion_invalid = 0


# print the invalid numbers of attributes
def show_invalid_result():
    print("--------NUMBER OF INVALID VALUES--------")
    print("User Info:", info_invalid, "   Intensity:", intensity_out_range, "   Keyword:",
          keyword_invalid, "   Sentiment:", sentiment_invalid, "   Emotion:", emotion_invalid)


def main():
    with open(FILE_NAME) as f:
        # read data
        df = csv.DictReader(f)
        # data line count
        line = 1
        # save the invalid number of attributes
        global info_invalid,intensity_out_range,keyword_invalid,sentiment_invalid,emotion_invalid
        # read each row of data
        print("--------Data processing--------")
        print("number of processed data:")
        for row in df:
            for key in other_keys:
                # check if user information contains invalid value
                if row[key] == '' or row[key] is None:
                    info_invalid = info_invalid + 1
            for key in intensity_keys:
                # check if intensity is ' ' or out of range [0,1]
                if row[key] == ' ':
                    intensity_out_range = intensity_out_range + 1
                else:
                    temp = float(row[key])
                    if temp < 0. or temp > 1.:
                        intensity_out_range = intensity_out_range + 1
            if not (row[keyword_key] in keyword_values):
                # check if keyword contains invalid value
                keyword_invalid = keyword_invalid + 1
            if not (row[sentiment_key] in sentiment_values):
                # check if sentiment contains invalid value
                sentiment_invalid = sentiment_invalid + 1
            if not (row[emotion_key] in emotion_values):
                # check if emotion contains invalid value
                emotion_invalid = emotion_invalid + 1
            if line % 1000000 == 0:
                print(line)
                # exit()
            line = line + 1
    print("number of total data:", line - 1)
    show_invalid_result()


if __name__ == '__main__':
    main()
    print('FINISHED!')
