from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal
import numpy as np
from key import Key
import fluidsynth
import OpenGL.GL as ogl
class Keyboard(QtCore.QObject):
	""" Represents the virtual keyboard.
	
	Handles drawing as well as math for transformations.
	
	"""
	""" Keyboard Type Constants """
	TYPE_FORWARD = 1
	TYPE_REVERSE = 2
	TYPE_SELECT = 3
	TYPE_DIRECTION_TOGGLE = 4
	def __init__(self, type, number_of_keys, width_factor, height_factor, gap_factor, key_start, filename, connector):
		""" Create the keyboard. """		
		self.vmin = np.array([0,0,0])
		self.vmax = np.array([1, width_factor, height_factor])
		self.scale = 1.0
		self.number_of_keys = number_of_keys
		self.width_factor = width_factor
		self.height_factor = height_factor
		self.gap_factor = gap_factor
		self.key_start = key_start
		self.filename = filename
		self.type = type
		self.connector = connector
		# Load previous transform from file (if exists)
		try:
			self.set_transform(np.load(self.filename))
			print('transform loaded from file')
		except:
			print('failed to load from file')
			self.set_transform(np.diag([100, 100, 100, 1]))
		
		# Compute the midi note value for a few octaves
		white_basis = np.array([0, 2, 4, 5, 7, 9, 11])
		black_basis = np.array([1, 3, 6, 8, 10])
		white_notes = np.hstack((white_basis + 36,
								 white_basis + 48, 
								 white_basis + 60, 
								 white_basis + 72))  
		black_notes = np.hstack((black_basis + 36,
								 black_basis + 48, 
								 black_basis + 60, 
								 black_basis + 72))

		def make_white_key(number, note):
			xmin = number * 1.0 / self.number_of_keys + self.gap_factor / 2
			xmax = (number + 1) * 1.0 / self.number_of_keys - self.gap_factor / 2
			ymin = self.vmin[1] 
			ymax = self.vmax[1]
			zmin = self.vmin[2]
			zmax = self.vmax[2]
			return Key(self.type, number, note, self.connector, [xmin, ymin, zmin], [xmax, ymax, zmax])
			
		whites = white_notes[self.key_start:self.key_start + self.number_of_keys]
		self.keys = map(make_white_key, range(0, self.number_of_keys), whites)
		
		# Create the synthesiser - and pass it to Key class
		self.synth = fluidsynth.Synth()
		self.synth.start('alsa')
		sfid = self.synth.sfload('/usr/share/sounds/sf2/FluidR3_GM.sf2')
		self.synth.program_select(0, sfid, 0, 0) 
		Key.synth = self.synth
			
	def set_transform(self, transform):
		""" Update the internal transform, calculate inverse, and save it. """
		self.transform = transform
		self.inv_transform = np.linalg.inv(transform)
		np.save(self.filename, self.transform)
	def nudge_roll(self, sign):
		""" Rotate about local y axis. """
		delta = np.eye(4)		
		t = sign * self.scale * 0.001
		c, s = np.cos(t), np.sin(t)
		Ry = np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])
		delta[0:3, 0:3] = Ry
		
		new_t = np.dot(self.transform, delta)
		self.set_transform(new_t)
	def nudge_pitch(self, sign):
		""" rotate about x axis """
		delta = np.eye(4)		
		t = sign * self.scale * 0.01
		c, s = np.cos(t), np.sin(t)
		
		Rx = np.array([[1, 0, 0], [0, c, -s], [ 0, s, c]])
		delta[0:3, 0:3] = Rx
		
		new_t = np.dot(self.transform, delta)
		self.set_transform(new_t)
	def nudge_yaw(self, sign):
		""" rotate about x axis """
		delta = np.eye(4)		
		t = sign * self.scale * 0.01
		c, s = np.cos(t), np.sin(t)
		
		Rz = np.array([[c, -s, 0], [s, c, 0], [ 0, 0, 1]])
		delta[0:3, 0:3] = Rz
		
		new_t = np.dot(self.transform, delta)
		self.set_transform(new_t)

	def nudge_x(self, sign):
		""" Move along the x axis"""
		delta = np.zeros((4,4))
		translation = self.transform[0:3, 0] * self.scale * 0.001 * sign
		delta[0:3, 3] = translation
		self.set_transform(self.transform + delta)

	def nudge_y(self, sign):
		""" Move along the y axis"""
		delta = np.zeros((4,4))
		translation = self.transform[0:3,1] * self.scale * 0.001 * sign
		delta[0:3, 3] = translation
		self.set_transform(self.transform + delta)
		
	
	def nudge_z(self, sign):
		""" Move along local z axis. """
		delta = np.zeros((4,4))
		translation = self.transform[0:3, 2] * self.scale * 0.001 * sign
		delta[0:3, 3] = translation
		self.set_transform(self.transform + delta)
		
	def update(self, points):
		""" Update state using points """
		
		# Convert points into local coordinate frame
		H = self.inv_transform
		pointsT = np.dot(H[0:3,0:3], points) + H[0:3, 3].reshape((3,1))
		
		# Clip to keyboard dimensions (speeds up later processing)
		big_enough = (pointsT > self.vmin.reshape((3, -1))).min(axis=0)
		small_enough = (pointsT < self.vmax.reshape((3, -1))).min(axis=0)		
		valid_indices = np.multiply(big_enough, small_enough)
		valid_pts = pointsT[:, valid_indices]	   
		
		# Update all the keys 
		for k in self.keys:
			k.update(valid_pts)
		
	def draw(self):
		""" Draw the keys. """
		
		ogl.glPushMatrix()
		ogl.glMultMatrixf(self.transform.T)
		
		# Draw notes
		for k in self.keys:
			if k.pressed:
				ogl.glColor4fv([0,1,0,0.4])				
			else:
				ogl.glColor4fv(k.colour)
			ogl.glVertexPointer(3, ogl.GL_FLOAT, 0, k.quads.T)
			ogl.glDrawArrays(ogl.GL_QUADS, 0, k.quads.shape[1])

		ogl.glPopMatrix()

