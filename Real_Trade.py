import pandas as pd

TW50 = ['6669.TW', '2327.TW', '4938.TW', '2382.TW', '2207.TW', '2303.TW', '2330.TW', '1101.TW', '2357.TW', '2886.TW']
df = pd.read_csv('data/TW50_beta_regressed.csv', index_col='Date')

betas = df.loc['2020-06-30', TW50].to_list()
print(betas)

TWMC100 = ['5269.TW', '8454.TW', '6415.TW', '3532.TW', '1590.TW', '2371.TW', '1229.TW', '1789.TW', '2356.TW', '8046.TW']
df2 = pd.read_csv('data/TWMC100_beta_regressed.csv', index_col='Date')

betas2 = df2.loc['2020-06-30', TWMC100].to_list()
print(betas2)