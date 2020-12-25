order = [
    'GK',
    'LB', 'LWB',
    'LCB', 'CB', 'RCB',
    'RB', 'RWB',
    'LDM', 'DM', 'RDM',
    'LCM', 'CM', 'RCM',
    'LAM', 'AM', 'RAM',
    'LW',
    'RW',
    'LST', 'ST', 'RST'
]


def sort_positions(array):
    return sorted(array, key=lambda x: order.index(x))
