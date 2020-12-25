import numpy as np
from dash.dependencies import Input, Output, MATCH

from utils.get_dropdown_input import get_dropdown_input
from metadata.id_types import *
from metadata.keys import *


def by_opposition(app, db):
    @app.callback(
        [Output({'type': opposition_formation_dropdown, id_index_team: MATCH}, options_prop),
         Output({'type': opposition_formation_dropdown, id_index_team: MATCH}, value_prop)],
        [Input({'type': club_dropdown, id_index_team: MATCH}, value_prop)])
    def update_opp_formation_dropdown(club):
        df = db.get_opposition_formations_by_clubid(club)
        options = get_dropdown_input(df, label_key, vector_key)
        return options, df['value'].values

    @app.callback(
        [Output({'type': possession_slider, id_index_team: MATCH}, value_prop),
         Output({'type': possession_slider, id_index_team: MATCH}, min_prop),
         Output({'type': possession_slider, id_index_team: MATCH}, max_prop)],
        [Input({'type': club_dropdown, id_index_team: MATCH}, value_prop)])
    def update_possession_slider(club):
        df = db.get_possession_by_clubid(club)
        possession_vals = df[possession_key].values * 100

        min_val = np.floor(possession_vals[0])
        max_val = np.ceil(possession_vals[-1])

        return [min_val, max_val], min_val, max_val
