import dash_html_components as html

from ui.modules.sidebar import tabs
from ui.modules.sidebar import title

def sidebar(app, cache, db):
    sidebar = html.Div([
        title(app),
        tabs(app, cache, db)
    ], id='sidebar', className='shadow')

    return sidebar