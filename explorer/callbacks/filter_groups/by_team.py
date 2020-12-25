from dash.dependencies import Input, Output, MATCH

from utils.get_dropdown_input import get_dropdown_input
from metadata.id_types import *
from metadata.keys import *


def by_team(app, db):
    @app.callback(
        [Output({'type': league_dropdown, id_index_team: MATCH}, options_prop),
         Output({'type': league_dropdown, id_index_team: MATCH}, value_prop)],
        [Input({'type': season_dropdown, id_index_team: MATCH}, value_prop)])
    def update_league_dropdown(season):
        df = db.get_leagues_by_season(season)
        options = get_dropdown_input(df, league_key, league_key)
        return options, options[0]['value']

    @app.callback(
        [Output({'type': club_dropdown, id_index_team: MATCH}, options_prop),
         Output({'type': club_dropdown, id_index_team: MATCH}, value_prop),
         Output({'type': team_colors_storage, id_index_team: MATCH}, data_prop)],
        [Input({'type': season_dropdown, id_index_team: MATCH}, value_prop),
         Input({'type': league_dropdown, id_index_team: MATCH}, value_prop)])
    def update_club_dropdown(season, league):
        df = db.get_clubs_by_league_and_season(league, season)
        options = get_dropdown_input(df, name_key, id_key)
        return options, options[0]['value'], df[[id_key, color_key]].to_json(date_format='iso', orient='split')

    @app.callback(
        [Output({'type': coach_dropdown, id_index_team: MATCH}, options_prop),
         Output({'type': coach_dropdown, id_index_team: MATCH}, value_prop)],
        [Input({'type': club_dropdown, id_index_team: MATCH}, value_prop)])
    def update_coaches_dropdown(club):
        df = db.get_coaches_by_clubid(club)
        options = get_dropdown_input(df, coach_key, coach_key)
        return options, df['value'].values
