import dash_core_components as dcc


def storage(_id, data=None):
    return dcc.Store(id=_id, data=data)
