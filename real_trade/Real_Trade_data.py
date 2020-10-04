import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np 
import pandas as pd
import eikon as ek
ek.set_app_key('bf38826c5e014c1cadf21425ee6e417d2b72fc9a')

Benchmark = '.FTSETWMC'
DATE = datetime.strptime('2020-09-30', '%Y-%m-%d')
time_delta =  relativedelta(months=-1)

RICs = list(pd.read_excel('data/TWMC100_RICs.xlsx', usecols='A')['RIC'])
df = pd.read_csv('data/TWMC100_20yr.csv', index_col='Date')

# df2 =ek.get_timeseries(RICs+['.TWII', Benchmark], fields='CLOSE', start_date='2020-07-31', end_date=DATE, interval='monthly', corax='adjusted')
# df2['Date'] = [DATE+2*time_delta, DATE+time_delta, DATE]
# df2.set_index('Date', inplace=True)
# df = df.append(df2)
# df.to_csv('data/TWMC100_20yr.csv')

# check if all data are gotten!
check1 = np.unique(np.isnan(df.iloc[-1]))
check2 = np.unique(np.isnan(df.iloc[-2]))
check3 = np.unique(np.isnan(df.iloc[-3]))
print([check1, check2, check3]) #[array([False]), array([False]), array([False])]

"""================================================================================================================"""

df3 = pd.read_csv('data/TWMC100_beta_price.csv',index_col='Date')
df4 = pd.read_csv('data/TWMC100_20yr.csv', index_col='Date')[-3:].drop(columns='.FTSETWMC')
# df3 = df3.append(df4)
# df3.to_csv('data/TWMC100_beta_price.csv')

check1 = np.unique(np.isnan(df3.iloc[-1]))
check2 = np.unique(np.isnan(df3.iloc[-2]))
check3 = np.unique(np.isnan(df3.iloc[-3]))
print([check1, check2, check3]) #[array([False]), array([False]), array([False])]