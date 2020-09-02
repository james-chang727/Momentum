"""

Momentum Strategy (DP, HP)

Deciding period (DP): we observe the performance of each stock in the previous period
Holding period (HP): we then implement the positions identified in the deciding period

Nuances of this strategy: The portfolio return is significant and the beta is near zero
when we use TAIEX's or TW50 index's return. However, when we calculate the portfolio return
using cumulative roll-over return of the index futures, the results are quite the opposite.

Possible reasons:
1. The future prices are not acquired properly (settlement prices, timing mismatch...)
2. Futures return and Index return deviates due to the "rolling yield" (questions this strategy)

"""

import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from function_scripts.get_TopWorse10 import get_DP_TopWorse10
from function_scripts.parse_date_labels import func

## Input variables
DP = 6
HP = 3
Index_name = 'TWMC100'
Benchmark = '.FTSETWMC'
futures = 'TXc1'

plot_map = {1: 'Monthly', 3: 'Quarterly', 6: 'Semi-annually'}

# Change
df = pd.read_csv('data/TWMC100_20yr.csv', index_col='Date')
df2 = pd.read_csv('data/Index_futures_20yr.csv', index_col='Date')[30:]  # Read data in, change length
df[futures] = df2['Settlement Price'].values

"""  filter out two dfs, one for extracting DP TopWorse10 list (df_getRIC),
     the other for applying to HP for actual return (df_applyRIC)  """

filt = [df.index[i] for i in range(len(df.index)) if i % HP == 0]
df_getRIC = df.loc[filt].pct_change(periods=int(DP / HP)).iloc[int(DP / HP):-1]
df_applyRIC = df.loc[filt].pct_change().iloc[int(DP / HP) + 1:].applymap(lambda x: x * 100)
df_beta = pd.read_csv('data/TWMC100_beta_regressed.csv', index_col='Date').loc[filt].iloc[int(DP / HP) + 1:]  # change

TopWorse10_list = get_DP_TopWorse10(df_getRIC.drop([Benchmark, '.TWII', futures], axis=1))  # Get TopWorse10 list of tuples of lists (get_TopWorse10.py)

def get_index_return():
    stk = []
    for i in range(len(df_getRIC)):
        ret = df2.pct_change()[1:]
        ret = ret['Settlement Price'].iloc[HP*i:HP*(i+1)]
        Index_futures_return = 100 * ((ret.apply(lambda x: x+1).cumprod().iloc[-1])-1)
        stk.append(Index_futures_return)
    return stk

Index_futures_return = get_index_return()


def get_port_return(lst, df):
    stk = []
    stk2 = []
    for i in range(len(lst)):
        beta_list = []
        for ric in lst[i][0]:
            stock_beta = df_beta[ric].iloc[i]
            Top10_return = df[lst[i][0]].iloc[i].sum()
            beta_list.append(stock_beta)

        port_return = 0.1 * Top10_return - (0.1 * sum(beta_list)) * df[futures].iloc[i]
        port_return2 = 0.1 * Top10_return - (0.1 * sum(beta_list)) * Index_futures_return[i]

        stk.append(port_return)
        stk2.append(port_return2)

    return stk, stk2, beta_list

portfolio_return = get_port_return(TopWorse10_list, df_applyRIC)[0]  # Get portfolio return

## Create a DataFrame with portfolio return and cumulative return as columns (parse_date_labels.py)

result = pd.DataFrame(portfolio_return, index=func(HP, df_applyRIC.index)).rename(columns={0: 'Portfolio Return'})
cum_return = (result['Portfolio Return']) / 100 + 1
result['Portfolio Return (cum_futures_ret)'] = get_port_return(TopWorse10_list, df_applyRIC)[1]
result['Index'] = df_applyRIC['.TWII'].values
result['Cumulative Return'] = cum_return.cumprod()

## T-test for portfolio alpha significance
from scipy.stats import ttest_1samp
from scipy.stats import linregress
import math

alpha_beta = tuple(linregress(result['Index'].dropna(), result['Portfolio Return'].dropna()))[0:2]
sharpe = math.sqrt(12) * (result['Portfolio Return'].mean() / (result['Portfolio Return'] - result['Index']).std())
t_stat = tuple(ttest_1samp(result['Portfolio Return'], 0, nan_policy='omit'))

print(alpha_beta)
print(sharpe)
print(t_stat)

# Read to xlsx, comment out
index = result.index.to_list()

# writer = pd.ExcelWriter(f'results/Short_{futures}futures_beta_hedged_{Index_name}_{DP}m{HP}m_tstat_{t_stat[0]:.2f}_pval_{t_stat[-1]:.2f}_{index[0]}_to_{index[-1]}.xlsx', engine='xlsxwriter')
# result.to_excel(writer)
# writer.save()

## Plotting
# plt overlap line and bar chart

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # set up the 2nd axis
ax1.bar(result.index.to_list(), height=result['Portfolio Return'], color='orange')
ax2.plot(result.index.to_list(), result['Cumulative Return'])
ax2.grid(b=False)
ax1.axes.xaxis.set_ticklabels([])

ax1.set_title(f'{index[0]}~{index[-1]} {plot_map[HP]} Portfolio Return (%) vs Cumulative Return')
ax1.set_ylabel('Portfolio Return (%)')
ax2.set_ylabel('Cumulative Return (base=1)')

# Save figure

# fig.savefig(f'results/Short_{futures}futures_beta_hedged_{Index_name}_{DP}m{HP}m_alpha_{alpha_beta[1]:.2f}_beta_{alpha_beta[0]:.2f}_sharpe_{sharpe:.2f}.png')
plt.close('all')
