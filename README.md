# Meta Harmony Bot

## TLDR of what it does
1. Get some chords to a song by an artist / band
2. Colour the chords and extensions using MetaHarmony principles
3. Output coloured chords and extensions

## Uses
1. Understand if there are common types of voice leading in a song
2. See if certain artists / bands use common chord movements

## Example
```python
from tools.song_getter import *

chords = song_getter.func(song_name = 'when I was your man', artist_name = 'bruno mars')
print(chords)

{'intro': [('D', None, 'dom', 'g', 'dom7', 'syntonic', 'y', '', '', ''),
  ('D', None, 'min', 'g', '', '', '', '', '', ''),
  ('C', None, 'maj', 'o', '', '', '', '', '', ''),
  ('D', None, 'dom', 'g', 'dom7', 'syntonic', 'y', '', '', ''),
  ('D', None, 'min', 'g', '', '', '', '', '', ''),
  ('C', None, 'maj', 'o', '', '', '', '', '', ''),
  ('G', '/B', 'maj', 'p', '', '', '', '', '', '')],
 'verse 1': [('A', None, 'min', 'o', '', '', '', '', '', ''),
  ('C', None, 'maj', 'o', '', '', '', '', '', ''),
  ('D', None, 'min', 'g', '', '', '', '', '', ''),
  ('G', None, 'maj', 'p', '', '', '', '', '', ''),
  ('G', None, 'dom', 'p', 'dom7', 'syntonic', 'b', '', '', ''),
  ('C', None, 'maj', 'o', '', '', '', '', '', ''),
  ('E', '/B', 'min', 'p', '', '', '', '', '', ''),
  ('A', None, 'min', 'o', '', '', '', '', '', ''),
  ('C', None, 'maj', 'o', '', '', '', '', '', ''),
  ('D', None, 'min', 'g', '', '', '', '', '', ''),
  ('G', None, 'maj', 'p', '', '', '', '', '', ''),
  ('C', None, 'maj', 'o', '', '', '', '', '', '')], ...
```

## Todos
~~* Get data cleanup to be able to handle inversions~~
~~* More colouring - sus chords, min7b5 chords, other extensions?~~
~~* Handle dominant 9th, 11ths etc~~
* Basic reharm, you enter key cube you're in (this determines alphacube and chord functions) and state to reharm to a mode e.g C lydian (shift SD up)
* Do the above but for an entire section e.g. change the intro to be xxx
(Don't affect chords not in the key e.g. Cmajor key, there's a Bb chord, leave it)
* Identify most likely key of each section of the song is
* Identify most likely mode each section of the song is
* Visualise the coloured chords in an interactive web app
* Get the coloured chords to format correctly based upon chord length e.g. 1 bar, 2 bars...
