import numpy as np
import math

def get_3cm_assignment(cms):
    cms_y = cms.sort_values('y')
    cms_x = cms.sort_values('x')

    ref_vector2 = [0, 10] / np.linalg.norm([0, 10])

    if cms_x.iloc[0]['y'] < cms_x.iloc[1]['y']:
        deep_vector = [cms_x.iloc[1]['x'] - cms_x.iloc[0]['x'], cms_x.iloc[1]['y'] - cms_x.iloc[0]['y']]
    else:
        deep_vector = [cms_x.iloc[0]['x'] - cms_x.iloc[1]['x'], cms_x.iloc[0]['y'] - cms_x.iloc[1]['y']]
    deep_angle = np.arccos(np.dot(ref_vector2, deep_vector/np.linalg.norm(deep_vector)))

    if cms_x.iloc[1]['y'] < cms_x.iloc[2]['y']:
        high_vector = [cms_x.iloc[2]['x'] - cms_x.iloc[1]['x'], cms_x.iloc[2]['y'] - cms_x.iloc[1]['y']]
    else:
        high_vector = [cms_x.iloc[1]['x'] - cms_x.iloc[2]['x'], cms_x.iloc[1]['y'] - cms_x.iloc[2]['y']]
    high_angle = np.arccos(np.dot(ref_vector2, high_vector/np.linalg.norm(high_vector)))

    if np.abs(math.degrees(deep_angle)-math.degrees(high_angle)) < 15:
        #d=(x−x1)(y2−y1)−(y−y1)(x2−x1)
        d=(cms_y.iloc[1]['x']-cms_y.iloc[0]['x'])*(cms_y.iloc[2]['y']-cms_y.iloc[0]['y'])-(cms_y.iloc[1]['y']-cms_y.iloc[0]['y'])*(cms_y.iloc[2]['x']-cms_y.iloc[0]['x'])
        
        if d<=0:
            cms.loc[cms_y.iloc[1].name, 'fixed_position'] = 'DM'
            cms.loc[cms_y.iloc[0].name, 'fixed_position'] = 'RCM'
            cms.loc[cms_y.iloc[2].name, 'fixed_position'] = 'LCM'
        else:
            cms.loc[cms_y.iloc[1].name, 'fixed_position'] = 'AM'
            cms.loc[cms_y.iloc[0].name, 'fixed_position'] = 'RDM'
            cms.loc[cms_y.iloc[2].name, 'fixed_position'] = 'LDM'
    else:
        if deep_angle < high_angle:
            cms.loc[cms_x.iloc[2].name, 'fixed_position'] = 'AM'

            if cms_x.iloc[1]['y'] < cms_x.iloc[0]['y']:
                cms.loc[cms_x.iloc[1].name, 'fixed_position'] = 'RDM'
                cms.loc[cms_x.iloc[0].name, 'fixed_position'] = 'LDM'
            else:
                cms.loc[cms_x.iloc[1].name, 'fixed_position'] = 'LDM'
                cms.loc[cms_x.iloc[0].name, 'fixed_position'] = 'RDM'
        else:
            cms.loc[cms_x.iloc[0].name, 'fixed_position'] = 'DM'

            if cms_x.iloc[1]['y'] < cms_x.iloc[2]['y']:
                cms.loc[cms_x.iloc[1].name, 'fixed_position'] = 'RCM'
                cms.loc[cms_x.iloc[2].name, 'fixed_position'] = 'LCM'
            else:
                cms.loc[cms_x.iloc[1].name, 'fixed_position'] = 'LCM'
                cms.loc[cms_x.iloc[2].name, 'fixed_position'] = 'RCM'

    return cms

cm_dict = {
    'DM': 'DM',
    'LDM': 'DM',
    'RDM': 'DM',
    'LCM': 'CM',
    'RCM': 'CM',
    'AM': 'AM',
    None: None
}
def get_4cm_assignment(cms):
    indexes = list(cms.index)
    partial = np.array([
        np.insert(get_3cm_assignment(cms.iloc[[0, 1, 2]])['fixed_position'].values, 3, [None]),
        np.insert(get_3cm_assignment(cms.iloc[[0, 1, 3]])['fixed_position'].values, 2, [None]),
        np.insert(get_3cm_assignment(cms.iloc[[0, 2, 3]])['fixed_position'].values, 1, [None]),
        np.insert(get_3cm_assignment(cms.iloc[[1, 2, 3]])['fixed_position'].values, 0, [None])
    ])
    partial = np.vectorize(cm_dict.get)(partial)

    n_all_dms = 0
    for cm_ass in partial.T:
        if len(cm_ass[cm_ass == 'DM']) == 3:
            n_all_dms += 1

    cms_y = cms.sort_values('y')
    cms_x = cms.sort_values('x')
    #2-2
    if n_all_dms == 2 or n_all_dms == 0:
        if cms_x.iloc[0]['y'] < cms_x.iloc[1]['y']:
            cms.loc[cms_x.iloc[0].name, 'fixed_position'] = 'RDM'
            cms.loc[cms_x.iloc[1].name, 'fixed_position'] = 'LDM'
        else:
            cms.loc[cms_x.iloc[0].name, 'fixed_position'] = 'LDM'
            cms.loc[cms_x.iloc[1].name, 'fixed_position'] = 'RDM'

        if cms_x.iloc[2]['y'] < cms_x.iloc[3]['y']:
            cms.loc[cms_x.iloc[2].name, 'fixed_position'] = 'RAM'
            cms.loc[cms_x.iloc[3].name, 'fixed_position'] = 'LAM'
        else:
            cms.loc[cms_x.iloc[2].name, 'fixed_position'] = 'LAM'
            cms.loc[cms_x.iloc[3].name, 'fixed_position'] = 'RAM'
    #1-2-1
    else:
        deep_cm = cms_y.loc[cms_x.iloc[[0, 1, 2]].index].sort_values('y')
        deep_cm = deep_cm.iloc[1]
        cms.loc[deep_cm.name, 'fixed_position'] = 'DM'

        other_cms = cms.loc[cms.index != deep_cm.name]

        ref_vector = [10, 0] / np.linalg.norm([10, 0])
        for i, row in other_cms.iterrows():
            vector = [row['x'] - deep_cm['x'], row['y'] - deep_cm['y']]
            other_cms.loc[i, 'angle'] = np.arccos(np.dot(ref_vector, vector/np.linalg.norm(vector)))

        am_idx = other_cms['angle'].idxmin()
        cms.loc[am_idx, 'fixed_position'] = 'AM'

        other_cms = other_cms.loc[other_cms.index != am_idx]

        if other_cms.iloc[0]['y'] < other_cms.iloc[1]['y']:
            cms.loc[other_cms.iloc[0].name, 'fixed_position'] = 'RCM'
            cms.loc[other_cms.iloc[1].name, 'fixed_position'] = 'LCM'
        else:
            cms.loc[other_cms.iloc[0].name, 'fixed_position'] = 'LCM'
            cms.loc[other_cms.iloc[1].name, 'fixed_position'] = 'RCM'


    return cms

def assign_roles(df):
    #CBs
    if df.loc[df['fixed_position'].isin(['LCB', 'CB', 'RCB'])].shape[0] == 1:
        cb_idx = df.loc[df['fixed_position'].isin(['LCB', 'CB', 'RCB'])]['y'].idxmax()
        df.loc[cb_idx, 'fixed_position'] = 'CB' 
    else:   
        lcb_idx = df.loc[df['fixed_position'].isin(['LCB', 'CB', 'RCB'])]['y'].idxmax()
        df.loc[lcb_idx, 'fixed_position'] = 'LCB'
        
        rcb_idx = df.loc[df['fixed_position'].isin(['LCB', 'CB', 'RCB'])]['y'].idxmin()
        df.loc[rcb_idx, 'fixed_position'] = 'RCB'

    #LWB RWB
    if df.loc[df['fixed_position'].isin(['LCB', 'CB', 'RCB'])].shape[0] == 3:
        if df.loc[df['fixed_position'] == 'LB'].shape[0] > 0:
            lb_idx = df.loc[df['fixed_position'] == 'LB']['y'].idxmax()
            df.loc[lb_idx, 'fixed_position'] = 'LWB'

        if df.loc[df['fixed_position'] == 'RB'].shape[0] > 0:
            rb_idx = df.loc[df['fixed_position'] == 'RB']['y'].idxmax()
            df.loc[rb_idx, 'fixed_position'] = 'RWB'

    #CMs
    if df.loc[df['fixed_position'] == 'CM'].shape[0] == 2:
        ldm_idx = df.loc[df['fixed_position'] == 'CM']['y'].idxmax()
        df.loc[ldm_idx, 'fixed_position'] = 'LDM'

        rdm_idx = df.loc[df['fixed_position'] == 'CM']['y'].idxmin()
        df.loc[rdm_idx, 'fixed_position'] = 'RDM'
    elif df.loc[df['fixed_position'] == 'CM'].shape[0] == 3:
        cms = df.loc[df['fixed_position'] == 'CM']
        df.loc[df['fixed_position'] == 'CM', 'fixed_position'] = get_3cm_assignment(cms)['fixed_position']

    elif df.loc[df['fixed_position'] == 'CM'].shape[0] == 4:
        cms = df.loc[df['fixed_position'] == 'CM']
        df.loc[df['fixed_position'] == 'CM', 'fixed_position'] = get_4cm_assignment(cms)['fixed_position']

    #ST
    if df.loc[df['fixed_position'].isin(['ST'])].shape[0] > 1:
        lst_idx = df.loc[df['fixed_position'] == 'ST']['y'].idxmax()
        df.loc[lst_idx, 'fixed_position'] = 'LST'

        rst_idx = df.loc[df['fixed_position'] == 'ST']['y'].idxmax()
        df.loc[rst_idx, 'fixed_position'] = 'RST'

    return df