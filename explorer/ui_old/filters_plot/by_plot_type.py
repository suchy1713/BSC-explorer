import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from plots.codes import plot_options

def by_plot_type(app, db, row, column):
    return [
        html.Label('Visualization', className='form-label'),
        dcc.Dropdown(
            options=plot_options,
            id={'type': 'plot', 'index-coords': f'{row}{column}'},
            clearable=False,
            searchable=False,
            value=plot_options[row]['value']
        )
    ]