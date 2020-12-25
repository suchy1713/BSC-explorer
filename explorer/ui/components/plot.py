import dash_core_components as dcc


def plot(fig, id_name):
    style = {'height': '40.48vh'}

    graph = dcc.Graph(
        id=id_name,#f'graph-{coords}',
        figure=fig,
        config={
            'responsive': True,
            'displayModeBar': False
        },
        style=style
    )

    return graph
