from ui.components.dropdown import dropdown, empty
from ui.components.multi_dropdown import multi_dropdown
from utils.get_dropdown_input_from_list import get_dropdown_input_from_list
from metadata.strings import *
from metadata.id_types import *
from metadata.keys import *

from plots.passing_network.generate import generate_passing_network
from plots.heatmap.generate import generate_heatmap_defence, generate_heatmap_attack
from plots.territory_plot.generate import territory_plot_attack, territory_plot_defence


class Viz:
    def __init__(self, name, generate_func):
        self.name = name
        self.generate_func = generate_func


class VizFilter:
    def __init__(self, id_type, component, empty_component, display_on, default):
        self.id_type = id_type
        self.component = component
        self.empty_component = empty_component
        self.display_on = display_on
        self.default = default


vizzes = {
    passing_net: Viz(passing_net, generate_passing_network),
    attacking_territories: Viz(attacking_territories, territory_plot_attack),
    defensive_territories: Viz(defensive_territories, territory_plot_defence),
    heatmap_attack: Viz(heatmap_attack, generate_heatmap_attack),
    heatmap_defence: Viz(heatmap_defence, generate_heatmap_defence)
}

viz_filters = lambda coords: {
    phase_label: VizFilter(
        phase_dropdown,
        lambda value: dropdown(
            phase_label,
            phase_dropdown,
            (id_index_coords, coords),
            get_dropdown_input_from_list([all_label, build_up_label, finishing_label]),
            active_option=value
        ),
        lambda value: empty(
            phase_dropdown,
            (id_index_coords, coords),
            get_dropdown_input_from_list([all_label]),
            value
        ),
        [passing_net, attacking_territories],
        all_label
    ),
    passes_label: VizFilter(
        passes_dropdown,
        lambda value: dropdown(
            passes_label,
            passes_dropdown,
            (id_index_coords, coords),
            get_dropdown_input_from_list([all_label, progressive_label, long_label, weighted_by_xt_label]),
            active_option=value
        ),
        lambda value: empty(
            passes_dropdown,
            (id_index_coords, coords),
            get_dropdown_input_from_list([all_label]),
            value
        ),
        [passing_net],
        all_label
    ),
    positions_label: VizFilter(
        positions_dropdown,
        lambda options: multi_dropdown(
            positions_label,
            positions_dropdown,
            (id_index_coords, coords),
            get_dropdown_input_from_list(options),
            active_options=[]
        ),
        lambda value: empty(
            positions_dropdown,
            (id_index_coords, coords),
            get_dropdown_input_from_list(value),
            value
        ),
        [heatmap_defence, heatmap_attack],
        all_label
    )
}
