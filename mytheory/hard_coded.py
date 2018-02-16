# *---------*
# | GENERAL |
# *---------*

NOTE_NAMES = ['C', 'C#|Db', 'D', 'D#|Eb', 'E', 'F', 'F#|Gb', 'G', 'G#|Ab', 'A', 'A#|Bb', 'B']
NOTE_MAP = []
MAP_LENGTH = 108

# My new musical alphabet... These are relative positions and are not meant to represent 
# the same pitches everytime their used. They rely on a 'context', the designated tonic pitch.
POSITIONS = {'1': 0, 'H': 1, '2': 2, 'N': 3, '3': 4, '4': 5, 'T': 6, '5': 7, 'U': 8, '6': 9, 'J': 10, '7': 11}

# *------*
# | JAZZ |
# *------*

# Add more chords and scales to improve robustness 
CHORD_INTERVALS = {'': [0, 4, 7], 'ma7': [0, 4, 7, 11], '7': [0, 4, 7, 10], '7#11': [0, 4, 7, 10, 14, 18], '-': [0, 3, 7], '-7': [0, 3, 7, 10], '-9': [0, 3, 7, 10, 14]}
MODE_INTERVALS = {'': [0, 2, 4, 5, 7, 9, 11], '7': [0, 2, 4, 5, 7, 9, 10], '-': [0, 2, 3, 5, 7, 9, 10]}

SUBDIVISIONS = {}
SUBDIVISIONS["swung"] = 3
SUBDIVISIONS["bossa"] = 2

# Pianist
PIANO_TARGET = 48
PIANO_FAST = 80
PIANO_SLOW = 60
PIANO_RHYTHMS = {}
PIANO_RHYTHMS["swung"] = {}
PIANO_RHYTHMS["swung"][1] = [[(PIANO_FAST, 3)]]
PIANO_RHYTHMS["swung"][2] = [[(PIANO_FAST, 5), (PIANO_SLOW, 1)]]
PIANO_RHYTHMS["swung"][3] = [[(PIANO_FAST, 3), 2, (PIANO_FAST, 3), 1]]
PIANO_RHYTHMS["swung"][4] = [[(PIANO_FAST, 3), 2, (PIANO_FAST, 7)], [2, (PIANO_FAST, 7), 3], [2, (PIANO_FAST, 1), 9], [(PIANO_FAST, 2), (PIANO_SLOW, 1), 9]]
PIANO_RHYTHMS["swung"][8] = [[2, (PIANO_FAST, 1), 2, (PIANO_FAST, 1), 5, (PIANO_FAST, 10), 3]]

# Bassist
BASS_CEILING = 72
BASS_FLOOR = 42
BASS_TARGET = (BASS_FLOOR + BASS_CEILING) / 2

BASS_FAST = 100
BASS_SLOW = 50	

# Charts
# TODO
	# Create some hard-coded charts that can be easily accessed for testing, and later practicing, purposes
