import os
import pygame
from time import sleep, time
from decimal import Decimal
import pygame.midi
import threading
from copy import copy
from mystuff.mytheory.general import *

# *------------------------------*
# | INITIALIZE AND CLOSE DEVICES |
# *------------------------------*

def initializeIO():
	pygame.init()
	pygame.midi.init()

	input_devices = {}
	output_devices = {}
	for i in range(pygame.midi.get_count()):
		if pygame.midi.get_device_info(i)[2]:
			input_devices[pygame.midi.get_device_info(i)[1]] = i
		if pygame.midi.get_device_info(i)[3]:
			output_devices[pygame.midi.get_device_info(i)[1]] = i

	print "Input devices detected..."
	for device in input_devices.keys():
		print(str(input_devices[device]) + ". " + device)

	print ""

	input_id = int(raw_input("Selection: "))
	keyboard = pygame.midi.Input(input_id)

	_=os.system("clear")

	print "Output devices detected..."
	for device in output_devices.keys():
		print str(output_devices[device]) + ". " + device

	print ""

	output_id = int(raw_input("Selection: "))
	synth = pygame.midi.Output(output_id)

	_=os.system("clear")
	return [keyboard, synth]
def closeIO(keyboard, synth):
	keyboard.close()
	synth.close()

# *--------------*
# | SOUND OUTPUT |
# *--------------*

class Instrument:
	def __init__(self, kind, synth, channel):
		self.kind = kind
		self.synth = synth
		self.channel = channel
		self.players = {}
		self.lock = threading.Lock()			

	def noteOn(self, pitch, velocity, playerID):
		with self.lock:
			self.players[pitch] = playerID
		self.synth.note_on(pitch, velocity, self.channel)

	def noteOff(self, pitch, playerID):
		with self.lock:
			try:
				if self.players[pitch] == playerID:
					self.synth.note_off(pitch, None, self.channel)
					self.players.pop(pitch)
			except KeyError:
				pass

# A thread class responsible for playing one 'unit' of sound data.
class UnitPlayer(threading.Thread):
	def __init__(self, instrument, unit_data):
		threading.Thread.__init__(self)
		self.ID = Decimal(time())
		self.instrument = instrument
		self.unit_data = unit_data

	def run(self):
		for i in self.unit_data[0]:
			self.instrument.noteOn(i, self.unit_data[1], self.ID)
		sleep(self.unit_data[2])
		for i in self.unit_data[0]:
			self.instrument.noteOff(i, self.ID)

# *-------------*
# | SOUND INPUT |
# *-------------*

def fetchNotes(keyboard, synth):
	listening = True
	note_data = []
	while listening:
		if keyboard.poll():
			midi_events = keyboard.read(1)
			if midi_events[0][0][2] > 0:
				synth.note_on(midi_events[0][0][1], midi_events[0][0][2])
				note_data = [midi_events[0][0][1], midi_events[0][0][2]]
			else:
				synth.note_off(midi_events[0][0][1], midi_events[0][0][2])
				listening = False
	return note_data

# *------*
# | JAZZ |
# *------*

#	The following is for testing purposes
#		if not self.patterns:
#			return [(0, ([60, 64, 67], 100, 2)), (1, ([71], 100, 2)), (3, ([65, 69, 72], 100, 4)), (7, ([67, 71, 74], 100, 2))]
#		else:
#			return [(0, ([48], 100, 1)), (3, ([48], 100, 1)), (4, ([48], 100, 1)), (5, ([48], 100, 1))]

class Session(threading.Thread):

	def __init__(self, chart, compers, n_reps=1, context=None, tempo=None):

		threading.Thread.__init__(self)
		self.chart = chart
		self.compers = compers
		self.n_reps = n_reps
		
		self.context = context
		if not context:
			self.context = chart.original_context
		self.tempo = tempo
		if not tempo:
			self.tempo = chart.original_tempo
		
		self.chart_duration = 0
		for bar_time_signature in chart.time_signature: 
			self.chart_duration += (float(bar_time_signature) / float(self.tempo)) * 60.0
		self.session_duration= self.n_reps * self.chart_duration

		self.start_time = 0
		self.arrangement = []
		self.players = []

	def arrange(self):

		parts = []

		# Get the Compers to write their parts
		for comper in self.compers:
			parts += [comper.comp(self.chart, self.context, self.tempo, self.n_reps)]

		events_remain = True
		while events_remain:

			current_event_times = []
			for part in parts:
				if part:
					current_event_times += [part[0][0]]
				else:
					current_event_times += [float("inf")]

			I = current_event_times.index(min(current_event_times))
			self.arrangement += [(self.compers[I].instrument, parts[I].pop(0))]

			events_remain = False
			for part in parts:
				events_remain = events_remain or bool(part)

	def where(self):

		t = time() - self.start_time
		if t > self.session_duration or t < 0:
			return ()

		pos = ((t % self.chart_duration) / self.chart_duration) * self.chart.n_bars
		where_in_chart = self.chart.where(pos)
		return (t, int(math.floor(t / self.chart_duration)), where_in_chart[0], where_in_chart[1], where_in_chart[2])

	def run(self):

		self.start_time = time()
		t = 0
		for session_event in self.arrangement:
			event = session_event[1]
			wait = event[0] - t

			sleep(wait)
			t += wait

			current_player = UnitPlayer(session_event[0], event[1])
			current_player.start()
			self.players += [current_player]

	def end(self):
		self.join()
		for player in self.players:
			player.join()




					




			



