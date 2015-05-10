###############################################################################
# Name      :
# Purpose   :
# Author    : Austin Gross
# Created   : 2015-04-24
# Copyright : Copyright (c) 2015 Velotron Heavy Industries.
###############################################################################


import pandas as pd
import statsmodels.formula.api as smf


def deseason(timeseries):
    '''Accept iterator of dicts of timeseries and yield deseasonalized data'''

    counter = pd.DataFrame(timeseries)

    counter['datetime'] = pd.to_datetime(counter.datetime)

    counter.sort('datetime', inplace=True)

    counter['trend'] = counter.index

    counter = counter[counter.notnull().any(axis=1)]

    counter.set_index('datetime', inplace=True)

    counter['woy'] = counter.index.weekofyear
    counter['dow'] = counter.index.dayofweek
    counter['hr'] = counter.index.hour

    counter.reset_index(inplace=True)

    fmla = 'inbound ~ trend + C(woy) + C(dow) + C(hr)'
    result = smf.ols(formula=fmla, data=counter).fit()

    counter['fitted_inbound'] = result.predict()
    counter['residuals_inbound'] = result.resid

    fmla = 'outbound ~ trend + C(woy) + C(dow) + C(hr)'
    result = smf.ols(formula=fmla, data=counter).fit()

    counter['fitted_outbound'] = result.predict()
    counter['residuals_outbound'] = result.resid

    mask = ['datetime', 'fitted_inbound', 'residuals_inbound',
            'fitted_outbound', 'residuals_outbound']

    return counter[mask].to_dict('records')
