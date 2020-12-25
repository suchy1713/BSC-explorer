import numpy as np
import pandas as pd

from metadata.keys import *
from metadata.strings import *


def group_formations(df):
    grouped = df[[vector_key, label_key, minutes_key]].groupby(vector_key).apply(
        lambda df: pd.Series({
            formation_label_key: df[label_key].values[0],
            vector_key: df[vector_key].values[0],
            nineties_key: df[minutes_key].sum()/90
        })
    )

    grouped = grouped.sort_values('90s_played', ascending=False)
    grouped.index = np.arange(1, len(grouped)+1)

    grouped[label_to_display_key] = formation_label(grouped[formation_label_key], grouped[nineties_key])

    return grouped
