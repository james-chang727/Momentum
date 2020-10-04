import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import eikon as ek
ek.set_app_key('bf38826c5e014c1cadf21425ee6e417d2b72fc9a')

""""=================================================================
The function returns a DataFrame that extracts monthly adjusted close 
price data from s_date to e_date for all RICs indicated and saves it 
to a file with filename as 'TrackedIndex_PeriodLength_data.csv'
====================================================================="""

def get_period_data(RIC_path, s_date, e_date):

    date_list = [d.strftime('%Y-%m-%d') for d in pd.date_range(start=s_date, end=e_date, freq='1M')]
    RIC_list = list(pd.read_excel(RIC_path, usecols='A')['RIC'])  # add in benchmark to get data
    max_row = 3000//int(len(RIC_list))
    
    df = ek.get_timeseries(RIC_list, fields='CLOSE', start_date=date_list[0], end_date=date_list[max_row-1],
                           interval='monthly', corax='adjusted')

    for i in range(len(date_list) // max_row - 1):
        df = df.append(ek.get_timeseries(RIC_list, fields='CLOSE', start_date=date_list[max_row * (i + 1)],
                                         end_date=date_list[max_row * (i + 2) - 1], interval='monthly', corax='adjusted'))

    df = df.append(ek.get_timeseries(RIC_list, fields='CLOSE', start_date=date_list[max_row * (len(date_list) // max_row)],
                                     end_date=date_list[-1], interval='monthly', corax='adjusted'))
    name = RIC_path.split('_')[0]

    return df.to_csv(f'{name}_20yr2.csv')

# change
get_period_data('data/TWMC100_RICs.xlsx', '2004-06-30', '2020-07-01')
