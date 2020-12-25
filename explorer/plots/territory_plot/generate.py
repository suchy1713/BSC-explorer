from plots.territory_plot.plot import plot
from plots.utils import get_hover_info, combine_events_and_receivals, get_buildup, get_finishing, exclude_corners
from plots.codes import Phases, Versions

def attacking_scoring(events, team_events, hull, points):
    return events['Xt'].sum()

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def defensive_scoring(events, team_events, hull, points):
    return 1
    events['intersections'] = 0
    for i, pas in events.iterrows():
        inters = 0
        for j in range(0, len(hull.vertices)-1):
            if intersect((pas['StartX'], pas['StartY']),
                         (pas['EndX'], pas['EndY']),
                         points[hull.vertices[j]],
                         points[hull.vertices[j+1]]):
                inters += 1
        events.loc[i, 'intersections'] = inters

    return events.loc[events['intersections'] > 1].shape[0]

def get_def_cutoff(x):
    return -3/160 * x + 135/4

from metadata.strings import *
def generate_territory_plot(version, events, players, nineties, version_dict, color=None):
    if version == 'Attack':
        events = events.loc[events['IsTouch'] == True]
        events = exclude_corners(events)
        phase = version_dict[phase_label]
        events = combine_events_and_receivals(events)
        #TODO shouldnt receivals be combined after this???
        if phase == build_up_label:
            events = get_buildup(events)
        elif phase == finishing_label:
            events = get_finishing(events)

        positions = events['PlayerPosition'].unique()

        return plot(events, positions, players, nineties, 20, attacking_scoring)
    elif version == 'Defence':
        events = events.loc[events['IsDefAction'] == True]
        positions = events['PlayerPosition'].unique()

        return plot(events, positions, players, nineties, get_def_cutoff(events.shape[0]), defensive_scoring)

def territory_plot_attack(events, players, nineties, version_dict, color=None):
    return generate_territory_plot('Attack', events, players, nineties, version_dict, color=None)

def territory_plot_defence(events, players, nineties, version_dict, color=None):
    return generate_territory_plot('Defence', events, players, nineties, version_dict, color=None)