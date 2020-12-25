import dash_bootstrap_components as dbc

from ui.components.plot_container import plot_container
from metadata.id_types import *
from metadata.keys import *


def content():
    return dbc.Row(
        dbc.CardColumns(
            [
                plot_container(plot_container_id, (id_index_coords, coords), coords[0], empty=True)
                for coords in ['00', '10', '01', '11']
            ],
            className='my-cards',
            style={'width': '100%'}
        ),
        className='content'
    )
