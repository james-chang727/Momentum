"""

Momentum Strategy (DP, HP)

Deciding period (DP): we observe the performance of each stock in the previous period
Holding period (HP): we then implement the positions identified in the deciding period

Starting from when the index was first clustered, we adjust our
portfolio for every deciding period. (i.e. we adjust our holdings every six months with
regards to the deciding period's performance)

"""

import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from function_scripts.get_TopWorse10 import get_DP_TopWorse10
from function_scripts.get_porfolio_return import get_port_return
from function_scripts.parse_date_labels import func

## Input variables
DP = 6
HP = 6
Index_name = 'TW50'
Benchmark = '.FTSETW50'

plot_map = {1: 'Monthly', 3: 'Quarterly', 6: 'Semi-annually'}

# Change
df = pd.read_csv('data/TW50_20yr.csv', index_col='Date')  # Read data in

"""  filter out two dfs, one for extracting DP TopWorse10 list (df_getRIC),
     the other for applying to HP for actual return (df_applyRIC)  """

filt = [df.index[i] for i in range(len(df.index)) if i % HP == 0]
df_getRIC = df.loc[filt].pct_change(periods=int(DP / HP)).iloc[int(DP / HP):-1]
df_applyRIC = df.loc[filt].pct_change().iloc[int(DP / HP) + 1:].applymap(lambda x: x * 100)

TopWorse10_list = get_DP_TopWorse10(df_getRIC.drop(Benchmark, axis=1))  # Get TopWorse10 list of tuples of lists (get_TopWorse10.py)

portfolio_return = get_port_return(TopWorse10_list, df_applyRIC.drop(Benchmark, axis=1))  # Get portfolio return (get_portfolio_return.py)

## Create a DataFrame with portfolio return and cumulative return as columns (parse_date_labels.py)

result = pd.DataFrame(portfolio_return, index=func(HP, df_applyRIC.index)).rename(columns={0: 'Portfolio Return'})
cum_return = (result['Portfolio Return']) / 100 + 1
result['Index'] = df_applyRIC['.TWII'].values
result['Cumulative Return'] = cum_return.cumprod()

## T-test for portfolio alpha significance
from scipy.stats import ttest_1samp
from scipy.stats import linregress
import math

alpha_beta = tuple(linregress(result.dropna()['Index'], result.dropna()['Portfolio Return']))[0:2]
sharpe = math.sqrt(12) * (result['Portfolio Return'].mean() / (result['Portfolio Return'] - result['Index']).std())
t_stat = tuple(ttest_1samp(result['Portfolio Return'], 0))

print(alpha_beta)
print(sharpe)
print(t_stat)

# Read to xlsx, comment out
index = result.index.to_list()

# writer = pd.ExcelWriter(f'results/{Index_name}_{DP}m{HP}m_tstat_{t_stat[0]:.2f}_pval_{t_stat[-1]:.2f}_{index[0]}_to_{index[-1]}.xlsx', engine='xlsxwriter')
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

# fig.savefig(f'results/{Index_name}_{DP}m{HP}m_alpha_{alpha_beta[1]:.2f}_beta_{alpha_beta[0]:.2f}_sharpe_{sharpe:.2f}.png')
plt.close('all')