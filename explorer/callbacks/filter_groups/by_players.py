from dash.dependencies import Input, Output, MATCH

from utils.get_dropdown_input import get_dropdown_input
from metadata.id_types import *
from metadata.keys import *


def by_players(app, db):
    @app.callback(
        [Output({'type': include_players_dropdown, id_index_team: MATCH}, options_prop),
         Output({'type': include_players_dropdown, id_index_team: MATCH}, value_prop),
         Output({'type': exclude_players_dropdown, id_index_team: MATCH}, options_prop),
         Output({'type': exclude_players_dropdown, id_index_team: MATCH}, value_prop)],
        [Input({'type': club_dropdown, id_index_team: MATCH}, value_prop)])
    def retrieve_players(club):
        df = db.get_players_by_clubid(club)
        options = get_dropdown_input(df, name_key, id_key)
        return options, [], options, []
