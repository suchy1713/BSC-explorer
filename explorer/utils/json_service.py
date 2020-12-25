import jsonpickle

def load(x):
    return jsonpickle.decode(x)

def dump(x):
    return jsonpickle.encode(x)