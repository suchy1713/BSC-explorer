import numpy as np

def get_st(n):
    if n == 1:
        return 'st'
    elif n==2:
        return 'nd'
    elif n==3:
        return 'rd'
    return 'th'

def get_formation_label(grouped, vector):
    my_grouped = grouped.loc[grouped['vector'] == vector]
    label = my_grouped['formation_label'].values[0]
    order = list(my_grouped.index)[0]
    time = my_grouped['90s_played'].values[0]
    time_all = grouped['90s_played'].sum()

    return f"{label} ({order}{get_st(order)} Most Used - {'{0:g}'.format(np.round(time, 1))} 90s, {'{0:g}'.format(np.round(time/time_all*100, 1))}%)"