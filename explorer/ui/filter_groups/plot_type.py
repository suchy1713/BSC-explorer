import numpy as np
import dash_html_components as html
from ui.components.filter_group_title import filter_group_title
from ui.components.tabs_icons import tabs_icons
from ui.components.dropdown import dropdown
from ui.components.storage import storage
from utils.get_dropdown_input_from_list import get_dropdown_input_from_list
from metadata.strings import *
from metadata.keys import *
from metadata.id_types import *
from metadata.viz_types import vizzes


def content(coords):
    id_index = (id_index_coords, f'{coords[0]}{coords[1]}')

    return [
        *filter_group_title(plot_type_filter_group_title),
        *dropdown(formation_filter_label, formation_dropdown, id_index),
        *dropdown(visual_filter_label, visual_dropdown, id_index, get_dropdown_input_from_list(vizzes.keys()), 0),
        html.Hr(),
        html.Div(id={'type': visual_filters_container, id_index_coords: f'{coords[0]}{coords[1]}'}),
        storage({'type': formations_storage, id_index_coords: f'{coords[0]}{coords[1]}'}),
        storage({'type': events_storage, id_index_coords: f'{coords[0]}{coords[1]}'}),
        storage({'type': version_dict_storage, id_index_coords: f'{coords[0]}{coords[1]}'})
    ]


def plot_type(team_id, grid_coords):
    def fun(x): return lambda: content(x)

    return [
        tabs_icons(
            f'plot-filters-{team_id}',
            [
                fun(c) for c in grid_coords
            ],
            [
                str(i+1) for i in range(0, len(grid_coords))
            ]
        )
    ]
