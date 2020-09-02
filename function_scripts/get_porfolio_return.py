"""

The function slices data from the afore-compiled TopWorse10_list from
the DataFrame, maps each iteration with the corresponding lagged
period_list and returns the portfolio return of each holding period

"""

def get_port_return(lst, df):
    stk = []

    for i in range(len(lst)):
        Top10_return = df[lst[i][0]].iloc[i].sum()
        Worse10_return = df[lst[i][-1]].iloc[i].sum()

        port_return = 0.1 * Top10_return - 0.1 * Worse10_return
        stk.append(port_return)

    return stk
