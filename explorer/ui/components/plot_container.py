import dash_bootstrap_components as dbc
import dash_html_components as html

from assets.css_rules import plot_container_rules
from metadata.id_types import *


def plot_container_content(id_index, should_reverse=False):
    return [
        dbc.CardBody(
            id={'type': plot_container_body_id, id_index[0]: id_index[1]}
        ),
        html.Div(
            str(should_reverse),
            style={'display': 'none'},
            id={'type': reversed_div_id, id_index[0]: id_index[1]}
        )
    ]


def plot_container(id_type, id_index, row, should_reverse=False, empty=False):
    margin = plot_container_rules['margin-top-top'] if row == '0' else plot_container_rules['margin-top-bottom']

    if empty:
        child = []
    else:
        child = plot_container_content(id_index, should_reverse)

    return dbc.Card(
        child,
        className='shadow div-card-bg',
        id={'type': id_type, id_index[0]: id_index[1]},
        style={
            'height': plot_container_rules['height'],
            'margin-top': margin,
            'width': plot_container_rules['width']
        }
    )
