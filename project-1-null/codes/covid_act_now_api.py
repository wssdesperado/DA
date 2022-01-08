import requests
import json
import csv

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/91.0.4472.114 Safari/537.36'}
url = 'https://api.covidactnow.org/v2/states.timeseries.json?apiKey=c0fca00fc52d4aec9ffdce7e971677e8'


def get_metric_attributes(state, num):
    num -= 1
    if 'vaccinationsInitiatedRatio' in state['metricsTimeseries'][num]:
        metric_attributes = state['metricsTimeseries'][num]['testPositivityRatio'], state['metricsTimeseries'][num][
            'caseDensity'], \
                            state['metricsTimeseries'][num][
                                'contactTracerCapacityRatio'], state['metricsTimeseries'][num]['infectionRate'], \
                            state['metricsTimeseries'][num]['infectionRateCI90'], \
                            state['metricsTimeseries'][num]['icuCapacityRatio'], state['metricsTimeseries'][num][
                                'vaccinationsInitiatedRatio'], \
                            state['metricsTimeseries'][num]['vaccinationsCompletedRatio']
    else:
        metric_attributes = state['metricsTimeseries'][num]['testPositivityRatio'], state['metricsTimeseries'][num][
            'caseDensity'], \
                            state['metricsTimeseries'][num][
                                'contactTracerCapacityRatio'], state['metricsTimeseries'][num]['infectionRate'], \
                            state['metricsTimeseries'][num]['infectionRateCI90'], \
                            state['metricsTimeseries'][num]['icuCapacityRatio'], None, None
    return metric_attributes


def get_actual_attributes(state, num):
    num -= 1
    if 'vaccinesDistributed' in state['actualsTimeseries'][num]:
        actual_attributes = state['actualsTimeseries'][num]['cases'], state['actualsTimeseries'][num]['deaths'], \
                            state['actualsTimeseries'][num][
                                'positiveTests'], \
                            state['actualsTimeseries'][num]['negativeTests'], state['actualsTimeseries'][num][
                                'contactTracers'], \
                            state['actualsTimeseries'][num]['hospitalBeds']['capacity'], \
                            state['actualsTimeseries'][num]['hospitalBeds'][
                                'currentUsageTotal'], state['actualsTimeseries'][num]['hospitalBeds'][
                                'currentUsageCovid'], \
                            state['actualsTimeseries'][num]['icuBeds']['capacity'], \
                            state['actualsTimeseries'][num]['icuBeds'][
                                'currentUsageTotal'], state['actualsTimeseries'][num]['icuBeds']['currentUsageCovid'], \
                            state['actualsTimeseries'][num]['newCases'], state['actualsTimeseries'][num]['newDeaths'], \
                            state['actualsTimeseries'][num][
                                'vaccinesAdministeredDemographics'], state['actualsTimeseries'][num][
                                'vaccinationsInitiatedDemographics'], state['actualsTimeseries'][num][
                                'vaccinesDistributed'], \
                            state['actualsTimeseries'][num]['vaccinationsInitiated'], state['actualsTimeseries'][num][
                                'vaccinationsCompleted'], \
                            state['actualsTimeseries'][num]['vaccinesAdministered']
    else:
        actual_attributes = state['actualsTimeseries'][num]['cases'], state['actualsTimeseries'][num]['deaths'], \
                            state['actualsTimeseries'][num][
                                'positiveTests'], \
                            state['actualsTimeseries'][num]['negativeTests'], state['actualsTimeseries'][num][
                                'contactTracers'], \
                            state['actualsTimeseries'][num]['hospitalBeds']['capacity'], \
                            state['actualsTimeseries'][num]['hospitalBeds'][
                                'currentUsageTotal'], state['actualsTimeseries'][num]['hospitalBeds'][
                                'currentUsageCovid'], \
                            state['actualsTimeseries'][num]['icuBeds']['capacity'], \
                            state['actualsTimeseries'][num]['icuBeds'][
                                'currentUsageTotal'], state['actualsTimeseries'][num]['icuBeds']['currentUsageCovid'], \
                            state['actualsTimeseries'][num]['newCases'], state['actualsTimeseries'][num]['newDeaths'], \
                            state['actualsTimeseries'][num][
                                'vaccinesAdministeredDemographics'], state['actualsTimeseries'][num][
                                'vaccinationsInitiatedDemographics'], None, None, None, None
    return actual_attributes


def get_risk_level_attributes(state, num):
    num -= 1
    risk_level_attributes = state['riskLevelsTimeseries'][num]['overall'], state['riskLevelsTimeseries'][num][
        'caseDensity']
    return risk_level_attributes


def get_cdc_transmission_level_timeseries(state, num):
    num -= 1
    cdc_transmission_level_timeseries_attributes = state['cdcTransmissionLevelTimeseries'][num]['cdcTransmissionLevel']
    return cdc_transmission_level_timeseries_attributes


def main():
    # storage the number of valid value for each attribute
    attributes = {
        'test_positivity_ratio': 0,
        'case_density': 0,
        'contact_tracer_capacity_ratio': 0,
        'infection_rate': 0,
        'infection_rate_ci': 0,
        'icu_capacity_ratio': 0,
        'vaccinations_initiated_ratio': 0,
        'vaccinations_completed_ratio': 0,
        'cdc_transmission_level': 0,
        'cases': 0,
        'deaths': 0,
        'positive_tests': 0,
        'negative_tests': 0,
        'contact_tracers': 0,
        'hospital_beds_capacity': 0,
        'hospital_beds_current_usage_total': 0,
        'hospital_beds_current_usage_covid': 0,
        'icu_beds_capacity': 0,
        'icu_beds_current_usage_total': 0,
        'icu_beds_current_usage_covid': 0,
        'new_cases': 0,
        'new_deaths': 0,
        'vaccines_distributed': 0,
        'vaccinations_initiated': 0,
        'vaccinations_competed': 0,
        'vaccines_administered': 0,
        'vaccines_administered_demographics': 0,
        'vaccinations_initiated_demographics': 0,
        'overall': 0,
        'case_density_risk_level': 0
    }

    output_file_path = "./results.csv"
    output = open(output_file_path, 'a')
    writer = csv.writer(output)
    writer.writerow(())

    # request api
    response_json = requests.get(url, header)
    # change json response into dict
    response_dict = json.loads(response_json.text)

    # count the number of missing values
    for state in response_dict:
        for metric in state['metricsTimeseries']:
            if metric['testPositivityRatio'] is not None:
                attributes['test_positivity_ratio'] += 1
            if metric['caseDensity'] is not None:
                attributes['case_density'] += 1
            if metric['contactTracerCapacityRatio'] is not None:
                attributes['contact_tracer_capacity_ratio'] += 1
            if metric['infectionRate'] is not None:
                attributes['infection_rate'] += 1
            if metric['infectionRateCI90'] is not None:
                attributes['infection_rate_ci'] += 1
            if metric['icuCapacityRatio'] is not None:
                attributes['icu_capacity_ratio'] += 1
            if 'vaccinationsInitiatedRatio' in metric and metric['vaccinationsInitiatedRatio'] is not None:
                attributes['vaccinations_initiated_ratio'] += 1
            if 'vaccinationsCompletedRatio' in metric and metric['vaccinationsCompletedRatio'] is not None:
                attributes['vaccinations_completed_ratio'] += 1

        for actual in state['actualsTimeseries']:
            if actual['cases'] is not None:
                attributes['cases'] += 1
            if actual['deaths'] is not None:
                attributes['deaths'] += 1
            if actual['positiveTests'] is not None:
                attributes['positive_tests'] += 1
            if actual['negativeTests'] is not None:
                attributes['negative_tests'] += 1
            if actual['contactTracers'] is not None:
                attributes['contact_tracers'] += 1
            if actual['hospitalBeds']['capacity'] is not None:
                attributes['hospital_beds_capacity'] += 1
            if actual['hospitalBeds']['currentUsageTotal'] is not None:
                attributes['hospital_beds_current_usage_total'] += 1
            if actual['hospitalBeds']['currentUsageCovid'] is not None:
                attributes['hospital_beds_current_usage_covid'] += 1
            if actual['icuBeds']['capacity'] is not None:
                attributes['icu_beds_capacity'] += 1
            if actual['icuBeds']['currentUsageTotal'] is not None:
                attributes['icu_beds_current_usage_total'] += 1
            if actual['icuBeds']['currentUsageCovid'] is not None:
                attributes['icu_beds_current_usage_covid'] += 1
            if actual['newCases'] is not None:
                attributes['new_cases'] += 1
            if actual['newDeaths'] is not None:
                attributes['new_deaths'] += 1
            if 'vaccinesDistributed' in actual and actual['vaccinesDistributed'] is not None:
                attributes['vaccines_distributed'] += 1
            if 'vaccinationsInitiated' in actual and actual['vaccinationsInitiated'] is not None:
                attributes['vaccinations_initiated'] += 1
            if 'vaccinationsCompleted' in actual and actual['vaccinationsCompleted'] is not None:
                attributes['vaccinations_competed'] += 1
            if 'vaccinesAdministered' in actual and actual['vaccinesAdministered'] is not None:
                attributes['vaccines_administered'] += 1
            if actual['vaccinesAdministeredDemographics'] is not None:
                attributes['vaccines_administered_demographics'] += 1
            if actual['vaccinationsInitiatedDemographics'] is not None:
                attributes['vaccinations_initiated_demographics'] += 1

        for risk_level in state['riskLevelsTimeseries']:
            if risk_level['overall'] is not None:
                attributes['overall'] += 1
            if risk_level['caseDensity'] is not None:
                attributes['case_density_risk_level'] += 1

        for cdc_transmission_level_timeseries in state['cdcTransmissionLevelTimeseries']:
            if cdc_transmission_level_timeseries['cdcTransmissionLevel'] is not None:
                attributes['cdc_transmission_level'] += 1
    # calculate the fraction of missing value
    for values in attributes.keys():
        attributes[values] /= len(response_dict[0]['cdcTransmissionLevelTimeseries'])
    # print cleanliness result in console
    print(attributes)
    # write dataset into csv file
    for data in response_dict:
        for num in range(1, len(data['metricsTimeseries'])):
            writer.writerow((get_metric_attributes(data, num), get_actual_attributes(data, num),
                             get_risk_level_attributes(data, num), get_cdc_transmission_level_timeseries(data, num)))


if __name__ == '__main__':
    main()
