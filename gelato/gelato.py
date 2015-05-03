###############################################################################
# Name      : 
# Purpose   :
# Author    : Austin Gross
# Created   : 2015-04-24
# Copyright : Copyright (c) 2015 Velotron Heavy Industries.
###############################################################################


import pandas as pd
# import statsmodels.api as sm
import statsmodels.formula.api as smf

import sys
sys.path.append('../')
from glass import glass


def deseasonalize(id=None):
    '''Accept location id and return deseasonalized data as json.'''
    counter = glass.get_counter_data(id=id)

    counter = pd.DataFrame(counter)

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

    result = counter[['datetime', 'result']].to_json()

    return(result)
