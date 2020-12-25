import pandas as pd
import numpy as np

corner_threshold = 2
ko_threshold=1


def exclude_corners(passes):
    corners = passes.loc[passes['StartX'] > 105-corner_threshold].loc[(passes['StartY'] > 68-corner_threshold) | (passes['StartY'] < corner_threshold)]
    passes = pd.concat([passes, corners]).drop_duplicates(keep=False)

    throw_ins = passes.loc[(passes['StartY'] == 0) | (passes['StartY'] == 68)]
    passes = pd.concat([passes, throw_ins]).drop_duplicates(keep=False)

    kick_offs = passes.loc[(52.5-ko_threshold < passes['StartX']) & (passes['StartX'] < 52.5+ko_threshold) & (34-ko_threshold < passes['StartY']) & (passes['StartY'] < 34+ko_threshold)]
    passes = pd.concat([passes, kick_offs]).drop_duplicates(keep=False)

    return passes


def get_hover_info(players, positions, nineties, not_plotted=[]):
    strings = []
    for pos in positions:
        if not (pos in not_plotted):
            pos_players = players.loc[players['position'] == pos]
            pos_players = pos_players[['name', 'minutes']].groupby('name').apply(
                lambda df: pd.Series({
                    'Name': df['name'].values[0],
                    'MinutesPercent': (df['minutes'].sum()/90)/nineties*100
                })
            )

            pos_players = pos_players.sort_values('MinutesPercent', ascending=False)
            pos_players.index = np.arange(0, pos_players.shape[0])
            
            pos_players['string'] = (pos_players.index+1).astype(str) + '. ' + pos_players['Name'] + ' (' + pos_players['MinutesPercent'].apply(lambda x: '{0:g}'.format(np.round(x, 1))) + '%)'
            pos_players = pos_players.head(3)

            string = '<b>Players:</b><br>' + '<br>'.join(pos_players['string'].values)

            strings.append(string)

    return strings

def reduce_vector(start, end, by_end, by_start):
    v_coord = np.array([end[0]-start[0], end[1]-start[1]])
    v_length = np.linalg.norm(v_coord)

    v_coord_for_end = v_coord/v_length*(v_length-by_end)
    v_coord_for_start = v_coord/v_length*(v_length-by_start)

    new_end = (v_coord_for_end[0] + start[0], v_coord_for_end[1] + start[1])
    new_start = (end[0] - v_coord_for_start[0], end[1] - v_coord_for_start[1])
    
    return new_start, new_end

def combine_events_and_receivals(passes):
    passes = passes.loc[passes['EventType'] == 'Pass'].loc[passes['OutcomeType'] == 'Successful']
    passes2 = pd.DataFrame({'PlayerPosition': passes['ReceiverPosition'], 'StartX': passes['EndX'], 'StartY': passes['EndY'], 'Xt': 0, 'TimeMinutes': passes['TimeMinutes']})
    passes = passes[['PlayerPosition', 'Xt', 'StartX', 'StartY', 'TimeMinutes']]
        
    return pd.concat([passes, passes2])

bu_percentile = 50
def get_buildup(passes, receivals=True):
    passes = passes.loc[passes['StartX'] <= np.percentile(passes['StartX'], bu_percentile)]
    return passes

fin_percentile = 60
def get_finishing(passes, receivals=True):
    passes = passes.loc[passes['StartX'] >= np.percentile(passes['StartX'], fin_percentile)]
    return passes

def get_average_positions(events):
    events = events.loc[events['IsTouch'] == True]
    positions = np.unique(events['PlayerPosition'])

    xs, ys = [], []
    for PlayerPosition in positions:
        position_touches = events.loc[events['PlayerPosition'] == PlayerPosition]
        position_touches = position_touches[['StartX', 'StartY']]
        position_receivals = events.loc[events['ReceiverPosition'] == PlayerPosition]
        position_receivals = pd.DataFrame(
            {'StartX': position_receivals['EndX'],
            'StartY': position_receivals['EndY']})
        position_touches = pd.concat([position_touches, position_receivals])

        xs.append(np.median(position_touches['StartX']))
        ys.append(np.median(position_touches['StartY']))

    return np.array(xs), np.array(ys), positions

bu_percentile = 50
fin_percentile = 60
from metadata.strings import *
def filter_phase(passes, phase):
    if phase == all_label:
        return passes

    if phase == build_up_label:
        return passes.loc[passes['StartX'] <= np.percentile(passes['StartX'], bu_percentile)]

    if phase == finishing_label:
        return passes.loc[passes['StartX'] >= np.percentile(passes['StartX'],fin_percentile)]