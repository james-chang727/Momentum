"""

The function returns a list of tuples: (Top10, Worse10) that was
identified from the deciding period and will be used to calculate the
portfolio return for the holding period.

"""

def get_DP_TopWorse10(df):
    stk = []
    for date in df.index:
        Top10 = df.loc[date].dropna().sort_values(ascending=False).head(10).index.to_list()
        Worse10 = df.loc[date].dropna().sort_values(ascending=False).tail(10).index.to_list()
        tup = Top10, Worse10
        stk.append(tup)

    return stk

