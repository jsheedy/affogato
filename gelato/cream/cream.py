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

import sys
sys.path.append('../..')
from glass import glass


def api_to_json(url=None):
    '''Takes a url, returns json.'''
    url += '?$limit=50000'
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

    return(df)


def ped_data(df):
    '''Splits pedestrian data into separate dataframe. Formats resulting
        dataframes.'''
    dfPeds = [x for x in df.columns if 'ped' in x]

    if dfPeds:
        temp = df

        df = df.drop(dfPeds, axis=1)

        dfPeds += ['date', 'id']

        dfPeds = temp[dfPeds]

        del temp

        dfPeds = format_df(dfPeds)
    else:
        dfPeds = pd.DataFrame()

    df = format_df(df)

    return(df, dfPeds)


def create_analysis_df():
    '''Append dataframes.'''
    counters = glass.get_counters()
    counters = list(counters)

    loop = pd.DataFrame()
    loopPeds = pd.DataFrame()
    for i in counters:
        print(i['url'])
        temp = api_to_json(i['url'])
        temp = json_to_df(temp)
        temp['id'] = i['id']

        temp, tempPeds = ped_data(temp)

        loop = loop.append(temp)

        loopPeds = loopPeds.append(tempPeds)

    return(loop, loopPeds)

# url = 'http://www-k12.atmos.washington.edu/k12/grayskies/quickfix.cgi?'
# url += 'uwa+overlay+/var/tmp/tempdata755833.html'

# df = urllib.urlopen(url).read().decode('utf-8')


def _analysis():
    weather = pd.read_csv('C:/Users/austing/Desktop/precip_2014.txt',
                          sep='\s*', header=None)

    weather = weather[[0, 1, 14]]

    weather = weather.astype('str')

    # weather['date'] =

    counters = glass.get_counters()

    counter = json_to_df(counters['Broadway Bikeway'][0])

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
