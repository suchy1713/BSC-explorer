from ast import literal_eval
import numpy as np
import pandas as pd
from dash import callback_context
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL, MATCH

from utils.get_intermid_output import get_intermid_output
from utils.get_formation_label import get_formation_label
from utils.group_formations import group_formations
from utils.json_service import load
from utils.sort_positions import sort_positions
from metadata.id_types import *
from metadata.keys import *
from metadata.strings import *
from metadata.viz_types import viz_filters


def build_preset_output(viz_filters_resolved, viz_filter_names):
    outputs = []
    for name in viz_filter_names:
        for coords in ['00', '10', '01', '11']:
            outputs.append(Output({'type': viz_filters_resolved[name].id_type, id_index_coords: coords}, value_prop))

    return outputs


def set_preset(app):
    viz_filters_resolved = viz_filters('')
    viz_filter_names = list(viz_filters_resolved.keys())

    @app.callback(
        [Output({'type': visual_dropdown, id_index_coords: coords}, value_prop) for coords in ['00', '10', '01', '11']],
        [Input(preset_dropdown, value_prop),
         Input(n_teams_dropdown, value_prop),
         Input(presets_storage, data_prop)])
    def update_viz_type(preset_name, n_teams, preset_data):
        preset_data = load(preset_data)
        n_teams = str(n_teams)

        preset = list(filter(lambda p: p.name == preset_name, preset_data[n_teams]))[0]
        viz_types = list(map(lambda x: preset.filter_values[x].viz_type, list(preset.filter_values.keys())))

        return viz_types


def intermid_version_dict(app):
    @app.callback(
        Output({'type': version_dict_storage, id_index_coords: MATCH}, data_prop),
        [Input({'type': f.id_type, id_index_coords: MATCH}, value_prop) for f in list(viz_filters('').values())])
    def save_versiondict(*args):
        version_dict = {}
        for name, value in zip(list(viz_filters('').keys()), args):
            version_dict[name] = value

        return version_dict


def generate_viz_filters(app):
    @app.callback(
        Output({'type': visual_filters_container, id_index_coords: MATCH}, children_prop),
        [Input({'type': visual_dropdown, id_index_coords: MATCH}, value_prop),
         Input(preset_dropdown, value_prop),
         Input(n_teams_dropdown, value_prop),
         Input(presets_storage, data_prop),
         Input({'type': events_storage, id_index_coords: MATCH}, data_prop)],
        [State({'type': visual_dropdown, id_index_coords: MATCH}, id_prop)])
    def generate_plot_filters(plot_label, preset_name, n_teams, preset_data, events_data, coords_id):
        index = coords_id[id_index_coords]

        preset_data = load(preset_data)
        n_teams = str(n_teams)
        preset = list(filter(lambda p: p.name == preset_name, preset_data[n_teams]))[0]

        content = []
        for filter_name, viz_filter in viz_filters(index).items():
            value = preset.filter_values[index].viz_filters[filter_name]

            if plot_label in viz_filter.display_on:
                if plot_label in [heatmap_attack, heatmap_defence]:
                    events_df = pd.read_json(events_data[intermid_events_key], orient='split')

                    players = events_df[position_key].unique()
                    receivers = events_df[receiver_position_key].unique()
                    players = players[~pd.isna(players)]
                    receivers = receivers[~pd.isna(receivers)]

                    positions = np.unique(
                        np.concatenate((
                            players,
                            receivers,
                        ))
                    )

                    value = sort_positions(positions)

                content.append(viz_filter.component(value))

            else:
                content.append([viz_filter.empty_component(value)])

        return [item for sublist in content for item in sublist]


def intermid_events(app, db):
    @app.callback(
        Output({'type': events_storage, id_index_coords: MATCH}, data_prop),
        Input({'type': formation_dropdown, id_index_coords: MATCH}, value_prop),
        State({'type': formations_storage, id_index_coords: MATCH}, data_prop))
    def retrieve_events(formation_vector, formations_storage_data):
        formations_df = pd.read_json(formations_storage_data[intermid_formations_key], orient='split')
        grouped = group_formations(formations_df)
        formation_label = get_formation_label(grouped, formation_vector)

        relevant_formations = formations_df.loc[formations_df[vector_key] == formation_vector]
        relevant_ids = relevant_formations[id_key].values
        events = db.get_events_by_formations(relevant_ids)
        players = db.get_players_by_formations(relevant_ids)

        intermid_dict = {
            intermid_events_key: events.to_json(date_format='iso', orient='split'),
            intermid_players_key: players.to_json(date_format='iso', orient='split'),
            intermid_nineties_key: relevant_formations[minutes_key].sum() / 90,
            intermid_formation_label_key: formation_label
        }

        return intermid_dict


def plot_type(app, db, coords):
    @app.callback(
        [Output({'type': formation_dropdown, id_index_coords: coords}, options_prop),
         Output({'type': formation_dropdown, id_index_coords: coords}, value_prop),
         Output({'type': formations_storage, id_index_coords: coords}, data_prop)],
        [Input({'type': club_dropdown, id_index_team: ALL}, value_prop),
         Input({'type': coach_dropdown, id_index_team: ALL}, value_prop),
         Input({'type': coach_dropdown, id_index_team: ALL}, options_prop),
         Input({'type': include_players_dropdown, id_index_team: ALL}, value_prop),
         Input({'type': include_players_dropdown, id_index_team: ALL}, options_prop),
         Input({'type': exclude_players_dropdown, id_index_team: ALL}, value_prop),
         Input({'type': exclude_players_dropdown, id_index_team: ALL}, options_prop),
         Input({'type': possession_slider, id_index_team: ALL}, value_prop),
         Input({'type': possession_slider, id_index_team: ALL}, min_prop),
         Input({'type': possession_slider, id_index_team: ALL}, max_prop),
         Input({'type': opposition_formation_dropdown, id_index_team: ALL}, value_prop),
         Input({'type': opposition_formation_dropdown, id_index_team: ALL}, options_prop),
         Input({'type': start_date_dropdown, id_index_team: ALL}, date_prop),
         Input({'type': start_date_dropdown, id_index_team: ALL}, min_date_allowed_prop),
         Input({'type': end_date_dropdown, id_index_team: ALL}, date_prop),
         Input({'type': end_date_dropdown, id_index_team: ALL}, max_date_allowed_prop),
         Input({'type': team_colors_storage, id_index_team: ALL}, data_prop)],
        [State(coords_lookup_storage, data_prop),
         State({'type': end_date_dropdown, id_index_team: ALL}, id_prop)])
    def retrieve_formations(clubs,
                            coaches,
                            coaches_options,
                            players_to_include,
                            players_to_include_options,
                            players_to_exclude,
                            players_to_exclude_options,
                            possession_vals,
                            possession_min,
                            possession_max,
                            opp_formation,
                            opp_formations_options,
                            start_dates,
                            start_dates_min,
                            end_dates,
                            end_dates_max,
                            colors,
                            lookup,
                            indexes):

        if not callback_context.triggered:
            raise PreventUpdate
        else:
            lookup = lookup['lookup']
            trigger_team_id = literal_eval(callback_context.triggered[0]['prop_id'].split('.')[0])[id_index_team]
            triggered = callback_context.triggered
            get_id = lambda x: literal_eval(x['prop_id'].split('.')[0])[id_index_team]
            get_id_func = np.vectorize(get_id)
            all_ids = np.unique(get_id_func(triggered))

            if not str(lookup[coords]) in all_ids:
                raise PreventUpdate
            else:
                return get_intermid_output(db, trigger_team_id, clubs, coaches, coaches_options,
                                           players_to_include, players_to_include_options, players_to_exclude,
                                           players_to_exclude_options, possession_vals, possession_min, possession_max,
                                           opp_formation, opp_formations_options, start_dates, start_dates_min,
                                           end_dates,
                                           end_dates_max, colors, indexes)
