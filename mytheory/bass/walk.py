# *-------*
# | NOTES |
# *-------*
# 
# This guy's good enough for now.
# By that I mean it's good enough for 12 bar blues.
#

import mystuff.useful
import mystuff.mytheory.hard_coded
import mystuff.mytheory.general

quarter_pitches = []
skip_pitches = []

jump_odds = (1, 8)
skip_odds = (1, 4) 
gait_odds = (1, 4)
turn_odds = (1, 10)
chrom_odds = (3, 4)
favor_tonic_odds = (2, 3)
favor_octave_skip = (3, 4)

chord = None
scale = None
next_chord = None
next_chord_base = None

pitch = None

direction = 1
step_distance = 2
beats_since_jump = 0

def decideToJump():
	global jump_odds
	global beats_since_jump
	if beats_since_jump < 2:
		return False
	return mystuff.useful.hatChoice(jump_odds)
def favorTonic():
	global favor_tonic_odds
	return mystuff.useful.hatChoice(favor_tonic_odds)
def maybeChangeGait():
	global gait_odds
	global step_distance
	if mystuff.useful.hatChoice(gait_odds):
		step_distance = (step_distance % 2) + 1
def getDirection(jump=False):
	global turn_odds
	global pitch
	global direction

	threshold = 7
	if jump:
		threshold = 12
		
	if pitch - mystuff.mytheory.hard_coded.BASS_FLOOR <= threshold:
		direction = 1
	elif mystuff.mytheory.hard_coded.BASS_CEILING - pitch <= threshold:
		direction = -1
	else:
		if mystuff.useful.hatChoice(turn_odds):
			direction *= -1

	return direction
def maybeSkip(change=False):
	global skip_odds
	global favor_octave_skip
	global skip_pitches
	global chord
	global next_chord
	global pitch
	if mystuff.useful.hatChoice(skip_odds):
		relevant_chord = None

		if change:
			relevant_chord = next_chord
		else:
			relevant_chord = chord

		skip_pitch = mystuff.mytheory.general.targetPitch(relevant_chord.pitches[0], pitch -1)
		if not favorTonic():
			skip_pitch = mystuff.mytheory.general.targetPitch(relevant_chord.pitches[2], pitch, -1)

		if skip_pitch == pitch - 12:
			if not mystuff.useful.hatChoice(favor_octave_skip):
				skip_pitch = pitch

	else:
		skip_pitch = -1
	skip_pitches += [skip_pitch]

def jump():
	global quarter_pitches
	global jump_odds
	global scale
	global pitch
	global beats_since_jump

	direction = getDirection(True)

	# The following line could cause a problem if pitch is a chord base note that's not in the scale.
	# It's a potential bug that's unlikely ever to arise, but it's best to be aware of it.
	previous_scale_index = scale.sequenceIndex(pitch)
	previous_index = scale.pitches.index(pitch)

	distance_to_tonic = (direction * (0 - previous_scale_index)) % scale.sequence_length
	distance_to_fifth = (direction * (4 - previous_scale_index)) % scale.sequence_length
	if not distance_to_tonic:
		distance_to_tonic = scale.sequence_length
	if not distance_to_fifth:
		distance_to_fifth = scale.sequence_length

	if min(distance_to_tonic, distance_to_fifth) < 3:
		pitch = scale.pitches[previous_index + direction * max(distance_to_tonic, distance_to_fifth)]
	else:
		if favorTonic():
			pitch = scale.pitches[previous_index + direction * distance_to_tonic]
		else:
			pitch = scale.pitches[previous_index + direction * distance_to_fifth]

	quarter_pitches += [pitch]
	beats_since_jump = 0

	maybeSkip()
	maybeChangeGait()
def step():
	global quarter_pitches
	global scale
	global chord
	global pitch 
	global step_distance
	global beats_since_jump

	domain = None
	if step_distance == 1:
		domain = scale
	else:
		domain = chord

	pitch = domain.getNeighbour(pitch, getDirection())
	quarter_pitches += [pitch]
	beats_since_jump += 1

	maybeSkip()

	scale_index = scale.sequenceIndex(pitch)
	if scale_index == 0 or scale_index == 4:
		maybeChangeGait()

def chromaticStep(destination):
	global quarter_pitches
	global chrom_odds
	global pitch
	if mystuff.useful.hatChoice(chrom_odds):
		pitch += ((pitch - destination) / 2)
		quarter_pitches += [pitch]
		maybeSkip()
		pitch = destination
		quarter_pitches += [pitch]
		maybeSkip(True)
		return True
	else:
		return False
def change(quick=False):
	global quarter_pitches
	global next_chord
	global next_chord_base
	global pitch
	global beats_since_jump

	direction = getDirection()

	if quick:
		if not next_chord_base:
			if favorTonic():
				pitch = mystuff.mytheory.general.targetPitch(next_chord.pitches[0], pitch, direction)
			else:
				pitch = mystuff.mytheory.general.targetPitch(next_chord.pitches[2], pitch, direction)
		else:
			pitch = mystuff.mytheory.general.targetPitch(next_chord_base, pitch, direction)
		quarter_pitches += [pitch]
		beats_since_jump += 1
		maybeSkip(True)
	else:
		weChromStepped = False

		closest_next_base = mystuff.mytheory.general.targetPitch(next_chord.pitches[0], pitch, direction)
		if next_chord_base:
			closest_next_base = mystuff.mytheory.general.targetPitch(next_chord_base, pitch, direction)
		closest_next_fifth = mystuff.mytheory.general.targetPitch(next_chord.pitches[2], pitch, direction)

		if (closest_next_base - pitch) == 2:
			weChromStepped = chromaticStep(closest_next_base)
			beats_since_jump += 2
		elif (closest_next_fifth - pitch) == 2:
			weChromStepped = chromaticStep(closest_next_fifth)
			beats_since_jump += 2

		if not weChromStepped:
			step()
			change(True)

	maybeChangeGait()

def stitchLine(time_signature, n_reps):

	global quarter_pitches
	global skip_pitches

	music = []
	n_beats = len(quarter_pitches)
	beat_index = 0
	subdivision = mystuff.mytheory.hard_coded.SUBDIVISIONS['swung']
	fast = mystuff.mytheory.hard_coded.BASS_FAST
	slow = mystuff.mytheory.hard_coded.BASS_SLOW

	for rep in range(n_reps):
		for bar_time_signature in time_signature:
			bar = []
			for beat in range(bar_time_signature):
				quarter_pitch = quarter_pitches[beat_index]
				skip_pitch = skip_pitches[beat_index]
				if skip_pitch < 0:
					bar += [([quarter_pitch], fast, subdivision)]
				else:
					quarter_duration = 2 * subdivision / 3
					rest = 0
					if skip_pitch == pitch:
						quarter_duration = subdivision / 3
						rest = subdivision / 3
					bar += [([quarter_pitch], fast, quarter_duration)] 
					if rest:
						bar += [rest]
					bar += [([skip_pitch], slow, subdivision / 3)]
				beat_index += 1

			music += [bar]

	return music
def walk(stretches, time_signature, n_reps): 

	global quarter_pitches
	global skip_pitches

	global skip_odds
	global jump_odds
	global gait_odds
	global turn_odds

	global chord
	global scale
	global next_chord
	global next_chord_base

	global pitch

	pitch = mystuff.mytheory.general.targetPitch(stretches[0][0], mystuff.mytheory.hard_coded.BASS_TARGET)
	quarter_pitches += [pitch]

	n_stretches = len(stretches)

	for r in range(n_reps):
		for stretch_index in range(n_stretches):

			stretch = stretches[stretch_index]

			chord_constituents = mystuff.mytheory.general.parseWord(stretch[0])
			key_constituents = mystuff.mytheory.general.parseWord(stretch[1])
			n_beats = stretch[2]

			next_chord_constituents = []
			if stretch_index == n_stretches - 1:
				next_chord_constituents = mystuff.mytheory.general.parseWord(stretches[0][0])
			else:
				next_chord_constituents = mystuff.mytheory.general.parseWord(stretches[stretch_index + 1][0])

			# By adding [:4] to our chord intervals array, we're specifying that we want at most four notes to populate our domain. The idea here is that
			# it's much easier to make bass lines. 
			chord = mystuff.mytheory.general.Domain(chord_constituents[0], mystuff.mytheory.hard_coded.CHORD_INTERVALS[chord_constituents[1]][:4])
			scale = mystuff.mytheory.general.Domain(key_constituents[0], mystuff.mytheory.hard_coded.MODE_INTERVALS[key_constituents[1]])
			next_chord = mystuff.mytheory.general.Domain(next_chord_constituents[0], mystuff.mytheory.hard_coded.CHORD_INTERVALS[next_chord_constituents[1]][:4])
			next_chord_base = next_chord_constituents[2]

			for beat in range(1, n_beats):
				if beat == n_beats - 1:
					change(not beat)
				elif decideToJump():
					jump()
				else:
					step()					
	skip_pitches += [-1]
	return stitchLine(time_signature, n_reps)
	