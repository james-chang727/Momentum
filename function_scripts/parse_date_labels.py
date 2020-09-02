def func(HP, lst):

    stk = []

    if HP == 1:
        for i in lst:
            split = i.split('-')
            join = '-'.join(split[0:-1])
            stk.append(join)

    elif HP == 3:
        for i in lst:
            split = i.split('-')
            if split[1] == '03':
                stk.append(f'{split[0]}Q1')
            elif split[1] == '06':
                stk.append(f'{split[0]}Q2')
            elif split[1] == '09':
                stk.append(f'{split[0]}Q3')
            else:
                stk.append(f'{split[0]}Q4')

    elif HP == 6:
        for i in lst:
            split = i.split('-')
            if split[1] == '12':
                stk.append(f'{split[0]}H2')
            else:
                stk.append(f'{split[0]}H1')

    return stk