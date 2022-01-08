
import csv
import pandas as pd
import plotly.graph_objects as go
import argparse
def draw(df,required_date,feature):
    # draw the distribution map
    fig = go.Figure(data=go.Choropleth(
        locations= df['state'],  # Spatial coordinates
        z = df[feature].astype(float),  # Data to be color-coded
        locationmode='USA-states',  # set of locations match entries in `locations`
        colorscale='Reds',
        colorbar_title=feature,
    ))

    fig.update_layout(
        title_text=required_date+ ': ',
        geo_scope='usa',  # limite map scope to USA
    )
    fig.show()
    fig.write_html('../dataset/state-'+ feature +'.html')

def read_data(required_date):
    # extract needed data into file
    Mydata = pd.read_csv('../dataset/labeled.csv', sep=',')
    with open('../dataset/State-death-' + required_date + '.csv', 'w+', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(['state', 'deaths','cases','vaccinationsCompleted','hospitalBeds capacity','vaccinationsCompletedRatio'])
        for i in range(len(Mydata['date'])):
            if Mydata['date'][i] == required_date:
                data = [Mydata['state'][i], Mydata['deaths'][i],Mydata['cases'][i], Mydata['vaccinationsCompleted'][i],Mydata['hospitalBeds capacity'][i],Mydata['vaccinationsCompletedRatio'][i]]
                csv_write = csv.writer(f)
                csv_write.writerow(data)
    f.close()
    df = pd.read_csv('../dataset/State-death-' + required_date + '.csv', sep=',')
    return df
def main():
    parser = argparse.ArgumentParser(description='date')
    parser.add_argument('date', type=str)
    date = parser.parse_args().date
    df = read_data(date)
    for feature in ['deaths','cases','vaccinationsCompleted','hospitalBeds capacity','vaccinationsCompletedRatio']:
        draw(df,date,feature)

if __name__ == '__main__':
    main()