###############################################################################
# Name      :
# Purpose   :
# Author    : Austin Gross
# Created   : 2015-04-24
# Copyright : Copyright (c) 2015 Velotron Heavy Industries.
###############################################################################


import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def data_prep(timeseries):
    '''Prepare timeseries data for analysis'''
    counter = pd.DataFrame(timeseries)

    counter['datetime'] = pd.to_datetime(counter.datetime)

    counter.sort('datetime', inplace=True)

    counter['trend'] = counter.index

    counter = counter[~counter.isnull().any(axis=1)]

    counter.set_index('datetime', inplace=True)

    counter['woy'] = counter.index.weekofyear
    counter['dow'] = counter.index.dayofweek
    counter['hr'] = counter.index.hour

    counter.reset_index(inplace=True)

    return counter


def deseason(timeseries, interact=False):
    '''Accept iterator of dicts of timeseries and yield deseasonalized data'''
    counter = data_prep(timeseries)

    fmla = 'inbound ~ -1 + trend + '

    if interact:
        fmla += ' C(counter_id) * C(hr) + C(woy) + C(dow)'
    else:
        fmla += ' C(counter_id) + C(woy) + C(dow) + C(hr)'

    result = smf.ols(formula=fmla, data=counter).fit()

    counter['fitted_inbound'] = result.predict()
    counter['residuals_inbound'] = result.resid
    counter['trend_inbound'] = result.params.trend * counter.trend

    fmla = 'outbound ~ -1 + trend + '

    if interact:
        fmla += ' C(counter_id) * C(hr) + C(woy) + C(dow)'
    else:
        fmla += ' C(counter_id) + C(woy) + C(dow) + C(hr)'
    result = smf.ols(formula=fmla, data=counter).fit()

    counter['fitted_outbound'] = result.predict()
    counter['residuals_outbound'] = result.resid
    counter['trend_outbound'] = result.params.trend * counter.trend

    mask = ['datetime', 'counter_id',
            'fitted_inbound', 'fitted_outbound',
            'residuals_inbound', 'residuals_outbound',
            'trend_inbound', 'trend_outbound']

    return counter[mask].to_dict('records')


def pronto_effect(timeseries):
    counter = data_prep(timeseries)

    mask = counter.datetime >= '2014-10-13'

    counter['post'] = 0
    counter.ix[mask, 'post'] = 1

    mask = [2, 7, 8, 9]
    mask = counter.counter_id.isin(mask)

    counter['treat'] = 0
    counter.ix[mask, 'treat'] = 1

    fmla = 'inbound ~ -1 + trend + C(woy) + C(dow) + C(hr) + '
    fmla += ' C(treat) * C(post)'
    result = smf.ols(formula=fmla, data=counter).fit()

    return counter
