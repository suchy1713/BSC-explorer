import dash_html_components as html

from ui.filter_groups.filter_groups import *
from ui.components.tabs_icons import tabs_icons


def team_filters(app, team_id, grid_coords, seasons):
    return tabs_icons(
        f'team-filters-{team_id}',
        [
            lambda: by_team(team_id, seasons),
            lambda: by_players(team_id),
            lambda: by_opposition(team_id),
            lambda: by_date(team_id),
            lambda: plot_type(team_id, grid_coords)
        ],
        [
            app.get_asset_url(f'filter_icons/team.png'),
            app.get_asset_url(f'filter_icons/player.png'),
            app.get_asset_url(f'filter_icons/opposition.png'),
            app.get_asset_url(f'filter_icons/date.png'),
            app.get_asset_url(f'filter_icons/system.png')
        ]
    )
