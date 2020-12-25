import pandas as pd

def get_color(colors, club_id):
    colors_df = pd.read_json(colors, orient='split')

    return colors_df.loc[colors_df['id'] == club_id]['color'].values[0]