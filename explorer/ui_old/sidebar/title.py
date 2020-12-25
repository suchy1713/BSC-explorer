import dash_html_components as html
import dash_bootstrap_components as dbc

def title(app):
    return dbc.CardHeader(
        [
            html.Img(
                src=app.get_asset_url('logo2.png'), 
                className='logo title-elem'
            ),
            html.H4(
                'BSC Explorer',
                style={'margin-bottom': '0'},
                className='title-elem'
            )
        ], className='sidebar-top', 
           style={'padding': '5px', 'border': 'none'}
    )