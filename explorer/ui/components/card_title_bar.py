import dash_html_components as html
import dash_bootstrap_components as dbc


def card_title_bar(title, subtitle, title2, subtitle2, row, color):
    margin = '5px'
    func = dbc.CardHeader if row == 0 else dbc.CardFooter

    return func([
        dbc.Row(
            [
                dbc.Col([
                    html.Div(
                        title,
                        style={'margin-bottom': '0'},
                        className='plot-card-title'
                    ),
                    html.Div(
                        subtitle,
                        style={'margin-bottom': '0', 'margin-top': '-3px'},
                        className='plot-card-subtitle'
                    )
                ], xs=6, style={'padding-left': margin}),
                dbc.Col([
                    html.Div(
                        title2,
                        style={'margin-bottom': '0', 'margin-top': '1px'},
                        className='plot-card-subtitle'),
                    html.Div(
                        subtitle2,
                        style={'margin-bottom': '0', 'margin-top': '2px'},
                        className='plot-card-subtitle')
                ], style={'text-align': 'right', 'padding-right': margin}, xs=6)
            ]
        )
    ], style={'border-color': color})
