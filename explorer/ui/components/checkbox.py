import dash_core_components as dcc


def checkbox(id_name, label, value, checked):
    return dcc.Checklist(
        options=[
            {'label': label, 'value': value}
        ],
        value=[value] if checked else [],
        id=id_name
    )
