import dash_html_components as html
import dash_bootstrap_components as dbc


def tabs(tabs_component_id, content_funcs, labels, tab_ids, active_tab_id_idx, display=None):
    if display is None:
        display = [True]*len(content_funcs)

    return html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(
                        content(),
                        label=label,
                        id=tab_id,
                        tab_id=tab_id,
                        style={} if display else {'display': 'none'}
                    ) for content, label, tab_id, dis in zip(content_funcs, labels, tab_ids, display)
                ],
                id=tabs_component_id,
                active_tab=tab_ids[active_tab_id_idx],
                className='nav-fill shadow-sm'
            )
        ]
    )
