import pandas as pd
import numpy as np
from utils.utils import reverse_venue
from math import isnan

corner_threshold = 2
def exclude_corners(passes):
    corners = passes.loc[passes['start_x'] > 105-corner_threshold].loc[(passes['start_y'] > 68-corner_threshold) | (passes['start_y'] < corner_threshold)]
    passes = pd.concat([passes, corners]).drop_duplicates(keep=False)

    throw_ins = passes.loc[(passes['start_y'] == 0) | (passes['start_y'] == 68)]
    passes = pd.concat([passes, throw_ins]).drop_duplicates(keep=False)

    return passes

def get_longest_period(events, data, venue):
    subs = pd.DataFrame(data[f'{venue}_subs'])

    if subs.shape[0] > 0:
        minutes = subs['time_minutes'].values
        minutes = np.append(minutes, [events.time_minutes.max()])
        minutes = np.insert(minutes, 0, 0)
    else:
        minutes = np.array([0, events.time_minutes.max()])

    periods = []
    for i in range(0, len(minutes)-1):
        periods.append((minutes[i], minutes[i+1]))

    mins = np.array([per[1]-per[0] for per in periods])
    final_period = periods[mins.argmax()]
    
    return events.loc[events['time_minutes'] < final_period[1]].loc[events['time_minutes'] > final_period[0]], final_period

def get_avg_def_actions(df):
    print(df['player'].isna().sum())
    names = np.unique(df['player'].loc[~(df['player'].isna())])
    xs, ys = [], []

    for name in names:
        player_df = df.loc[df['player'] == name]
        xs.append(np.mean(player_df['start_x']))
        ys.append(np.mean(player_df['start_y']))

    return xs, ys, names

def get_average_positions(events):
    names, ids = [], []
    jerseys = np.unique(events['jersey_number'])
    def_act = events.loc[(events['isDefAction'] == True)]
    events = events.loc[(events['isTouch'] == True)]
    team_passes = events.loc[events['type'] == 'Pass']

    xs, ys = [], []
    for jersey in jerseys:
        player_events = events.loc[events['jersey_number'] == jersey]
        player_def = def_act.loc[def_act['jersey_number'] == jersey]
        player_passes = team_passes.loc[team_passes['jersey_number'] == jersey]
        id = player_events['playerId'].values
        
        passes = events.loc[events['type'] == 'Pass'].loc[events['outcomeType'] == 'Successful']
        passes = passes.loc[passes['receiver_jersey'] == jersey]
        receivals = pd.DataFrame({'player': passes['receiver'], 'start_x': passes['end_x'], 'start_y': passes['end_y']})
        player_events = player_events[['player', 'start_x', 'start_y']]
        player_events = pd.concat([player_events, player_def])
        
        # func = np.median #np.median
        # func2 = np.median

        # t = (func2(player_events['start_x']), func2(player_events['start_y']))
        # d = (func(player_def['start_x']), func(player_def['start_y']))
        # gamma = 0.7

        # xs.append(gamma*t[0] + (1-gamma)*d[0])
        # ys.append(gamma*t[1] + (1-gamma)*d[1])
        
        xs.append(player_events['start_x'].mean())
        ys.append(player_events['start_y'].mean())

        name = player_events['player'].values
        if len(name) > 0:
            names.append(name[0])
        else:
            names.append('')

        if len(id) > 0:
            ids.append(id[0])
        else:
            ids.append(-150)
    
    return np.array(xs), np.array(ys), np.array(jerseys), np.array(names), np.array(ids)

def exclude_gk(xs, ys, names, ids, gk_id=None):
    if gk_id == None:
        empty_idxs = np.where(names == '')
        xs, ys, names, ids = np.delete(xs, empty_idxs), np.delete(ys, empty_idxs), np.delete(names, empty_idxs), np.delete(ids, empty_idxs)
        
        gk_idx = np.argmin(xs)
        gk = {
            'name': names[gk_idx],
            'id': ids[gk_idx]
        }
        xs, ys, names, ids = np.delete(xs, gk_idx), np.delete(ys, gk_idx), np.delete(names, gk_idx), np.delete(ids, gk_idx)
        
    else:
        gk_idx = np.where(ids == gk_id)[0]
        gk_name = names[gk_idx]
        gk = {'name': gk_name, 'id': ids[gk_idx]}
        xs, ys, names, ids = np.delete(xs, gk_idx), np.delete(ys, gk_idx), np.delete(names, gk_idx), np.delete(ids, gk_idx)

        empty_idxs = np.where(names == '')
        xs, ys, names, ids = np.delete(xs, empty_idxs), np.delete(ys, empty_idxs), np.delete(names, empty_idxs), np.delete(ids, empty_idxs)

    return xs, ys, names, ids, gk


def get_coords(events, gk=None):
    xs, ys, _, names, ids = get_average_positions(events)
    xs, ys, names, ids, gk = exclude_gk(xs, ys, names, ids, gk)

    return xs, ys, names, ids, gk

def filter_by_venue(events, data, venue):
    return events.loc[events['team_name'] == data[f'{venue}_name']]

def label_positions(data, venue, positions):
    pos_dict = dict(zip(positions['name'], positions['fixed_position']))
    events = pd.DataFrame(data['events'])

    events = exclude_corners(events)
    events = events.loc[events['team_name'] == data[f'{venue}_name']]
    events = before_subs(events, data[f'{venue}_subs'])
    events['opposition'] = data[f'{reverse_venue(venue)}_name']
    events['game_date'] = data['date']
    events['competition'] = data['competition']
    events['player_position'] = events['player'].map(pos_dict)

    passes = events.loc[events['type'] == 'Pass'].loc[events['outcomeType'] == 'Successful']
    events = pd.concat([events, passes]).drop_duplicates(keep=False)

    passes['receiver_position'] = passes['receiver'].map(pos_dict)
    events['receiver_position'] = None

    passes.loc[passes['receiver_position'].isna(), 'receiver_position'] = 'GK'
    events = pd.concat([events, passes]).sort_values('time_minutes')
    events.loc[events['player_position'].isna(), 'player_position'] = 'GK'

    return events

def add_gk(positions, gk):
    new_df = pd.DataFrame({'id': [gk['id'][0]], 'name': [gk['name'][0]], 'fixed_position': ['GK']})
    return positions.append(new_df, ignore_index=True)