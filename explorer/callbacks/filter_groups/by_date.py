from datetime import datetime as dt
from datetime import timedelta
from dash.dependencies import Input, Output, MATCH

from metadata.id_types import *
from metadata.keys import *


def by_date(app, db):
    @app.callback(
        [Output({'type': start_date_dropdown, id_index_team: MATCH}, min_date_allowed_prop),
         Output({'type': start_date_dropdown, id_index_team: MATCH}, date_prop),
         Output({'type': start_date_dropdown, id_index_team: MATCH}, initial_visible_month_prop),
         Output({'type': end_date_dropdown, id_index_team: MATCH}, max_date_allowed_prop),
         Output({'type': end_date_dropdown, id_index_team: MATCH}, date_prop),
         Output({'type': end_date_dropdown, id_index_team: MATCH}, initial_visible_month_prop)],
        [Input({'type': club_dropdown, id_index_team: MATCH}, value_prop)])
    def update_date_pickers(club):
        df = db.get_dates_by_clubid(club)
        return df[date_key].min(), \
               df[date_key].min(), \
               df[date_key].min(), \
               df[date_key].max(), \
               df[date_key].max(), \
               df[date_key].max()


    @app.callback(
        Output({'type': start_date_dropdown, id_index_team: MATCH}, max_date_allowed_prop),
        Input({'type': end_date_dropdown, id_index_team: MATCH}, date_prop))
    def first_date_set_max(first_date):
        try:
            return dt.strftime(
                dt.strptime(first_date, '%Y-%m-%d') - timedelta(1), '%Y-%m-%d')
        except ValueError:
            return dt.strftime(
                dt.strptime(first_date, '%Y-%m-%dT%H:%M:%S') - timedelta(1), '%Y-%m-%dT%H:%M:%S')


    @app.callback(
        Output({'type': end_date_dropdown, id_index_team: MATCH}, min_date_allowed_prop),
        Input({'type': start_date_dropdown, id_index_team: MATCH}, date_prop))
    def last_date_set_max(last_date):
        try:
            return dt.strftime(dt.strptime(last_date, '%Y-%m-%d') + timedelta(1), '%Y-%m-%d')
        except ValueError:
            return dt.strftime(
                dt.strptime(last_date, '%Y-%m-%dT%H:%M:%S') - timedelta(1), '%Y-%m-%dT%H:%M:%S')