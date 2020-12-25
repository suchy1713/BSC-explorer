import pandas as pd
from metadata.keys import *


def get_color(colors, club_id):
    colors_df = pd.read_json(colors, orient='split')

    return colors_df.loc[colors_df[id_key] == club_id][color_key].values[0]
