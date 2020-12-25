import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import json

from plots.passing_network.generate import generate_passing_network
from plots.territory_plot.generate import territory_plot_attack, territory_plot_defence
from plots.codes import Passes, Phases, passes_strings, phases_strings, version_strings
from ui.css_rules import rules
from ui.plot.get_color import get_color

plot_funcs = {
    'Pass Network': generate_passing_network,
    'Territory Plot - Attack': territory_plot_attack,
    'Territory Plot - Defence': territory_plot_defence
}

def get_subtitle(plot_type, version_dict):
    subtitle = ''

    subtitle += plot_type

    if not version_dict[phases_strings] in [0, None]:
        subtitle += f" - {phases_strings[version_dict['phase']]}"

        if not version_dict['passes'] in [0, None]:
            subtitle += f", {passes_strings[version_dict['passes']]}"

        return subtitle

    if not version_dict['passes'] in [0, None]:
        subtitle += f" - {passes_strings[version_dict['passes']]}"

    return subtitle

def get_graph(index, events, players, nineties, version_dict, plot_type, color):
    fig = plot_funcs[plot_type](events, players, nineties, version_dict, color)

    style = {'height': '40.48vh'}

    graph = dcc.Graph(
        id=f'graph-{index}',
        figure=fig,
        config={
            'responsive': True,
            'displayModeBar': False
        },
        style=style
    )

    return graph

margin = '5px'
def get_header(club, season, formation_text, filters_text, color, plot_type, version_dict):
    card_title_text = f"{club.split('_')[0]} {season}"
    card_subtitle_text = get_subtitle(plot_type, version_dict)
    return dbc.CardHeader([
        dbc.Row(
            [
                dbc.Col([
                    html.Div(card_title_text, style={'margin-bottom': '0'}, className='plot-card-title'),
                    html.Div(card_subtitle_text, style={'margin-bottom': '0', 'margin-top': '-3px'}, className='plot-card-subtitle')
                ], xs=6, style={'padding-left': margin}),
                dbc.Col([
                    html.Div(formation_text, style={'margin-bottom': '0'}, className='plot-card-subtitle'),
                    html.Div(filters_text, style={'margin-bottom': '0', 'margin-top': '0px'}, className='plot-card-subtitle')
                ], style={'text-align': 'right', 'padding-right': margin}, xs=6)
            ]
        )
    ], style={'border-color': color})

def get_footer(club, season, formation_text, filters_text, color, plot_type, version_dict):
    card_title_text = f"{club.split('_')[0]} {season}"
    card_subtitle_text = get_subtitle(plot_type, version_dict)
    return dbc.CardFooter([
        dbc.Row(
            [
                dbc.Col([
                    html.Div(card_title_text, style={'margin-bottom': '0'}, className='plot-card-title'),
                    html.Div(card_subtitle_text, style={'margin-bottom': '0', 'margin-top': '-3px'}, className='plot-card-subtitle')
                ], xs=6, style={'padding-left': margin}),
                dbc.Col([
                    html.Div(formation_text, style={'margin-bottom': '0'}, className='plot-card-subtitle'),
                    html.Div(filters_text, style={'margin-bottom': '0', 'margin-top': '0px'}, className='plot-card-subtitle')
                ], style={'text-align': 'right', 'padding-right': margin}, xs=6)
            ]
        )
    ], style={'border-color': color})

def get_body_style(row):
    if row == 0:
        return {'margin-top': '0rem', 'margin-bottom': '0rem', 'text-align': 'center', 'color': rules['color']}
    else:
        return {'padding-top': '0rem', 'padding-bottom': '0rem', 'text-align': 'center', 'color': rules['color']}

def reverse(i):
    return 1 if i == 0 else 0

def plot_container(app, row, column, reversed=False):
    return [dbc.CardBody(
            style=get_body_style(row),
            id={'type': 'plot-container-body', 'index-coords': f'{row}{column}'}
        ), html.Div(
            str(reversed),
            style={'display': 'none'},
            id={'type': 'reversed', 'index-coords': f'{row}{column}'}
        )]