import dash_core_components as dcc
import dash_html_components as html

from ui.filters_team.system.by_formation import by_formation
from ui.filters_team.filter_group_title import filter_group_title
from ui.filters_plot.plot_filters_tabs import tabs

def by_system(app, db, team_id, grid_coords):
    return [
        tabs(app, db, grid_coords, team_id)
    ]