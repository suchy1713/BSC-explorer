import dash_core_components as dcc
import dash_html_components as html

from ui.css_rules import rules
from ui.filters_team.by_team import by_team
from ui.filters_team.by_player import by_player
from ui.filters_team.by_opposition import by_opposition
from ui.filters_team.by_date import by_date
from ui.filters_team.by_system import by_system

content_funcs = {
    'team': by_team,
    'player': by_player,
    'opposition': by_opposition,
    'date': by_date,
    'system': by_system
}

def get_items(app, db, team_id, item_id, i, grid_coords):
    if i == 0:
        active_text = ' active'
        aria_sel = 'true'
    else:
        active_text = ''
        aria_sel = 'false'
    
    list_item = html.Li(
        html.A(
            html.Img(
                src=app.get_asset_url(f'filter_icons/{item_id}.png'),
                className='tab-icon'
            ), 
            id=f'{item_id}-{team_id}-tab', 
            className=f'nav-link{active_text}', 
            href=f"#{item_id}-{team_id}", 
            role="tab", 
            **{'data-toggle': 'tab', 'aria-controls': f'{item_id}-{team_id}', 'aria-selected': aria_sel}
        ), 
        className='tabs-5 nav-item'
    )

    content_item = html.Div([
                        html.Div(
                            content_funcs[item_id](app, db, team_id, grid_coords)
                        )], 
                        className=f'tab-pane{active_text} filters-tab-content',
                        id=f'{item_id}-{team_id}',
                        role="tabpanel",
                        **{'aria-labelledby': f'{item_id}-{item_id}-tab'},
                    )

    return list_item, content_item

def tabs(app, db, team_id, grid_coords):
    list_items, content_items = [], []
    item_ids = list(content_funcs.keys())
    for i, item_id in zip(range(0, len(item_ids)), item_ids):
        list_item, content_item = get_items(app, db, team_id, item_id, i, grid_coords)
        list_items.append(list_item)
        content_items.append(content_item)

    return html.Div(
        [
            html.Ul(
                list_items,
                id=f'tabs-filters-{team_id}',
                className='nav-fill nav nav-tabs shadow-sm'
            ),
            html.Div(
                content_items,
                className='tab-content my-tab-content shadow'
            ),
        ], className='main-tab-content'
    )