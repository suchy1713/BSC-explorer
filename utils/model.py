import pickle
import math
import numpy as np
import pandas as pd
from utils.utils import reverse_venue
from datetime import datetime
from utils.genetuning import correct_preds

def get_positions(model, X_df, verbosity=0, roles=True, only_predict=False):
    if only_predict:
        probas = model.predict_proba(X_df)*100
        labels = model.classes_
        proba_df = pd.DataFrame(probas, columns=labels)
        
        proba_df = correct_preds(proba_df, verbosity=1, use_absolute=False)
        proba_df['position'] = model.predict(X_df)
        n_fixed = (proba_df['position'] != proba_df['fixed_position']).sum()
        print(f"Fixed: {n_fixed}")
        if n_fixed > 0:
            print(proba_df[['position', 'fixed_position']])
        return proba_df['fixed_position']

    probas = model.predict_proba(X_df[features_X])*100
    preds = model.predict(X_df[features_X])
    labels = model.classes_
    proba_df = pd.DataFrame(probas, columns=labels).round(2)

    proba_df['name'] = X_df['name']#.apply(lambda x: x.split()[-1])
    proba_df['x'] = X_df['x']
    proba_df['y'] = X_df['y']
    proba_df['position'] = preds
    
    proba_df['team_name'] = X_df['team_name']
    proba_df['opposition'] = X_df['opposition_name']
    proba_df['filename'] = X_df['filename']

    proba_df = correct_preds(proba_df, verbosity=verbosity)
    
    if roles:
        proba_df = assign_roles(proba_df)

    return proba_df

def formation_to_label(formation):
    n_players = []

    #defenders
    n_players.append(formation['n_cb'].values[0] + 2)

    #3 or 4 lines?
    if formation['n_am'].values[0] > 0:
        n_players.append(formation['n_cm'].values[0] + formation['n_dm'].values[0])
        n_players.append(formation['n_am'].values[0] + formation['n_lw'].values[0] + formation['n_rw'].values[0])
        n_players.append(formation['n_st'].values[0])
    else:
        n_mid = formation['n_cm'].values[0] + formation['n_dm'].values[0]

        if n_mid >= 4:
            n_players.append('diamond')
        else:
            n_players.append(n_mid)
        n_players.append(formation['n_st'].values[0] + formation['n_lw'].values[0] + formation['n_rw'].values[0])

    n_players = np.array(n_players).astype(str)

    label = '-'.join(n_players)

    #disgusting, get rid of this asap
    if label == '4-2-4':
        label = '4-4-2'

    return label

def get_formation(data, venue, df):
    df = pd.DataFrame({
        'team_name': [data[f'{venue}_name']],
        'opposition': [data[f'{reverse_venue(venue)}_name']],
        'date': [data['date']],
        'season': [get_season(data['date'])],
        'competition': [data['competition']],
        'coach': [data[f'{venue}_coach']],
        'vector': [[
            df.loc[df['fixed_position'].isin(['LST', 'RST', 'ST'])].shape[0],
            df.loc[df['fixed_position'].isin(['LCB', 'RCB', 'CB'])].shape[0],
            df.loc[df['fixed_position'].isin(['LWB', 'LB'])].shape[0],
            df.loc[df['fixed_position'].isin(['RWB', 'RB'])].shape[0],
            df.loc[df['fixed_position'].isin(['LW'])].shape[0],
            df.loc[df['fixed_position'].isin(['RW'])].shape[0],
            df.loc[df['fixed_position'].isin(['AM'])].shape[0],
            df.loc[df['fixed_position'].isin(['DM', 'LDM', 'RDM'])].shape[0],
            df.loc[df['fixed_position'].isin(['LCM', 'CM', 'RCM'])].shape[0]
        ]],
        'n_st': [df.loc[df['fixed_position'].isin(['LST', 'RST', 'ST'])].shape[0]],
        'n_cb': [df.loc[df['fixed_position'].isin(['LCB', 'RCB', 'CB'])].shape[0]],
        'n_lb': [df.loc[df['fixed_position'].isin(['LWB', 'LB'])].shape[0]],
        'n_rb': [df.loc[df['fixed_position'].isin(['RWB', 'RB'])].shape[0]],
        'n_lw': [df.loc[df['fixed_position'].isin(['LW'])].shape[0]],
        'n_rw': [df.loc[df['fixed_position'].isin(['RW'])].shape[0]],
        'n_am': [df.loc[df['fixed_position'].isin(['AM', 'LAM', 'RAM'])].shape[0]],
        'n_dm': [df.loc[df['fixed_position'].isin(['DM', 'LDM', 'RDM'])].shape[0]],
        'n_cm': [df.loc[df['fixed_position'].isin(['LCM', 'CM', 'RCM'])].shape[0]]
    })

    df['label'] = formation_to_label(df)

    return df