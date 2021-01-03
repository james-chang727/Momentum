import pandas as pd

df = pd.read_csv('data/TWMC100_20yr.csv', index_col='Date')[-7:].iloc[[0,6]]
Top10_current = df.pct_change().iloc[-1].sort_values(ascending=False).head(10)
print(list(Top10_current.index))

TWMC100 = list(Top10_current.index)
df2 = pd.read_csv('data/TWMC100_beta_regressed_24mths.csv', index_col='Date')

betas = df2.loc['2020-12-31', TWMC100].to_list()
print(betas)

