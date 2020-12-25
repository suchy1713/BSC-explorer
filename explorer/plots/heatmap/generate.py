from plots.heatmap.plot import plot
from plots.utils import exclude_corners, combine_events_and_receivals
from metadata.keys import *
from metadata.strings import *


def filter_by_positions(events, positions):
    return events.loc[events[position_key].isin(positions)]


def generate_heatmap(version, events, players, nineties, version_dict, color):
    if version == 'Attack':
        events = exclude_corners(events)
        events = events.loc[events['IsTouch'] == True]
        events = combine_events_and_receivals(events)
    elif version == 'Defence':
        events = events.loc[events['IsDefAction'] == True]

    positions = version_dict[positions_label]
    if 0 < len(positions) < 11:
        events = filter_by_positions(events, positions)

    return plot(events, color)


def generate_heatmap_attack(events, players, nineties, version_dict, color=None):
    return generate_heatmap('Attack', events, players, nineties, version_dict, color)


def generate_heatmap_defence(events, players, nineties, version_dict, color=None):
    return generate_heatmap('Defence', events, players, nineties, version_dict, color)
