import dash_bootstrap_components as dbc


def button(label, id_name):
    return dbc.Button(label, outline=True, color='warning', id=id_name)
