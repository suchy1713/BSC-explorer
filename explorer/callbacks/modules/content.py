import pandas as pd
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
from dash import callback_context

from ui.components.card_title_bar import card_title_bar
from ui.components.plot_container import plot_container, plot_container_content
from ui.components.plot import plot
from utils.get_card_subtitle import get_card_subtitle
from metadata.id_types import *
from metadata.keys import *
from metadata.viz_types import vizzes


def get_card_title(club):
    return f"{club.split('_')[0]} {club.split('_')[1]}"


def content(app):
    @app.callback(
        [Output({'type': plot_container_id, id_index_coords: '00'}, children_prop),
         Output({'type': plot_container_id, id_index_coords: '10'}, children_prop),
         Output({'type': plot_container_id, id_index_coords: '01'}, children_prop),
         Output({'type': plot_container_id, id_index_coords: '11'}, children_prop)],
        Input(vertical_checkbox, value_prop))
    def update_vertical(value):
        if len(value) > 0:
            return plot_container_content((id_index_coords, '00')), \
                   plot_container_content((id_index_coords, '10')), \
                   plot_container_content((id_index_coords, '01')), \
                   plot_container_content((id_index_coords, '11')),
        else:
            return plot_container_content((id_index_coords, '00')), \
                   plot_container_content((id_index_coords, '01'), True), \
                   plot_container_content((id_index_coords, '10'), True), \
                   plot_container_content((id_index_coords, '11')),

    @app.callback(
        Output({'type': plot_container_body_id, id_index_coords: MATCH}, children_prop),
        [Input({'type': version_dict_storage, id_index_coords: MATCH}, data_prop),
         Input({'type': reversed_div_id, id_index_coords: MATCH}, children_prop)],
        [State({'type': visual_dropdown, id_index_coords: MATCH}, value_prop),
         State({'type': formations_storage, id_index_coords: MATCH}, data_prop),
         State({'type': events_storage, id_index_coords: MATCH}, data_prop),
         State({'type': visual_dropdown, id_index_coords: MATCH}, id_prop)])
    def generate_plot(version_dict, should_reverse, viz_type, formations, events, id_name):
        # import numpy as np
        # from ast import literal_eval
        #
        # triggered = callback_context.triggered
        # get_id = lambda x: literal_eval(x['prop_id'].split('.')[0])['type']
        # get_id_func = np.vectorize(get_id)
        # all_ids = np.unique(get_id_func(triggered))
        # print(all_ids)

        index = id_name[id_index_coords]
        row = int(str(index)[0])

        if should_reverse == 'True':
            row = 1 if row == 0 else 0

        try:
            events_df = pd.read_json(events[intermid_events_key], orient='split')
            players_df = pd.read_json(events[intermid_players_key], orient='split')
            nineties = events[intermid_nineties_key]
            color = formations[intermid_team_color_key]
            club = formations[intermid_club_id_key]
        except TypeError:
            raise PreventUpdate

        fig = vizzes[viz_type].generate_func(events_df, players_df, nineties, version_dict, color)
        plot_instance = plot(fig, plot_id(index))

        card_title_text = get_card_title(club)
        card_subtitle_text = get_card_subtitle(viz_type, version_dict)
        formation_label = events[intermid_formation_label_key]
        filters_label = formations[intermid_filters_label_key]
        title_bar = card_title_bar(
            card_title_text,
            card_subtitle_text,
            formation_label,
            filters_label,
            row, color
        )

        card_content = [title_bar, plot_instance]

        if row == 1:
            card_content = card_content[::-1]

        return card_content
