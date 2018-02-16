import math
import mystuff.mytheory.hard_coded
import mystuff.mytheory.general 

def musicToTime(music, tempo, subdivision):

	units = []
	coefficient = (60.0 / float(tempo)) / float(subdivision)
	t = 0
	for bar in music:
		for music_unit in bar:
			if isinstance(music_unit, int):
				# In this case, music_unit is the duration of a rest in subdivision beats
				t += coefficient * music_unit
			else:
				duration = coefficient * music_unit[2]
				units += [(t, (music_unit[0], music_unit[1], duration))]
				t += duration

	return units

class Chart:

	# TEMPO AND TIME_SIGNATURE MUST ALWAYS BE W.R.T THE QUARTER NOTE

	def __init__(self, name, progression, changes, tune, time_signature, feel, original_context, original_tempo):

		self.name = name
		self.progression = progression
		self.changes = changes
		self.tune = tune
		self.time_signature = time_signature
		if isinstance(time_signature, int):
			self.time_signature = []
			for bar in progression:
				self.time_signature += [time_signature]
		self.feel = feel
		self.original_context = original_context
		self.original_tempo = original_tempo
		self.n_bars = len(progression)
		
	def where(self, pos):

		bar_pos = pos % 1
		bar_index = int(math.floor(pos))
		bar = self.progression[bar_index]
		
		beat_index = int(math.floor(len(bar) * bar_pos))
		while not bar[beat_index]:
			beat_index -= 1
			
		return (bar_index, bar[beat_index], self.changes(pos))

	def getChordStretches(self):

		stretches = []
		chord = ''
		previous_chord = self.progression[0][0]
		beat_count = 0
		bar_number = 0
		division = 0
		i = 0
		changes_index = 0

		while bar_number < self.n_bars:

			division = len(self.progression[bar_number])
			i = 0
			while i < division:
				chord = self.progression[bar_number][i]
				if chord and chord != previous_chord:
					stretches += [(previous_chord, self.changes(changes_index), beat_count)]
					previous_chord = chord
					beat_count = 0
					changes_index = bar_number + (float(i) / float(division))
				if division == 1:
					beat_count += self.time_signature[bar_number]
				elif division == 2:
					beat_count += 2
				else:
					beat_count += 1

				i += 1

			bar_number += 1

		stretches += [(previous_chord, self.changes(changes_index), beat_count)]

		return stretches
class Comper:
	def __init__(self, instrument):
		self.instrument = instrument
		self.comp_styles = {}
	def comp(self, chart, context=None, tempo=None, n_reps=1):
		if not context:
			context = chart.original_context
		if not tempo:
			tempo = chart.original_tempo

		comp_style = self.comp_styles[chart.feel]
		music = comp_style(mystuff.mytheory.general.contextualize(chart.getChordStretches(), context), chart.time_signature, n_reps) 

		return mystuff.mytheory.jazz.musicToTime(music, tempo, mystuff.mytheory.hard_coded.SUBDIVISIONS[chart.feel])
