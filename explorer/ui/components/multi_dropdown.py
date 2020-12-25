import dash_core_components as dcc
import dash_html_components as html


def multi_dropdown(label, id_type, id_index, options=None, active_options=None):
    if options is None:
        options = []

    if active_options is None:
        active_options = []

    return [
        html.Label(label, className='form-label'),
        dcc.Dropdown(
            id={'type': id_type, id_index[0]: id_index[1]},
            clearable=False,
            searchable=False,
            multi=True,
            className='input',
            options=options,
            value=active_options
        )
    ]
