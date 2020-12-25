from metadata.strings import *
from metadata.keys import *


class Preset:
    def __init__(self, name, filter_values):
        self.name = name
        self.filter_values = filter_values


class Values:
    def __init__(self, viz_type, passes, phase, positions):
        self.viz_type = viz_type
        self.viz_filters = {
            passes_label: passes,
            phase_label: phase,
            positions_label: positions
        }

standard_1 = {
    '00': Values(passing_net, all_label, all_label, []),
    '10': Values(passing_net, progressive_label, all_label, []),
    '01': Values(attacking_territories, default_passes, all_label, []),
    '11': Values(defensive_territories, default_passes, default_phase, [])
}

standard_2 = {
    '00': Values(passing_net, all_label, all_label, []),
    '10': Values(attacking_territories, default_passes, all_label, []),
    '01': Values(passing_net, all_label, all_label, []),
    '11': Values(attacking_territories, default_passes, all_label, [])
}

test2 = {
    '00': Values(passing_net, weighted_by_xt_label, build_up_label, []),
    '10': Values(passing_net, weighted_by_xt_label, finishing_label, []),
    '01': Values(passing_net, weighted_by_xt_label, build_up_label, []),
    '11': Values(passing_net, weighted_by_xt_label, finishing_label, [])
}

standard_4 = {
    '00': Values(passing_net, all_label, all_label, []),
    '10': Values(passing_net, all_label, all_label, []),
    '01': Values(passing_net, all_label, all_label, []),
    '11': Values(passing_net, all_label, all_label, [])
}

presets = {
    '1': [
        Preset('Standard (1)', standard_1)
    ],
    '2': [
        Preset('Standard (2)', standard_2),
        Preset('Test', test2)
    ],
    '4': [
        Preset('Standard (4)', standard_4)
    ]
}
