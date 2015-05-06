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


def deseasonalize(timeseries):
    '''Accept iterator of dicts of timeseries and yields deseasonalized data'''

    counter = pd.DataFrame(timeseries)

    counter['datetime'] = pd.to_datetime(counter.datetime)

    counter['trend'] = counter.index

    counter = pd.melt(counter, id_vars=['datetime', 'trend'])

    counter = counter[counter.value.notnull()]

    counter['value'] = counter.value.astype('int')

    counter.set_index('datetime', inplace=True)

    counter['woy'] = counter.index.weekofyear
    counter['dow'] = counter.index.dayofweek
    counter['hr'] = counter.index.hour

    counter.reset_index(inplace=True)

    fmla = 'value ~ -1 + trend + C(woy) + C(dow) + C(hr)'
    result = smf.ols(formula=fmla, data=counter).fit()

    counter['result'] = result.resid

    return counter[['datetime','result']]
