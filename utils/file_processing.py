import pandas as pd
import numpy as np
from utils.events import exclude_corners, filter_by_venue, get_longest_period, get_coords
from utils.features import get_features
import operator

def parse_raw(data, venue):
    events = exclude_corners(pd.DataFrame(data['events']))
    events = filter_by_venue(events, data, venue)
    events, period = get_longest_period(events, data, venue)

    x, y, names, ids, gk = get_coords(events)

    df = get_features(x, y, names, ids, events)

    return df, gk, period


avg_touches_per_interval = 120
def parse_raw_ensemble(data, venue, verbosity=1):
    events = exclude_corners(pd.DataFrame(data['events']))
    events = filter_by_venue(events, data, venue)
    events, period = get_longest_period(events, data, venue)
    passes = events.loc[(events['isTouch'] == True) | (events['isDefAction'] == True)]
    
    interval = int((period[1]-period[0]) * (avg_touches_per_interval/passes.shape[0]))

    gks = {}
    for i in range(int(np.floor(period[0])), int(np.ceil(period[1]-interval-1))):
        events_limited = events.loc[(events['time_minutes'] >= i) & (events['time_minutes'] <= i+interval)]
        _, _, _, _, gk = get_coords(events_limited)

        if gk['id'] in list(gks.keys()):
            gks[gk['id']] += 1
        else:
            gks[gk['id']] = 1

    gk = max(gks.items(), key=operator.itemgetter(1))[0]

    x, y, names, _, _ = get_coords(events, gk)
    coord_df = pd.DataFrame({'x': x, 'y': y, 'name': names})

    dfs = []
    n_events = []
    for i in range(int(np.floor(period[0])), int(np.ceil(period[1]-interval-1))):
        events_limited = events.loc[(events['time_minutes'] >= i) & (events['time_minutes'] <= i+interval)]
        n_events.append(events_limited.loc[(events_limited['isTouch'] == True) | (events_limited['isDefAction'] == True)].shape[0])

        x, y, names, ids, gk_obj = get_coords(events_limited, gk)
        df = get_features(x, y, names, ids, events_limited)
        dfs.append(df)

    if verbosity > 0:
        print(f'Number of Periods: {len(n_events)}')
        print(f'Interval: {interval}')
        print(f'Avg Actions/Period: {np.mean(n_events)}')

    return dfs, period, gk_obj, coord_df