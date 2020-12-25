import dash_html_components as html
from ui.components.dropdown import dropdown
from ui.components.storage import storage
from ui.components.checkbox import checkbox
from ui.components.text_input import text_input
from ui.components.button import button
from metadata.id_types import *
from metadata.strings import *
from metadata.presets import presets
from utils.json_service import dump


def layout_filters():
    return [
        checkbox(vertical_checkbox, vertical_label, 'v', True),
        storage(coords_lookup_storage),
        storage(presets_storage, data=dump(presets)),
        *dropdown(
            n_teams_label,
            classic_id=n_teams_dropdown,
            options=[{'label': i, 'value': i} for i in [1, 2, 4]],
            active_option_idx=1),
        *dropdown(
            preset_label,
            classic_id=preset_dropdown
        ),
        html.Hr(),
        *text_input(
            save_preset_label,
            save_preset_placeholder,
            preset_name_input
        ),
        html.Br(),
        button(save_preset_button_label, save_preset_button)
    ]
