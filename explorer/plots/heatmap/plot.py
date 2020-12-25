import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from plots.utils_plotly import set_style, draw_field, hex_to_rgba
from metadata.keys import *

bin_edges_x = [0, 16.5, 34.5, 52.5, 70.5, 88.5, 105]
bin_edges_y = [0, 13.85, 24.85, 43.15, 54.15, 68]

min_alpha = -0.2
max_alpha = 0.45

additional_lines = [
    {'x': [16.5, 16.5], 'y': [0, 13.85]},
    {'x': [16.5, 16.5], 'y': [54.15, 68]},
    {'x': [88.5, 88.5], 'y': [0, 13.85]},
    {'x': [88.5, 88.5], 'y': [54.15, 68]},
    {'x': [5.5, 16.5], 'y': [24.85, 24.85]},
    {'x': [5.5, 16.5], 'y': [43.15, 43.15]},
    {'x': [88.5, 99.5], 'y': [24.85, 24.85]},
    {'x': [88.5, 99.5], 'y': [43.15, 43.15]}
]


def draw_lines(fig, orientation, coords, to_exclude, color):
    for coord in coords:
        if coord in to_exclude:
            continue

        if orientation == 'vertical':
            xs = [coord, coord]
            ys = [0.25, 67.75]
        else:
            xs = [16.5, 88.5]
            ys = [coord, coord]

        fig.add_trace(
            go.Scatter(
                x=xs, y=ys,
                mode='lines',
                line=dict(
                    color=hex_to_rgba('#6e6e6e', 1),
                    width=1,
                    dash='dash'
                ),
                showlegend=False,
                hoverinfo='none'
            )
        )

    for line in additional_lines:
        fig.add_trace(
            go.Scatter(
                x=line['x'], y=line['y'],
                mode='lines',
                line=dict(
                    color=hex_to_rgba('#6e6e6e', 1),
                    width=1,
                    dash='dash'
                ),
                showlegend=False,
                hoverinfo='none'
            )
        )

    return fig


def draw_norm_heatmap(fig, events, color):
    heatmap, _, _ = np.histogram2d(
        events['StartX'],
        events['StartY'],
        bins=(bin_edges_x, bin_edges_y),
        range=((0, 105), (0, 68))
    )
    heatmap = heatmap.T
    norm_heatmap = heatmap.copy()
    heatmap = np.round(heatmap / heatmap.sum() * 100, 0)

    process_hmap_text_fun = lambda x: f"{'{0:g}'.format(x)}%" if x > 5 else ''
    process_hmap_text = np.vectorize(process_hmap_text_fun)
    heatmap = process_hmap_text(heatmap)

    for i in range(0, len(bin_edges_x)-1):
        for j in range(0, len(bin_edges_y)-1):
            area = (bin_edges_y[j+1]-bin_edges_y[j])*(bin_edges_x[i+1]-bin_edges_x[i])
            norm_heatmap[j][i] /= area

    norm_heatmap = (norm_heatmap-norm_heatmap.min())/((norm_heatmap.max()-norm_heatmap.min())/(max_alpha-min_alpha)) + min_alpha

    fig = go.Figure()
    set_style(fig)
    draw_field(fig)

    dummy_xs, dummy_ys = [], []
    for i in range(0, len(bin_edges_x)-1):
        for j in range(0, len(bin_edges_y)-1):
            x1 = bin_edges_x[i]
            x2 = bin_edges_x[i+1]
            y1 = bin_edges_y[j]
            y2 = bin_edges_y[j+1]

            dummy_xs.append((x2-x1)/2 + x1)
            dummy_ys.append((y2-y1)/2 + y1)

            if norm_heatmap[j][i] > 0:
                fig.add_trace(
                    go.Scatter(
                        x=[x1, x2, x2, x1, x1], y=[y1, y1, y2, y2, y1],
                        mode='lines',
                        line=dict(
                            color=hex_to_rgba(color, 0.05),
                            width=0,
                        ),
                        showlegend=False,
                        fill="tonext",
                        fillcolor=hex_to_rgba('#96783b', norm_heatmap[j][i]),
                        hoverinfo='none'
                    )
                )

    # fig.add_trace(
    #     go.Scatter(
    #         x=dummy_xs, y=dummy_ys,
    #         text=heatmap.flatten(order='F'),
    #         mode='markers+text',
    #         textfont=dict(
    #             size=12,
    #             color='#cdcdcd'
    #         ),
    #         marker=dict(
    #             size=30,
    #             color=hex_to_rgba('#ffffff', 0)
    #         ),
    #         # customdata=infos,
    #         # hovertemplate='%{customdata}<extra></extra>',
    #         showlegend=False
    #     )
    # )

    fig = draw_lines(fig, 'vertical', bin_edges_x, [0, 52.5, 105, 16.5, 88.5], color)
    fig = draw_lines(fig, 'horizontal', bin_edges_y, [0, 68], color)

    return fig


def plot(events, color):
    fig = go.Figure()
    set_style(fig)
    draw_field(fig)

    fig = draw_norm_heatmap(fig, events, color)

    return fig
