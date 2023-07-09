from functions.chord_data_processers import *
from langchain.tools import tool
from typing import Dict


@tool
def song_getter(song_name : str, artist_name : str) -> Dict:
    """
    Creates a url using the song_name and artist_name to get the non processed chord sheet and then processes it into a dictionary

    Example output : {'intro' : ['Cmaj', 'D', 'Emin'], 'verse' : ['Fmin', 'Dmin', 'Gmin']}
    """
    url = url_creator(song_name = song_name, artist_name = artist_name)

    return get_unclean_chord_data(url)      