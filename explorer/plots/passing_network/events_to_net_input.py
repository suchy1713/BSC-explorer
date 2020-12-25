import numpy as np
import pandas as pd

from plots.utils import filter_phase, get_average_positions
from plots.codes import Passes

from metadata.strings import *

ref_vec = (10, 0)
ref_vec_len = np.sqrt(100)
cosine_threshold = 0.125
own_thr = 30
from_own_thr = 15
opp_thr = 10
count_limit_perc = 75

def get_scores(count):
    pc2 = pd.DataFrame({'PlayerPosition': count['ReceiverPosition'], 'count': count['count']})
    scores = pd.concat([count[['PlayerPosition', 'count']], pc2]).groupby(['PlayerPosition']).sum()
    scores['position'] = scores.index

    return scores

def events_to_net_input(events, version_passes, version_phase):
    events = filter_phase(events, version_phase)
    passes = events.loc[events['EventType'] == 'Pass'].loc[events['OutcomeType'] == 'Successful']

    if version_passes == all_label:
        passes_count = passes.groupby(['PlayerPosition', 'ReceiverPosition']).size().reset_index().rename(columns={0:'count'}).sort_values('count')
        scores = get_scores(passes_count)
        passes_count = passes_count.loc[passes_count['count'] >= np.percentile(passes_count['count'], count_limit_perc)]

        xs, ys, positions = get_average_positions(events)

    if version_passes == progressive_label:
        passes_tmp = passes.copy()
        passes_tmp['vec_x'] = passes_tmp['EndX']-passes_tmp['StartX']
        passes_tmp['vec_y'] = passes_tmp['EndY']-passes_tmp['StartY']
        passes_tmp['vec_len'] = np.sqrt(passes_tmp['vec_x']**2 + passes_tmp['vec_y']**2)
        passes_tmp['cosine'] = passes_tmp.apply(lambda row: np.dot([row['vec_x'], row['vec_y']], ref_vec)/(row['vec_len']*ref_vec_len), axis=1)
        passes_tmp['length'] = np.sqrt((passes_tmp['StartX']-passes_tmp['EndX'])**2 + (passes_tmp['StartY']-passes_tmp['EndY'])**2)
        passes_tmp = passes_tmp.loc[passes_tmp['cosine'] > 1-cosine_threshold]

        own = passes_tmp.loc[(passes_tmp['StartX'] <= 52.5) & (passes_tmp['EndX'] <= 52.5) & (passes_tmp['length'] > own_thr)]
        from_own = passes_tmp.loc[(passes_tmp['StartX'] <= 52.5) & (passes_tmp['EndX'] > 52.5) & (passes_tmp['length'] > from_own_thr)]
        opp = passes_tmp.loc[(passes_tmp['StartX'] > 52.5) & (passes_tmp['EndX'] > 52.5) & (passes_tmp['length'] > opp_thr)]
        prog = pd.concat([own, from_own, opp])
        
        passes_count = prog.groupby(['PlayerPosition', 'ReceiverPosition']).size().reset_index().rename(columns={0:'count'}).sort_values('count')
        scores = get_scores(passes_count)
        passes_count = passes_count.loc[passes_count['count'] >= np.percentile(passes_count['count'], count_limit_perc)]

        xs, ys, positions = get_average_positions(events)

    if version_passes == long_label:
        long_events = passes
        long_events['length'] = np.sqrt((long_events['StartX']-long_events['EndX'])**2 + (long_events['StartY']-long_events['EndY'])**2)
        long_events = long_events.loc[long_events['length'] > 33]
        passes_count = long_events.groupby(['PlayerPosition', 'ReceiverPosition']).size().reset_index().rename(columns={0:'count'}).sort_values('count')
        scores = get_scores(passes_count)
        passes_count = passes_count.loc[passes_count['count'] >= np.percentile(passes_count['count'], count_limit_perc)]

        xs, ys, positions = get_average_positions(events)

    if version_passes == weighted_by_xt_label:
        pos_events = passes.loc[events['Xt'] > 0]
        values_count = pos_events.groupby(['PlayerPosition', 'ReceiverPosition'])['Xt'].sum().reset_index().rename(columns={'Xt':'count'})

        passes_count = pos_events.groupby(['PlayerPosition', 'ReceiverPosition']).size().reset_index().rename(columns={0:'count'}).sort_values('count')
        scores = get_scores(values_count)
        values_count = values_count.loc[values_count['count'] > np.percentile(values_count['count'], count_limit_perc)]

        xs, ys, positions = get_average_positions(events)
        passes_count = values_count

    scores = scores.loc[scores['position'].isin(positions)]
    missing_positions = np.setdiff1d(positions, scores['position'].values)

    if len(missing_positions) > 0:
        missing_df = pd.DataFrame({'position': missing_positions, 'count': 0})
        missing_df.index = missing_positions
        scores = pd.concat([scores, missing_df])
        scores = scores.reindex(positions)

    return passes_count, xs, ys, positions, scores
