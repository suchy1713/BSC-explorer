import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import networkx
from scipy.spatial import ConvexHull

from plots.utils_plotly import set_style, draw_field, hex_to_rgba
from plots.utils import get_hover_info

def get_perc(n_passes):
    perc = -3/1700*n_passes + 525/17

    if perc < 0:
        return 10
    if perc > 100:
        return 50
    return perc

def generate_hulls(actions, positions, cutoff_perc, scoring):
    hulls = []
    pointses = []
    scores = []
    new_positions = []
    not_plotted = []
    for _, position in zip(range(0, len(positions)), positions):
        try:
            actions_to_plot = actions.loc[actions['PlayerPosition'] == position]
            center = [actions_to_plot['StartX'].mean(), actions_to_plot['StartY'].mean()]

            actions_to_plot2 = actions_to_plot.copy()
            actions_to_plot['length'] = np.sqrt((center[0]-actions_to_plot['StartX'])**2 + (center[1]-actions_to_plot['StartY'])**2)
            actions_to_plot = actions_to_plot.loc[actions_to_plot['length'] <= np.percentile(actions_to_plot['length'], cutoff_perc)]
            points = actions_to_plot[['StartX', 'StartY']].values
            hull = ConvexHull(actions_to_plot[['StartX','StartY']])
            hulls.append(hull)
            pointses.append(points)
            scores.append(scoring(actions_to_plot2, actions, hull, points))
            new_positions.append(position)
        except:
            not_plotted.append(position)
            continue

    scores = np.array(scores)
    min_val = np.min(scores)
    max_val = np.max(scores)

    if min_val != max_val:
        scores = (scores-min_val)/((max_val-min_val)/(1-0)) + 0
    
    return new_positions, hulls, pointses, scores, not_plotted

colors = ['#1e90ff', 
          '#a9a9a9',
          '#ff8c00',
          '#32cd32',
          '#48d1cc',
          '#cd853f',
          '#ff69b4',
          '#ba55d3',
          '#ffff00',
          '#ff6347',
          '#f5DEB3']
colors = np.array(colors)

def plot_hulls(fig, new_positions, hulls, pointses, scores, infos):
    dic = {}
    base_color = '#1b4a21'
    max_alpha, min_alpha = 0.3, 0
    max_outline, min_outline = 2.3, 0.7
    outline = 1.3

    dummy_xs, dummy_ys = [], []
    dummy_pos = []
    for i, position, hull, points, score in zip(range(0, len(new_positions)), new_positions, hulls, pointses, scores):        
        xs = points[hull.vertices][:, 0]
        ys = points[hull.vertices][:, 1]

        xs = np.append(xs, xs[0])
        ys = np.append(ys, ys[0])

        if np.min(scores) == np.max(scores):
            width = outline
        else:
            width = (score-0)/((1-0)/(max_outline-min_outline)) + min_outline

        alpha = (score-0)/((1-0)/(max_alpha-min_alpha)) + min_alpha
        fig.add_trace(
                go.Scatter(
                    x=xs, y=ys,
                    mode='lines', 
                    line=dict(
                        color=hex_to_rgba(colors[i], 0.95),
                        width=width,
                    ), 
                    showlegend=False, 
                    fill="tonext", 
                    fillcolor=hex_to_rgba(base_color, 0),
                    hoverinfo='none'
                )
        )

        dummy_xs.append(np.mean(xs))
        dummy_ys.append(np.mean(ys))
        dummy_pos.append(position)

    max_font, min_font = 15, 7
    font = 9

    if np.min(scores) == np.max(scores):
        sizes = font
    else:
        sizes = (scores-0)/((1-0)/(max_font-min_font)) + min_font

    fig.add_trace(
        go.Scatter(
            x=dummy_xs, y=dummy_ys,
            text=[f'<b>{pos}</b>' for pos in dummy_pos],
            mode='markers+text', 
            textfont=dict(
                size=sizes,
                color=colors
            ),
            marker=dict(
                size=30,
                color=hex_to_rgba('#ffffff', 0)
            ), 
            customdata=infos,
            hovertemplate='%{customdata}<extra></extra>',
            showlegend=False
        )
    )

    return dic

def plot(events, positions, players, nineties, cutoff_perc, scoring):
    fig = go.Figure()
    set_style(fig)
    draw_field(fig)

    new_positions, hulls, pointses, scores, not_plotted = generate_hulls(events, positions, cutoff_perc, scoring)
    infos = get_hover_info(players, positions, nineties, not_plotted)
    plot_hulls(fig, new_positions, hulls, pointses, scores, infos)

    #fig.data = tuple([fig.data[-1]] + list(fig.data[:-1]))

    #print(fig.data)

    return fig
