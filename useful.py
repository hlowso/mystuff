import numpy
import random

def closestIndex(array, value):
	return numpy.argmin(map(lambda x: abs(x - value), array))

def hatChoice(odds):
	chances = odds[0]
	hat_size = odds[1]
	hat = []
	while chances:
		hat += [True]
		chances -= 1
		hat_size -= 1
	while hat_size:
		hat += [False]
		hat_size -= 1
	return random.choice(hat)

def customHatChoice(odds):
	hat = []
	n_choices = len(odds)
	for i in range(n_choices):
		for j in range(odds[i]):
			hat += [i]
	return random.choice(hat)
