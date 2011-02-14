from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal
import PyQGLViewer
import OpenGL.GL as ogl
import numpy as np
import time
import fluidsynth
import freenect
#from keyboard import Keyboard
PLAY_TIME = 0.1			# Minimum time a note will sound for
REPEAT_TIME = 0.1		  # Minimum time between the start of two notes
MIN_POINTS = 4			 # Minimum points in a key for it to be pressed

def get_quads(vmin, vmax):
	""" Return the 6 faces of a rectangluar prism defined by (vmin, vmax). """
	x1, y1, z1, x2, y2, z2 = np.hstack((vmin, vmax))
		
	return np.array([[x1, y1, z1], [x1, y2, z1], [x2, y2, z1], [x2, y1, z1],
					 [x1, y1, z2], [x2, y1, z2], [x2, y2, z2], [x1, y2, z2],
					 [x1, y1, z1], [x1, y1, z2], [x1, y2, z2], [x1, y2, z1],
					 [x2, y1, z1], [x2, y2, z1], [x2, y2, z2], [x2, y1, z2],
					 [x1, y1, z1], [x2, y1, z1], [x2, y1, z2], [x1, y1, z2],
					 [x1, y2, z1], [x1, y2, z2], [x2, y2, z2], [x2, y2, z1]]).T

class Key(QtCore.QObject):

	sendkey = pyqtSignal(int, int, name="sendkey")

	""" Represents a key's state, position and colour. """
	def __init__(self, type, number, note, connector, vmin, vmax, colour=(0,0,1,0.5)):
		""" Create a key corresponding to a midi note. """
		QtCore.QObject.__init__(self)
		self.note = note		
		self.vmin = np.array(vmin)
		self.vmax = np.array(vmax)		
		self.colour = colour
		self.quads = get_quads(self.vmin, self.vmax)
		self.pressed = False
		self.last_pressed = 0
		self.type = type
		self.number = number
		self.connector = connector
		self.sendkey.connect(self.connector.typewriterSlot)

		
	def update(self, points):
		""" Update the key's press status by using the 3D points. """
		# Compute how many points are within the extents of the key
		big_enough = (points > self.vmin.reshape((3, -1))).min(axis=0)
		small_enough = (points < self.vmax.reshape((3, -1))).min(axis=0)		
		inkey_indices = np.multiply(big_enough, small_enough)		
		
		if(sum(inkey_indices) > MIN_POINTS):
			self.press()
		else:
			self.release()

	def press(self):
		""" Plays the note if the key was previously unpressed. """
		press_time = time.clock()
		
		if not(self.pressed) and press_time - self.last_pressed > PLAY_TIME:
			self.pressed = True
			Key.synth.noteon(0, self.note, 127)			
			self.last_pressed = press_time
			self.sendkey.emit(self.type, self.number)
		
	def release(self):
		""" Stop the note if the key was previously pressed. """
		unpress_time = time.clock()
		
		if self.pressed and unpress_time - self.last_pressed > REPEAT_TIME:
			self.pressed = False
			Key.synth.noteoff(0, self.note)  

