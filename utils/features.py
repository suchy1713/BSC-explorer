import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from scipy.stats import circmean

ref_vector = [10, 0] / np.linalg.norm([10, 0])
sp_x = 10
sp_y = 10

def norm(arr):
    return (arr - arr.min())/(arr.max()-arr.min())

def find_nearest(array, value):
    if len(array) == 0:
        return -1

    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def get_def_actions(names, events):
    events = events.loc[events['isDefAction'] == True]
    new_names, xs, ys, ns = [], [], [], []
    for name in names:
        player_df = events.loc[events['player'] == name]

        if player_df.shape[0] > 0:
            new_names.append(name)
            xs.append(np.mean(player_df['start_x']))
            ys.append(np.mean(player_df['start_y']))
            ns.append(player_df.shape[0])

    coords = pd.DataFrame({'name': new_names, 'x': xs, 'y': ys, 'actions': ns})

    return coords

def get_min_hull_positions(names, events):
    touches = events.loc[events['isTouch'] == True]
    passes = events.loc[events['type'] == 'Pass'].loc[events['outcomeType'] == 'Successful']

    xs = []
    for name in names:
        player_touches = touches.loc[touches['player'] == name]
        player_receivals = passes.loc[passes['receiver'] == name]
        player_receivals = pd.DataFrame({'player': player_receivals['receiver'], 'start_x': player_receivals['end_x'], 'start_y': player_receivals['end_y']})
        player_touches = player_touches[['player', 'start_x', 'start_y']]
        player_touches = pd.concat([player_touches, player_receivals])

        try:
            center_x = player_touches['start_x'].mean()
            player_touches['distance_x'] = np.abs(center_x-player_touches['start_x'])
            
            player_touches = player_touches.loc[player_touches['distance_x'] <= np.percentile(player_touches['distance_x'], 35)]
            hull = ConvexHull(player_touches[['start_x','start_y']])
            points = player_touches[['start_x', 'start_y']].values
            vertices_xs = points[hull.vertices][:, 0]
            xs.append(np.min(vertices_xs))
        except:
            xs.append(np.median(player_touches['start_x']))

    return pd.DataFrame({'name': names, 'x': xs})

def argmax2d(X):
    n, m = X.shape
    x_ = np.ravel(X)
    k = np.argmax(x_)
    i, j = k // m, k % m
    return i, j

def get_bins(events):
    try:
        n_bins = (7, 5)
        heatmap, _, _ = np.histogram2d(events['start_x'], events['start_y'], bins=n_bins, range=((0, 105), (0, 68)))
        heatmap = heatmap.T

        return argmax2d(heatmap)
    except Exception:
        print('hmap exception')
        return 0, 0

def get_features(xs, ys, names, ids, events):
    df = pd.DataFrame({
        'name': names,
        'id': ids,
        'x': xs,
        'y': ys,
        'left': 0,
        'right': 0,
        'min_hull_left': 0,
        'min_hull_right': 0,
        'up': 0,
        'down': 0,
        'angle': 0,
        'local_left': 0,
        'local_right': 0,
        'local_up': 0,
        'local_down': 0,
        'nearest_left': 0,
        'nearest_right': 0,
        'nearest_top': 0,
        'nearest_bottom': 0,
        'hull_left': 0,
        'hull_right': 0,
        'hull_top': 0,
        'hull_bottom': 0,
        'hull_volume': 0,
        'centrality': 0,
        'avg_pass_length': 0,
        'avg_pass_angle': 0,
        'avg_receival_angle': 0,
        'left_defensive': 0,
        'right_defensive': 0,
        'up_defensive': 0,
        'bottom_defensive': 0,
        'def_actions': 0,
        'y_deviation': 0,
        'x_deviation': 0
    })
    def_df = get_def_actions(names, events)
    min_hull_positions = get_min_hull_positions(names, events)

    for i, row in df.iterrows():
        df.loc[i, 'left'] = df.loc[df['x'] < row['x']].shape[0]
        df.loc[i, 'right'] = df.loc[df['x'] > row['x']].shape[0]
        df.loc[i, 'up'] = df.loc[df['y'] > row['y']].shape[0]
        df.loc[i, 'down'] = df.loc[df['y'] < row['y']].shape[0]

        vector = [105-row['x'], 34-row['y']]
        df.loc[i, 'angle'] = np.arccos(np.dot(ref_vector, vector / np.linalg.norm(vector)))

        df.loc[i, 'local_left'] = df.loc[df['x'] < row['x']].loc[df['y'] <= row['y']+sp_y].loc[df['y'] >= row['y']-sp_y].shape[0]
        df.loc[i, 'local_right'] = df.loc[df['x'] > row['x']].loc[df['y'] <= row['y']+sp_y].loc[df['y'] >= row['y']-sp_y].shape[0]
        df.loc[i, 'local_up'] = df.loc[df['y'] > row['y']].loc[df['x'] <= row['x']+sp_x].loc[df['x'] >= row['x']-sp_x].shape[0]
        df.loc[i, 'local_down'] = df.loc[df['y'] < row['y']].loc[df['x'] <= row['x']+sp_x].loc[df['x'] >= row['x']-sp_x].shape[0]

        horizontal = df.loc[i, 'local_left'] + df.loc[i, 'local_right'] + 1e-15
        vertical = df.loc[i, 'local_up'] + df.loc[i, 'local_down'] + 1e-15

        df.loc[i, 'local_left'] /= horizontal
        df.loc[i, 'local_right'] /= horizontal
        df.loc[i, 'local_up'] /= vertical
        df.loc[i, 'local_down'] /= vertical

        nl = find_nearest(df.loc[df['x'] < row['x']]['x'], row['x'])
        df.loc[i, 'nearest_left'] = nl if nl == -1 else np.abs(nl-row['x']) / (df['x'].max() - df['x'].min())

        nr = find_nearest(df.loc[df['x'] > row['x']]['x'], row['x'])
        df.loc[i, 'nearest_right'] = nr if nr == -1 else np.abs(nr-row['x']) / (df['x'].max() - df['x'].min())

        nt = find_nearest(df.loc[df['y'] > row['y']]['y'], row['y'])
        df.loc[i, 'nearest_top'] = nt if nt == -1 else np.abs(nt-row['y']) / (df['x'].max() - df['x'].min())

        nb = find_nearest(df.loc[df['y'] < row['y']]['y'], row['y'])
        df.loc[i, 'nearest_bottom'] = nb if nb == -1 else np.abs(nb-row['y']) / (df['x'].max() - df['x'].min())

        events = events.loc[events['isTouch'] == True]
        team_x_max = events['start_x'].max()
        player_passes_made = events.loc[events['player'] == row['name']][['player', 'jersey_number', 'start_x', 'start_y', 'end_x', 'end_y', 'xt', 'time_minutes']]
        player_receivals = events.loc[events['receiver'] == row['name']]
        player_receivals = pd.DataFrame(
            {'player': player_receivals['receiver'],
            'jersey_number': player_receivals['receiver_jersey'],
            'start_x': player_receivals['end_x'],
            'start_y': player_receivals['end_y'],
            'end_x': 0,
            'end_y': 0,
            'xt': 0,
            'time_minutes': player_receivals['time_minutes']})
        player_passes = pd.concat([player_passes_made, player_receivals])
        player_passes['y_deviation'] = 34 - player_passes['start_y']
        player_passes['x_deviation'] = team_x_max - player_passes['start_x']

        df.loc[i, 'y_deviation'] = np.mean(np.abs(player_passes['y_deviation']))
        df.loc[i, 'x_deviation'] = np.mean(np.abs(player_passes['x_deviation']))

        if player_passes[player_passes['y_deviation'] < 0].shape[0] > player_passes.shape[0]/2:
            df.loc[i, 'y_deviation'] *= -1

        if row['name'] in def_df['name'].values:
            pl_def_x = def_df.loc[def_df['name'] == row['name']]['x'].values[0]
            pl_def_y = def_df.loc[def_df['name'] == row['name']]['y'].values[0]

            df.loc[i, 'left_defensive'] = def_df.loc[def_df['x'] < pl_def_x].shape[0]
            df.loc[i, 'right_defensive'] = def_df.loc[def_df['x'] > pl_def_x].shape[0]
            df.loc[i, 'bottom_defensive'] = def_df.loc[def_df['y'] < pl_def_y].shape[0]
            df.loc[i, 'up_defensive'] = def_df.loc[def_df['y'] > pl_def_y].shape[0]
            df.loc[i, 'def_actions'] = def_df.loc[def_df['name'] == row['name']]['actions'].values[0]
        else:
            df.loc[i, 'left_defensive'] = row['left']
            df.loc[i, 'right_defensive'] = row['right']
            df.loc[i, 'bottom_defensive'] = row['down']
            df.loc[i, 'up_defensive'] = row['up']
            df.loc[i, 'def_actions'] = 0

        pl_hull_min_x = min_hull_positions.loc[min_hull_positions['name'] == row['name']]['x'].values[0]

        df.loc[i, 'min_hull_left'] = min_hull_positions.loc[min_hull_positions['x'] < pl_hull_min_x].shape[0]
        df.loc[i, 'min_hull_right'] = min_hull_positions.loc[min_hull_positions['x'] > pl_hull_min_x].shape[0]

        try:
            center = [player_passes['start_x'].mean(), player_passes['start_y'].mean()]
            player_passes['distance'] = np.sqrt((center[0]-player_passes['start_x'])**2 + (center[1]-player_passes['start_y'])**2)
            player_passes = player_passes.loc[player_passes['distance'] <= np.percentile(player_passes['distance'], 55)]
            hull = ConvexHull(player_passes[['start_x','start_y']])
            points = player_passes[['start_x', 'start_y']].values
            xs = points[hull.vertices][:, 0]
            ys = points[hull.vertices][:, 1]
            center = np.mean(xs), np.mean(ys)
            df.loc[i, 'hull_volume'] = hull.volume
            df.loc[i, 'hull_left'] = center[0] - xs.min()
            df.loc[i, 'hull_right'] = xs.max() - center[0]
            df.loc[i, 'hull_bottom'] = center[1] - ys.min()
            df.loc[i, 'hull_top'] = ys.max() - center[1]
            df.loc[i, 'posadj_hull_x'] = xs.max() - xs.min()
            df.loc[i, 'posadj_hull_y'] = ys.max() - ys.min()
        except:
           pass

        player_passes_made['length'] = np.sqrt((player_passes_made['end_x']-player_passes_made['start_x'])**2 + (player_passes_made['end_y']-player_passes_made['start_y'])**2)
        df.loc[i, 'centrality'] = player_passes_made.shape[0]
        df.loc[i, 'avg_pass_length'] = player_passes_made['length'].mean()

        player_passes_made = events.loc[events['player'] == row['name']].loc[events['type'] == 'Pass'].loc[events['outcomeType'] == 'Successful']
        
        vectors_x = player_passes_made['end_x']-player_passes_made['start_x']
        vectors_y = player_passes_made['end_y']-player_passes_made['start_y']

        ref_vector2 = [10, 0] / np.linalg.norm([10, 0])
        angles = []
        for vx, vy in zip(vectors_x, vectors_y):
            angle = np.arccos(np.dot(ref_vector2, [vx, vy]/np.linalg.norm([vx, vy])))
            if vy < 0:
                angle *= -1
            angles.append(angle)

        df.loc[i, 'avg_pass_angle'] = circmean(angles)


        vectors_x = player_receivals['end_x']-player_receivals['start_x']
        vectors_y = player_receivals['end_y']-player_receivals['start_y']

        ref_vector2 = [10, 0] / np.linalg.norm([10, 0])
        angles = []
        for vx, vy in zip(vectors_x, vectors_y):
            angle = np.arccos(np.dot(ref_vector2, [vx, vy]/np.linalg.norm([vx, vy])))
            if vy < 0:
                angle *= -1
            angles.append(angle)

        df.loc[i, 'avg_receival_angle'] = circmean(angles)




    df['angle'] = norm(df['angle'])
    df['left_defensive'] = norm(df['left_defensive'])
    df['right_defensive'] = norm(df['right_defensive'])
    df['up_defensive'] = norm(df['up_defensive'])
    df['bottom_defensive'] = norm(df['bottom_defensive'])
    df['def_actions'] = norm(df['def_actions'])
    df['left'] = norm(df['left'])
    df['right'] = norm(df['right'])
    df['min_hull_left'] = norm(df['min_hull_left'])
    df['min_hull_right'] = norm(df['min_hull_right'])
    df['up'] = norm(df['up'])
    df['down'] = norm(df['down'])
    df['hull_left'] /= 105
    df['hull_right'] /= 105
    df['hull_top'] /= 68
    df['hull_bottom'] /= 68
    df['hull_volume'] = norm(df['hull_volume'])
    df['centrality'] = norm(df['centrality'])
    df['avg_pass_length'] = norm(df['avg_pass_length'])
    df['x_deviation'] = norm(df['x_deviation'])
    df.loc[df['y_deviation'] >= 0, 'y_deviation'] = norm(df.loc[df['y_deviation'] >= 0]['y_deviation'])
    df.loc[df['y_deviation'] < 0, 'y_deviation'] = (1 - norm(df.loc[df['y_deviation'] < 0]['y_deviation']))*(-1)
    #df['avg_pass_angle'] = norm(df['avg_pass_angle'])

    return df