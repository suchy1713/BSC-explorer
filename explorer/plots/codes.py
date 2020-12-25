from enum import Enum

class Passes(Enum):
    All = 0
    Forward = 1
    Progressive = 2
    Sideways = 3
    Backwards = 4
    Long = 5
    Weighted_by_Positive_xT = 6
    Weighted_by_Negative_xT = 7
    All_Centrality = 7

passes_strings = {
    1: 'Forward',
    2: 'Progressive',
    3: 'Sideways',
    4: 'Backwards',
    5: 'Long',
    6: 'Weighted by xT',
    #7: 'Negative xT',
    None: ''
}

passes = [
    {'label': 'All', 'value': 0},
    #{'label': 'Forward', 'value': 1},
    {'label': 'Progressive', 'value': 2},
    #{'label': 'Sideways', 'value': 3},
    #{'label': 'Backwards', 'value': 4},
    {'label': 'Long', 'value': 5},
    {'label': 'Weighted by xT', 'value': 6},
    #{'label': 'Weighted by Negative xT', 'value': 7}
]

class Phases(Enum):
    All = 0
    Deep = 1
    High = 2

phases = [
    {'label': 'All', 'value': 0},
    {'label': 'Deep', 'value': 1},
    {'label': 'High', 'value': 2}
]

plot_options = [
    {'label': 'Pass Network', 'value': 'Pass Network'},
    {'label': 'Territory Plot - Attack', 'value': 'Territory Plot - Attack'},
    {'label': 'Territory Plot - Defence', 'value': 'Territory Plot - Defence'}
]

class Versions(Enum):
    Attacking = 1
    Defensive = 2

phases_strings = {
    1: 'Deep',
    2: 'High',
    None: ''
}

versions = [
    {'label': 'Attack', 'value': 1},
    {'label': 'Defence', 'value': 2}
]

version_strings = {
    1: 'Attack',
    2: 'Defence',
    None: ''
}