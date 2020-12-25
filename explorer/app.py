import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache

from ui.modules.sidebar import sidebar
from ui.modules.content import content
from callbacks.register_callback import register_callbacks
from db.db import db
from retrieve_seasons import retrieve_seasons

app = dash.Dash(__name__, 
                external_stylesheets=['https://fonts.googleapis.com/css2?family=Alegreya+Sans&display=swap'],
                external_scripts=[
                    'https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js'
                ],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                suppress_callback_exceptions=True
)

db = db()
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

seasons = retrieve_seasons(db)
app.layout = dbc.Container([
    sidebar(app, seasons),
    content()
], fluid=True)

register_callbacks(app, db, seasons)

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False, dev_tools_ui=False, dev_tools_props_check=False)
