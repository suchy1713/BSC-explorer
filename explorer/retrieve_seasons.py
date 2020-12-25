from utils.get_dropdown_input import get_dropdown_input
from metadata.keys import *


def retrieve_seasons(db):
    df = db.get_seasons()
    options = get_dropdown_input(df, season_key, season_key)

    return options
