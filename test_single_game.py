import streamlit as st
import xgboost
import pickle
import json
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils.events import get_avg_def_actions, get_longest_period, exclude_gk
from utils.file_processing import parse_raw, parse_raw_ensemble
from utils.PositionClassifier import columns as cols
from utils.PositionClassifier import PositionClassifier
from utils.genetuning import correct_preds
from utils.roles import assign_roles

# with open('model/4_model/brain.xgb', 'rb') as handle:
#     model = pickle.load(handle)

posClassifier = PositionClassifier('model/4_model/brain.xgb')

from utils.field import draw_field
from utils.plot import set_style

def init_plot():
    fig = plt.figure(figsize=(15, 10))
    ax = plt.axes([0.05, 0.05, 0.9, 0.9])
    set_style()
    draw_field(ax, correct_aspect=True, arrow=False)

    return fig, ax

color_pos = {
    'CB': 'tan',
    'RCB': 'goldenrod',
    'LCB': 'darkkhaki',
    'LB': 'springgreen',
    'LWB': 'springgreen',
    'RB': 'slategrey',
    'RWB': 'slategrey',
    'DM': 'mediumorchid',
    'LCM': 'plum',
    'RCM': 'hotpink',
    'LDM': 'deeppink',
    'RDM': 'fuchsia',
    'CM': 'purple',
    'LAM': 'darkorchid',
    'RAM': 'darkorchid',
    'AM': 'darkorchid',
    'LW': 'darkturquoise',
    'RW': 'tomato',
    'RST': 'navy',
    'LST': 'navy',
    'ST': 'navy',
}

ovr_pos = {
    'CB': 'CB',
    'RCB': 'CB',
    'LCB': 'CB',
    'LB': 'LB',
    'LWB': 'LB',
    'RB': 'RB',
    'RWB': 'RB',
    'DM': 'CM',
    'LCM': 'CM',
    'RCM': 'CM',
    'LDM': 'CM',
    'RDM': 'CM',
    'CM': 'CM',
    'LAM': 'CM',
    'RAM': 'CM',
    'AM': 'CM',
    'LW': 'LW',
    'RW': 'RW',
    'RST': 'ST',
    'LST': 'ST',
    'ST': 'ST',
}

def get_bold_styles(x):
    styles = ['', '']

    for i in ['CB', 'CM', 'LB', 'LW', 'RB', 'RW', 'ST']:
        if ovr_pos[x['adjusted']] == i:
            styles.append('font-weight: bold')
        else:
            styles.append('')
    
    return styles

def plot_plot(dfs, coord_df):
    proba_df, _ = posClassifier.ensemble_predict_proba(dfs, coord_df, verbosity=1)

    fig, ax = init_plot()
    ax.scatter(
        proba_df['x'],
        proba_df['y'],
        marker='o',
        s=500,
        linewidths=3,
        edgecolors='0.65',
        zorder=1000,
        c=proba_df['fixed_position'].map(color_pos)
    )

    for _, row in proba_df.iterrows():
        try:
            ax.annotate(f"{row['name'].split()[-1]} ({row['fixed_position']})", (row['x'], row['y']-3.2), ha='center', zorder=1001, fontsize=14)
        except Exception:
            print('whoops')

    st.pyplot(fig, dpi=300)

    proba_df['adjusted'] = proba_df['fixed_position']
    proba_df['name'] = proba_df['name'].apply(lambda x: f"{x.split(' ')[0][0]}. {x.split(' ')[-1]}")
    proba_df = proba_df.sort_values('position')
    show = proba_df[['name', 'position', 'adjusted', 'CB', 'CM', 'LB', 'LW', 'RB', 'RW', 'ST']]
    show = show.set_index(['name'])

    show = show.style.set_precision(1).background_gradient(cmap='Greens', low=0, high=2, axis=None)
    
    show.apply(get_bold_styles, axis=1)

    st.table(show)


f = st.file_uploader('Raw JSON')
if f is not None:
    data = json.load(f)

    st.markdown('<h3>Home</h3>', unsafe_allow_html=True)
    dfs, _, _, coord_df = parse_raw_ensemble(data, 'home')
    plot_plot(dfs, coord_df)

    st.markdown('<h3>Away</h3>', unsafe_allow_html=True)
    dfs, _, _, coord_df = parse_raw_ensemble(data, 'away')
    plot_plot(dfs, coord_df)   