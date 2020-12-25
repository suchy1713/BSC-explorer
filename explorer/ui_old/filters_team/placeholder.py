import dash_html_components as html
import dash_core_components as dcc

def get_placeholder():
    coords = ['00', '01', '10', '11']
    types = ['formations', 'events', 'players', 'nineties', 'clubId', 'formationLabel', 'filtersLabel', 'teamColor', 'versionDict']
    
    divs = []
    for coord in coords:
        divs.append(dcc.Dropdown(id={'type': f'formation', 'index-coords': f'{coord}'}, style={'display': 'none'}))
        divs.append(dcc.Dropdown(id={'type': f'plot', 'index-coords': f'{coord}'}, style={'display': 'none'}))
        divs.append(dcc.Dropdown(id={'type': f'passes', 'index-coords': f'{coord}'}, style={'display': 'none'}))
        divs.append(dcc.Dropdown(id={'type': f'phase', 'index-coords': f'{coord}'}, style={'display': 'none'}))
        for _type in types:
            divs.append(html.Div(id={'type': f'intermid-{_type}', 'index-coords': f'{coord}'}, style={'display': 'none'}))
    
    return divs