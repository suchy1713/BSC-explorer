import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH

from ui.filters_plot.by_plot_type import by_plot_type
from ui.filters_team.filter_group_title import filter_group_title
from ui.filters_team.system.by_formation import by_formation

def plot_filters_content(app, db, team_id, row, column):
    return [
        *filter_group_title('Customize Plot'),
        *by_formation(app, db, team_id, row, column),
        *by_plot_type(app, db, row, column),
        html.Hr(),
        html.Div(id={'type': 'plot-filters-content', 'index-coords': f'{row}{column}'}),
        html.Div(id={'type': 'intermid-versionDict', 'index-coords': f'{row}{column}'}, style={'display': 'none'})
    ]