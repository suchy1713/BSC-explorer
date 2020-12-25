import numpy as np

def calc_metrics(formation, events):
    passes = events.loc[events['type'] == 'Pass'].loc[events['outcomeType'] == 'Successful']
    formation['xt'] = passes['xt'].sum()
    formation['avg_height'] = passes['start_x'].median()
    formation['minutes'] = passes['time_minutes'].max()
    formation['n_passes'] = passes.shape[0]

    return formation