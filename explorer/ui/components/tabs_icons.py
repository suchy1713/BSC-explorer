import dash_html_components as html
import dash_bootstrap_components as dbc


def get_items(tabs_component_id, content, icon, i):
    if i == 0:
        active_text = ' active'
        aria_sel = 'true'
    else:
        active_text = ''
        aria_sel = 'false'

    if icon[-3:] in ['png', 'jpg']:
        label = html.Img(
            src=icon,
            className='tab-icon'
        )
    else:
        label = icon

    list_item = html.Li(
        html.A(
            label,
            id=f'{i}-{tabs_component_id}-tab',
            className=f'nav-link{active_text}',
            href=f"#{i}-{tabs_component_id}",
            role="tab",
            **{'data-toggle': 'tab', 'aria-controls': f'{i}-{tabs_component_id}', 'aria-selected': aria_sel}
        ),
        className='tabs-5 nav-item'
    )

    content_item = html.Div([
        html.Div(
            content()
        )],
        className=f'tab-pane{active_text} filters-tab-content',
        id=f'{i}-{tabs_component_id}',
        role="tabpanel",
        **{'aria-labelledby': f'{i}-{tabs_component_id}-tab'},
    )

    return list_item, content_item


def tabs_icons(tabs_component_id, content_funcs, icons):
    list_items, content_items = [], []
    for i, icon, content in zip(range(0, len(icons)), icons, content_funcs):
        list_item, content_item = get_items(tabs_component_id, content, icon, i)
        list_items.append(list_item)
        content_items.append(content_item)

    return html.Div(
        [
            html.Ul(
                list_items,
                id=f'{tabs_component_id}-list',
                className='nav-fill nav nav-tabs shadow-sm'
            ),
            html.Div(
                content_items,
                className='tab-content my-tab-content shadow'
            ),
        ], className='main-tab-content'
    )
