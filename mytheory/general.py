from random import randint, choice
import math
import numpy
import mystuff.useful
import mystuff.mytheory.hard_coded

def fillNoteMap():
	for oc in range(-1, 8):
		for n in range(12):
			note = mystuff.mytheory.hard_coded.NOTE_NAMES[n] + str(oc)
			mystuff.mytheory.hard_coded.NOTE_MAP += [note]
def parseWord(word):
	A = word.split('^')
	B = A[0].split('/')

	root_name = B[0]
	chord_name = ''
	base_name = ''

	try:
		base_name = B[1]
	except IndexError:
		try:
			C = A[1].split('/')
			chord_name = C[0]
			base_name = C[1]
		except IndexError:
			pass

	return (root_name, chord_name, base_name)
def contextualize(subject, context):

	if isinstance(subject, str):
		if not subject:
			return ''
		elif len(subject) == 1:
			root_name_index = mystuff.mytheory.hard_coded.NOTE_NAMES.index(context)
			subject_index = (root_name_index + mystuff.mytheory.hard_coded.POSITIONS[subject]) % 12
			return mystuff.mytheory.hard_coded.NOTE_NAMES[subject_index]
		else:
			constituents = parseWord(subject)
			contextualized_word = contextualize(constituents[0], context)
			if constituents[1]:
				contextualized_word += "^" + constituents[1]
			if constituents[2]:
				contextualized_word += "/" + contextualize(constituents[2], context)
			return contextualized_word
	elif isinstance(subject, list):
		if isinstance(subject[0], list):
			progression = []
			for bar in subject:
				new_bar = []
				for word in bar:
					new_bar += [contextualize(word, context)]
				progression += [new_bar]
			return progression
		else:
			stretches = []
			for stretch in subject:
				new_stretch = (contextualize(stretch[0], context), contextualize(stretch[1], context), stretch[2])
				stretches += [new_stretch]
			return stretches
	else:
		def changes(measure):
			return contextualize(subject(measure), context)
		return changes
def targetPitch(subject, target, direction=None):
	pitch = subject
	if isinstance(subject, str):
		pitch = mystuff.mytheory.hard_coded.NOTE_NAMES.index(parseWord(subject)[0])
	pitch %= 12

	while (target - pitch) > 5:
		pitch += 12

	if direction:
		if direction > 0:
			if pitch < target:
				pitch += 12
		else:
			if pitch > target:
				pitch -= 12
	return pitch

class Domain:

	# ~ Attributes ~ 

		# root            (chr)
		# sequence_length (int)
		# pitches         (arr)
	# ~ Functions ~ 

		# sequenceIndex(pitch): 
		
			# Takes a pitch (int) a note (char) or
			# specific note (str) and returns the 
			# index of that note's position in the 
			# sequence of the domain.

	def __init__(self, root_name, sequence):
		
		self.root_name = root_name
		self.sequence_length = len(sequence)

		lowest_tonic = mystuff.mytheory.hard_coded.NOTE_NAMES.index(root_name)
		lowest_pitches = []

		for i in sequence:
			lowest_pitches += [(lowest_tonic + i) % 12]

		self.pitches = []
		for pitch in range(mystuff.mytheory.hard_coded.MAP_LENGTH):
			if (pitch % 12) in lowest_pitches:
				self.pitches += [pitch]

	def sequenceIndex(self, pitch):
		try:
			return self.pitches.index(pitch) % self.sequence_length
		except IndexError:
			return -1

	def getNeighbour(self, pitch, direction):
		pitch_index = mystuff.useful.closestIndex(self.pitches, pitch)
		if not direction:
		 	neighbours = [self.pitches[pitch_index - 1], self.pitches[pitch_index + 1]]
			return neighbours[numpy.argmin([pitch - neighbours[0], neighbours[1] - pitch])]
		return self.pitches[pitch_index + direction]
