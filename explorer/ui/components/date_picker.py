import dash_core_components as dcc
import dash_html_components as html


def date_picker(label, id_type, id_index):
    return (
        html.Label(label, className='form-label'),
        dcc.DatePickerSingle(
            id={'type': id_type, id_index[0]: id_index[1]},
            clearable=False,
            display_format='YYYY-MM-DD',
            first_day_of_week=1,
            style={'display': 'block'},
            className='input'
        )
    )
