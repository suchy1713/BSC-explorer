import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import plotly.express as px

import matplotlib.pyplot as plt

import sys
sys.path.append('../../')
from utils.field import draw_field
from utils.plot import set_style

def get_position_filename(filename):
    position_filename = list(filename)
    position_filename[0] = 'p'
    position_filename = ''.join(position_filename)

    return position_filename

st.set_page_config(
    page_title="Label Positions",
    page_icon="🧊",
    layout="wide"
)

directory = '../1_generate_features/data/'
save_directory = 'data/'
is_there_a_file = False
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        position_filename = get_position_filename(filename)

        if position_filename not in os.listdir(save_directory):
            is_there_a_file = True
            break

if is_there_a_file:
    cols = st.beta_columns([0.15, 0.02, 0.15, 0.05, 0.62])

    df = pd.read_csv(directory + filename)
    with cols[4]:
        st.write(filename)
    df['name_to_display'] = df['name'].apply(lambda x: x.split(' ')[-1])

    colors = {'CB': '#805d08', 'LB': 'olive', 'RB': 'olive', 'CM': '#873a87', 'LW': 'tomato', 'RW': 'tomato', 'ST': '#2c2c94'}
    positions = ['CB', 'LB', 'RB', 'CM', 'LW', 'RW', 'ST']
    positions = np.array(positions)
    inputs = []
    for player, i in zip(df['name'].values, range(0, df.shape[0])):
        s = player
        if i < 5:
            with cols[0]:
                inputs.append(st.selectbox(s, positions))
        else:
            with cols[2]:
                inputs.append(st.selectbox(s, positions))


    with cols[2]:
        if st.button('Submit'):
            df['position'] = inputs
            df[['name', 'position']].to_csv(save_directory + position_filename, index=False)

    fig = px.scatter(data_frame=df,
                        x='x', 
                        y='y',
                        text='name_to_display'
        )

    fig.update_traces(marker=dict(size=16,
                                color=list(map(colors.get, inputs)),
                                line=dict(width=2,
                                        color='#333333')),
                    selector=dict(mode='markers+text'))

    fig.update_layout(
        paper_bgcolor="#131313",
        plot_bgcolor='rgba(50,50,50,50)',
        font_family="Lato",
        font_color="#cdcdcd"
    )

    fig.update_xaxes(range=(0, 105), visible=False)
    fig.update_yaxes(range=(0, 68), visible=False)

    with cols[4]:
        st.plotly_chart(fig)

else:
    st.info('No files to label')