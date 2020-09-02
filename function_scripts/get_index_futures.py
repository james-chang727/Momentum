import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import re
import pandas as pd
# import eikon as ek
# ek.set_app_key('bf38826c5e014c1cadf21425ee6e417d2b72fc9a')

# data, err = ek.get_data('TXc1', ['TR.SETTLEMENTPRICE.DATE', 'TR.SETTLEMENTPRICE'],
#                         {'SDate': '0', 'EDate': '-222', 'Frq': 'M'})
# data.drop('Instrument', axis=1, inplace=True)
# data['Date'] = data['Date'].apply(lambda x: x.split('T')[0])
# data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
#
#
# data.sort_values('Date', inplace=True)
# data.set_index('Date', inplace=True)
#
#
# print(data.index)
# data.to_csv(f'../data/Index_futures_20yr.csv')



# import requests
# from bs4 import BeautifulSoup
#
# url = 'https://www.taifex.com.tw/enl/eng5/futIndxFSP'
# source = requests.get(url).text
#
# soup = BeautifulSoup(source, 'lxml')
#
# table = soup.find(class_='table_c')
# df = pd.read_html(str(table))[0]
# df = df[['the final settlement day', 'contract delivery month', '（TX/MTX）']]



# settle_df = pd.read_csv('../data/test.csv', names=['Date'])
# settle_df['Delivery Month'] = settle_df['Date'].apply(lambda x: x.split('\t')[1])
# settle_df['Settlement Price'] = settle_df['Date'].apply(lambda x: x.split('\t')[-1])
# settle_df['Date'] = settle_df['Date'].apply(lambda x: x.split('\t')[0])
# settle_df.set_index(settle_df['Delivery Month'], inplace=True)
#
# pattern = re.compile(r'\d{6}W[1-5]')
# stk = []
#
# for string in settle_df['Delivery Month']:
#     matches = pattern.finditer(string)
#     for match in matches:
#         stk.append(match.group(0))
#
# settle_df.drop(stk, axis=0, inplace=True)
# settle_df.reset_index(drop=True, inplace=True)
# settle_df.set_index('Date', inplace=True)
#
# settle_df.to_csv('../data/Index_Futures_taifex.csv')

settle_df = pd.read_csv('../data/Index_Futures_taifex.csv')[1:]

date = settle_df['Date'].to_list()

for i in range(len(date)):
    date[i] = date[i].split('/')[0] + '-' + date[i].split('/')[1] + '-' + date[i].split('/')[2]

settle_df['Date'] = date
settle_df['Date'] = pd.to_datetime(settle_df['Date'], format='%Y-%m-%d')
settle_df.sort_values(by=['Date'], ascending=True, inplace=True)
settle_df.set_index('Date', inplace=True)