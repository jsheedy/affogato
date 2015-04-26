###############################################################################
# Name      : 
# Purpose   :
# Author    : Austin Gross
# Created   : 2015-04-24
# Copyright : Copyright (c) 2015 Velotron Heavy Industries.
###############################################################################


import json                         # interface with APIs
import pandas as pd
# import statsmodels.api as sm
import statsmodels.formula.api as smf
import urllib                       # interface with APIs


def api_to_json(url=None):
    '''Takes a url, returns json.'''
    try:
        df = urllib.request.urlopen(url).read().decode('utf-8')
    except IOError as e:
        return e
    except NameError as e:
        return e

    return(df)


def json_to_df(df):
    '''Takes a socrata json and returns a dataframe.'''
    try:
        df = json.loads(df)
    except ValueError as e:
        return e

    df = pd.DataFrame(df)

    return(df)


def format_df(df):
    '''Strip identifier from 'totals' column.'''
    df.columns = [x.split('_')[-1] for x in df.columns.tolist()]

    df['date'] = pd.to_datetime(df.date)

    df.set_index('date', inplace=True)

    df = df.astype('float')

    return(df)


def ped_data(df):
    '''Splits pedestrian data into separate dataframe. Formats resulting
        dataframes.'''
    dfPeds = [x for x in df.columns if 'ped' in x]

    if dfPeds:
        temp = df

        df = df.drop(dfPeds, axis=1)

        dfPeds += ['date']

        dfPeds = temp[dfPeds]

        del temp

        dfPeds = format_df(dfPeds)
    else:
        dfPeds = pd.DataFrame()

    df = format_df(df)

    return(df, dfPeds)


# def get_counters():
#     counters = \
#         {'SW Oregon': ('https://data.seattle.gov/resource/mefu-7eau.json',
#                        (47.562903, -122.365474)),  # 26th Ave SW Greenway at SW Oregon St
#          'Myrtle Edwards': ('https://data.seattle.gov/resource/4qej-qvrz.json',
#                             (47.619760, -122.361463)),  # Elliott Bay Trail in Myrtle Edwards Park
#          'I90': ('https://data.seattle.gov/resource/u38e-ybnc.json',
#                  (47.590466, -122.286760)),  # MTS Trail west of I90 Bridge
#          'Sealth Trail': ('https://data.seattle.gov/resource/uh8h-bme7.json',
#                           (47.527991, -122.280988)),  # Chief Sealth Trail North of Thistle
#          'NW 58th': ('https://data.seattle.gov/resource/47yq-6ugv.json',
#                      (47.670921, -122.384768)),  # NW 58th St Greenway at 22nd Ave NW
#          'Burke Gilman': ('https://data.seattle.gov/resource/2z5v-ecg8.json',
#                           (47.679563, -122.265262)),  # Burke Gilman Trail north of NE 70th St
#          'NE 62nd': ('https://data.seattle.gov/resource/3h7e-f49s.json',
#                      (47.673972, -122.285791)),  # 39th Ave NE Greenway at NE 62nd St
#          'Broadway Bikeway': ('https://data.seattle.gov/resource/j4vh-b42a.json',
#                               (47.612966, -122.320829)),  # Broadway Bikeway at Union St
#          'Fremont Street': ('https://data.seattle.gov/resource/65db-xm6k.json',
#                             (47.647716, -122.347391)),  # Fremont Street Bridge
#          'Spokane Street': ('https://data.seattle.gov/resource/upms-nr8w.json',
#                             (47.571353, -122.350940))}  # Spokane Street Bridge

#     return(counters)


# url = 'http://www-k12.atmos.washington.edu/k12/grayskies/quickfix.cgi?'
# url += 'uwa+overlay+/var/tmp/tempdata755833.html'

# df = urllib.urlopen(url).read().decode('utf-8')



def _analysis():
    weather = pd.read_csv('C:/Users/austing/Desktop/precip_2014.txt',
                          sep='\s*', header=None)

    weather = weather[[0, 1, 14]]

    weather = weather.astype('str')

    # weather['date'] = 

    counters = b.get_counters()

    counter = b.api_to_json(counters['Broadway Bikeway'][0])

    counter = b.api_to_df(counter)

    counter, counterPed = b.ped_data(counter)

    counter['woy'] = counter.index.weekofyear
    counter['dow'] = counter.index.dayofweek
    counter['hr'] = counter.index.hour

    fmla = 'nb ~ C(woy) + C(dow) * C(hr)'
    result = smf.ols(formula=fmla, data=counter).fit()
    print(result.summary())

    fmla = 'nb ~ C(woy) + C(dow) * C(hr)'
    result = smf.poisson(formula=fmla, data=counter).fit()
    print(result.summary())

    return()
