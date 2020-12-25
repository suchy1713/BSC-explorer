from dash.dependencies import Input, Output

from utils.get_dropdown_input_from_list import get_dropdown_input_from_list
from utils.json_service import load
from metadata.id_types import *
from metadata.keys import *


def layout_filters(app):
    @app.callback(
        Output(coords_lookup_storage, data_prop),
        Input(n_teams_dropdown, value_prop))
    def save_lookup_coords(n_teams):
        if n_teams == 1:
            lookup = {'00': 1, '10': 1, '01': 1, '11': 1}
            inverted_lookup = {1: [(0, 0), (1, 0), (0, 1), (1, 1)]}
        elif n_teams == 2:
            lookup = {'00': 1, '10': 1, '01': 2, '11': 2}
            inverted_lookup = {1: [(0, 0), (1, 0)], 2: [(0, 1), (1, 1)]}
        elif n_teams == 4:
            lookup = {'00': 1, '10': 2, '01': 3, '11': 4}
            inverted_lookup = {1: [(0, 0)], 2: [(1, 0)], 3: [(0, 1)], 4: [(1, 1)]}

        return {
            lookup_key: lookup,
            inverted_lookup_key: inverted_lookup,
            n_teams_key: n_teams
        }

    @app.callback(
        [Output(preset_dropdown, options_prop),
         Output(preset_dropdown, value_prop)],
        [Input(n_teams_dropdown, value_prop),
         Input(presets_storage, data_prop)])
    def update_preset_dropdown(n_teams, presets_data):
        presets_data = load(presets_data)
        n_teams = str(n_teams)

        presets = presets_data[n_teams]
        names = map(lambda preset: preset.name, presets)
        options = get_dropdown_input_from_list(names)

        return options, options[0]['value']
