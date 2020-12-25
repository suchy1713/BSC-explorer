import dash_core_components as dcc
import dash_html_components as html


def range_slider(label, id_type, id_index):
    return (
        html.Label(label, className='form-label'),
        dcc.RangeSlider(
            id={'type': id_type, id_index[0]: id_index[1]},
            min=0,
            max=100,
            value=[0, 100],
            pushable=1,
            tooltip={'placement': 'bottom'},
            className='input'
        )
    )
