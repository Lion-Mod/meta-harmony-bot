from langchain.tools import tool

@tool
def create_url(artist_name : str, song_name : str) -> str:
    """Gets the url from chordbook to extract chords from based upon the song_name and artist_name"""
    return f'https://www.mychordbook.com/chords/{artist_name.lower().replace(" ", "-")}/{song_name.lower().replace(" ","=")}'
