import dash_core_components as dcc
import dash_html_components as html


def dropdown(label, id_type=None, id_index=None, options=None, active_option_idx=0, active_option=None, classic_id=None):
    if options is None:
        options = []

    if classic_id is not None:
        _id = classic_id
    else:
        _id = {'type': id_type, id_index[0]: id_index[1]}

    if active_option is not None:
        value = active_option
    else:
        value = options[active_option_idx]['value'] if len(options) > 0 else None

    return (
        html.Label(label, className='form-label'),
        dcc.Dropdown(
            options=options,
            id=_id,
            clearable=False,
            searchable=False,
            value=value,
            className='input'
        )
    )


def empty(id_type, id_index, options, value):
    return html.Div([
            dcc.Dropdown(
                options=options,
                id={'type': id_type, id_index[0]: id_index[1]},
                style={'display': 'none'},
                value=value
            )
        ])
