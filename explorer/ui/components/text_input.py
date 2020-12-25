import dash_core_components as dcc
import dash_html_components as html


def text_input(label, placeholder, id_name):
    return (
        html.Label(label, className='form-label'),
        html.Br(),
        dcc.Input(
            placeholder=placeholder,
            id=id_name,
            type='text',
            className='Select-control text-input'
        )
    )
