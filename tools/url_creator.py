from langchain.tools import tool

@tool
def url_creator(song_name : str, artist_name : str) -> str:
    """Gets the url from chordbook to extract chords from"""
    return f'https://www.mychordbook.com/chords/{artist_name.lower().replace(" ", "-")}/{song_name.lower().replace(" ","-")}'
