import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from ui.css_rules import rules
from ui.filters_plot.plot_filters_content import plot_filters_content

content_coords = {
    'top_left': (0, 0),
    'bottom_left': (1, 0),
    'top_right': (0, 1),
    'bottom_right': (1, 1)
}

def get_items(app, db, team_id, coord, i):
    row, column = coord

    if i == 0:
        active_text = ' active'
        aria_sel = 'true'
    else:
        active_text = ''
        aria_sel = 'false'
    
    list_item = html.Li(
        html.A(
            get_label(*coord), 
            id=f'tablabel-{row}{column}', 
            className=f'nav-link{active_text}', 
            href=f"#tabcontent-{row}{column}", 
            role="tab", 
            **{'data-toggle': 'tab', 'aria-controls': f'tabcontent-{row}{column}', 'aria-selected': aria_sel}
        ), 
        className='tabs-4 nav-item'
    )

    content_item = html.Div([
                        html.Div(
                            plot_filters_content(app, db, team_id, row, column)
                        )], 
                        className=f'tab-pane{active_text} filters-tab-content',
                        id=f'tabcontent-{row}{column}',
                        role="tabpanel",
                        **{'aria-labelledby': f'tablabel-{row}{column}'},
                    )

    return list_item, content_item

def get_label(row, column):
    row_str = 'Top' if row == 0 else 'Bottom'
    col_str = 'Left' if column == 0 else 'Right'

    return f'{row_str} {col_str}'

def tabs(app, db, grid_coords, team_id):
    list_items, content_items = [], []

    for i, coord in zip(range(0, len(grid_coords)), grid_coords):
        list_item, content_item = get_items(app, db, team_id, coord, i)
        list_items.append(list_item)
        content_items.append(content_item)

    return html.Div(
        [
            html.Ul(
                list_items,
                id=f'tabs-filters-plot-{team_id}',
                className='nav-fill nav nav-tabs shadow-sm'
            ),
            html.Div(
                content_items,
                className='tab-content my-tab-content shadow'
            ),
        ], className='main-tab-content-small'
    )