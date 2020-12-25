import dash_core_components as dcc
import dash_html_components as html

from plots.codes import passes, phases, versions

def empty(_type, idx):
    return html.Div([
            dcc.Dropdown(
                options=[],
                id={'type': _type, 'index-coords': idx},
                style={'display': 'none'}
            )
        ])

def version_select(idx, hide=False):
    if hide:
        return empty('version', idx)

    return html.Div([
            html.Label('Version', className='form-label'),
            dcc.Dropdown(
                options=versions,
                id={'type': 'version', 'index-coords': idx},
                clearable=False,
                searchable=False,
                value=versions[0]['value']
            )
        ])

def passes_select(idx, hide=False):
    if hide:
        return empty('passes', idx)

    return html.Div([
            html.Label('Pass Type', className='form-label'),
            dcc.Dropdown(
                options=passes,
                id={'type': 'passes', 'index-coords': idx},
                clearable=False,
                searchable=False,
                value=passes[0]['value']
            )
        ])

def phase_select(idx, hide=False):
    if hide:
        return empty('phase', idx)

    return html.Div([
            html.Label('Location', className='form-label'),
            dcc.Dropdown(
                options=phases,
                id={'type': 'phase', 'index-coords': idx},
                clearable=False,
                searchable=False,
                value=phases[0]['value']
            )
        ])