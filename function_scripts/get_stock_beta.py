import warnings
warnings.simplefilter(action='ignore', category=RuntimeWarning)

import pandas as pd
import numpy as np
from statsmodels.regression.linear_model import OLS

data = pd.read_csv('data/TWMC100_beta_price.csv', index_col='Date')
data = data.pct_change()[1:]
print(data.index)

def get_beta():

    stk = []
    for column in data.drop(['.TWII'], axis=1).columns:
        stk1 = []

        for i in range(196):  # change value for different indices
            if data[column].iloc[i:i+24].isnull().all():
                beta = np.NaN
                stk1.append(beta)
            else:
                beta = OLS(data[column].iloc[i:i+24], data['.TWII'].iloc[i:i+24], missing='drop').fit().params[-1]
                stk1.append(beta)

        stk.append(stk1)


    df = pd.DataFrame(stk).T
    df.index = data.index.to_list()[23:]
    df.index.name = 'Date'
    df.columns = data.drop('.TWII', axis=1).columns.to_list()

    return df.to_csv(f'data/TWMC100_beta_regressed_24mths.csv')

get_beta()
