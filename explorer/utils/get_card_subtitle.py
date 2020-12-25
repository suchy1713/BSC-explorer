from metadata.strings import *
from ast import literal_eval


def is_none_or_default(value, default):
    return value in [default, None]


def get_card_subtitle(viz_type, version_dict):
    subtitle = ''

    subtitle += viz_type

    if not is_none_or_default(version_dict[phase_label], all_label):
        subtitle += f" - {version_dict[phase_label]}"

        if not is_none_or_default(version_dict[passes_label], all_label):
            subtitle += f", {version_dict[passes_label]}"

        return subtitle

    if not is_none_or_default(version_dict[passes_label], all_label):
        subtitle += f" - {version_dict[passes_label]}"

    if 0 < len(version_dict[positions_label]) < 11:
        subtitle += f" - Positions: {', '.join(version_dict[positions_label])}"

    return subtitle
