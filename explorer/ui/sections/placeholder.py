import dash_html_components as html
import dash_core_components as dcc

from metadata.id_types import *
from metadata.keys import *
from metadata.viz_types import *


def get_placeholder():
    coords = ['00', '01', '10', '11']
    types = [events_storage, formations_storage, version_dict_storage]

    viz_filters_resolved = viz_filters('')
    viz_filters_types = list(map(lambda x: x.id_type, list(viz_filters_resolved.values())))

    divs = []
    for coord in coords:
        divs.append(dcc.Dropdown(id={'type': formation_dropdown, id_index_coords: coord}, style={'display': 'none'}))
        divs.append(dcc.Dropdown(id={'type': visual_dropdown, id_index_coords: coord}, style={'display': 'none'}))
        for _type in types:
            divs.append(
                dcc.Store(id={'type': _type, id_index_coords: coord})
            )
        for _type in viz_filters_types:
            divs.append(
                dcc.Dropdown(id={'type': _type, id_index_coords: coord}, style={'display': 'none'})
            )

    return divs
