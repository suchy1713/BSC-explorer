from plots.passing_network.events_to_net_input import events_to_net_input
from plots.passing_network.plot import plot
from plots.utils import get_hover_info, exclude_corners
from plots.codes import Phases, Passes

from metadata.strings import *

def generate_passing_network(events, players, nineties, version_dict, color):
    events = exclude_corners(events)

    counts, xs, ys, positions, scores = events_to_net_input(
        events,
        version_dict[passes_label],
        version_dict[phase_label]
    )

    infos = get_hover_info(players, positions, nineties)

    return plot(counts, xs, ys, positions, scores, infos, color)