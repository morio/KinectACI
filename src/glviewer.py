from PyQt4 import QtCore
import PyQGLViewer
import OpenGL.GL as ogl
import numpy as np
import freenect
from keyboard import Keyboard

SAMPLE_STRIDE = 2		  # Divide depth map resolution by this amount
# Precompute U, V coordinates (since they never change)

class Viewer(PyQGLViewer.QGLViewer):
	""" Subclass PyQGLViewer to provide additional functionality. """
	
	def __init__(self, connector):
		PyQGLViewer.QGLViewer.__init__(self)
		self.U, self.V = np.meshgrid(np.arange(0,640, SAMPLE_STRIDE), np.arange(0,480, SAMPLE_STRIDE))
		
		self.points = np.zeros((3,1))
		self.connector = connector
		self.keyboards = [Keyboard(Keyboard.TYPE_FORWARD, 4, 1, 1, 0.001, 0,"keyboard1.npy" , connector), \
						Keyboard(Keyboard.TYPE_REVERSE, 4, 1, 1, 0.001, -8, "keyboard2.npy", connector), \
						Keyboard(Keyboard.TYPE_SELECT, 1, 2, 2, 0.01, -16, "keyboard3.npy", connector),\
						Keyboard(Keyboard.TYPE_DIRECTION_TOGGLE,1,2,2,0.01,8, "keyboard4.npy", connector) ]
		self.num_keyboard = 4
		self.keyboard = self.keyboards[0]
	def init(self):
		""" For initialisation once OpenGL context is created. """
		self.setAnimationPeriod(33)
		
		ogl.glDisable(ogl.GL_LIGHTING)
		ogl.glEnableClientState(ogl.GL_VERTEX_ARRAY)
		ogl.glEnable(ogl.GL_BLEND)
		ogl.glBlendFunc(ogl.GL_SRC_ALPHA, ogl.GL_ONE_MINUS_SRC_ALPHA)
		ogl.glEnable(ogl.GL_CULL_FACE)
		ogl.glPointSize(2.0)

		self.setStateFileName('keyboard_anywhere.xml')
		if not self.restoreStateFromFile():
			self.camera().setSceneRadius(500)
		
		# Make key commands appear in the help
		self.kbt = ['lower left', 'lower right', 'upper left']
		self.setKeyDescription(QtCore.Qt.Key_1, 
				'set the {0} point of the keyboard'.format(self.kbt[0]))		
		self.setKeyDescription(QtCore.Qt.Key_2, 
				'set the {0} point of the keyboard'.format(self.kbt[1]))		
		self.setKeyDescription(QtCore.Qt.Key_3, 
				'set the {0} point of the keyboard'.format(self.kbt[2]))
		self.setKeyDescription(QtCore.Qt.Key_Z,
				'shift the keyboard slightly in the local +Z direction')
		self.setKeyDescription(QtCore.Qt.ShiftModifier + QtCore.Qt.Key_Z,
				'shift the keyboard slightly in the local -Z direction')
		self.setKeyDescription(QtCore.Qt.Key_Plus, 
				'rotate the keyboard slightly about the local +Y axis')
		self.setKeyDescription(QtCore.Qt.Key_Minus, 
				'rotate the keyboard slightly about the local -Y axis')

		
		self.tilt = 0; 
		self.kb_corners = np.zeros((3,3))
		self.kb_corner_index = 0				
	def depth_to_xyz(self,u, v, stride, depth):
		""" Convert depth map to cartesian coordinates. 		
		Parameters as originally determined by Zephod (? I think). Or found on
		the OpenKinect.org mailing list
		
		"""
		
		depth_flipped = depth[::-stride, ::stride]
		valid = depth_flipped != 2047	# Non-return = 2047
		
		us = u[valid].flatten()
		vs = v[valid].flatten()
		ds = depth_flipped[valid]
	
		KinectMinDistance = -10
		KinectDepthScaleFactor = .0021
		
		zz = 100.0 / (-0.00307 * ds + 3.33)
		xx = (us - 320) * (zz + KinectMinDistance) * KinectDepthScaleFactor
		yy = (vs - 240) * (zz + KinectMinDistance) * KinectDepthScaleFactor
		zz = -(zz - 200)	# Move sensor from origin (easier for displaying)
		
		points = np.vstack((xx,yy,zz)).astype(float)
		return points					 


		
	def animate(self):
		""" Get the latest data from the kinect, and update the state. """

			
		depth, timestamp = freenect.sync_get_depth()

		xyz = self.depth_to_xyz(self.U, self.V, SAMPLE_STRIDE, np.array(depth))
		self.points = xyz
		for board in self.keyboards :
			board.update(self.points)
	
	def draw(self):
		""" Draw the point cloud and keyboard. """ 
		ogl.glColor4f(0.6,0.6,0.6,1)
		ogl.glVertexPointer(3, ogl.GL_FLOAT, 0, self.points.T)
		ogl.glDrawArrays(ogl.GL_POINTS, 0, self.points.shape[1])
		for board in self.keyboards :
			board.draw()

	def keyPressEvent(self, event):
		""" Handle keyboard events. """		
		if event.key() == QtCore.Qt.Key_F1:
			self.kb_corner_index = 0
			self.displayMessage('shift + click to set {0} corner'.format(self.kbt[0]))
		elif event.key() == QtCore.Qt.Key_F2:
			self.kb_corner_index = 1
			self.displayMessage('shift + click to set {0} corner'.format(self.kbt[1]))
		elif event.key() == QtCore.Qt.Key_F3:
			self.kb_corner_index = 2
			self.displayMessage('shift + click to set {0} corner'.format(self.kbt[2]))
		elif event.key() == QtCore.Qt.Key_Z:
			# Shift the keyboard in Z	
			if event.modifiers() and QtCore.Qt.ShiftModifier:
				self.keyboard.nudge_z(-1)
				self.displayMessage("Move in negative z-axis")
			else:
				self.keyboard.nudge_z(1)					   
				self.displayMessage("Move in positive z-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_R:
			self.keyboard.nudge_pitch(1)
			self.displayMessage("Rotate clockwise around x-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_F:
			self.displayMessage("Rotate counter-clockwise around x-axis")
			self.keyboard.nudge_pitch(-1)
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_C:
			# Rotate the keyboard
			self.keyboard.nudge_roll(1)  
			self.displayMessage("Rotate clockwise around y-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_X:	  
			# Rotate the keyboard
			self.keyboard.nudge_roll(-1)
			self.displayMessage("Rotate counter-clockwise around y-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_E:
			self.keyboard.nudge_yaw(1)
			self.displayMessage("Rotate clockwise around z-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_Q:
			self.keyboard.nudge_yaw(-1)
			self.displayMessage("Rotate counter-clockwise around z-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_I:
			self.keyboard.scale_x(1)
			self.displayMessage("Scale up x-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_J:
			self.keyboard.scale_x(-1)
			self.displayMessage("Scale down x-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_O:
			self.keyboard.scale_y(1)
			self.displayMessage("Scale up y-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_K:
			self.keyboard.scale_y(-1)
			self.displayMessage("Scale down y-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_P :
			self.keyboard.scale_z(1)
			self.displayMessage("Scale up z-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_L :
			self.keyboard.scale_z(-1)
			self.displayMessage("Scale down z-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_A:
			self.keyboard.nudge_x(-1)
			self.displayMessage("Move in negative x-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_D:
			self.keyboard.nudge_x(1)
			self.displayMessage("Move in positive x-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_W:
			self.keyboard.nudge_y(1)
			self.displayMessage("Move in positive y-axis")			
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_S:
			self.keyboard.nudge_y(-1)
			self.displayMessage("Move in negative y-axis")
			self.updateGL()
		elif event.key() == QtCore.Qt.Key_Plus and QtCore.Qt.ShiftModifier:
			self.keyboard.scale += 10
			self.displayMessage("Transform scale is set to {0}".format(self.keyboard.scale))
		elif event.key() == QtCore.Qt.Key_Plus:
			self.keyboard.scale += 1
			self.displayMessage("Transform scale is set to {0}".format(self.keyboard.scale))
		elif event.key() == QtCore.Qt.Key_Minus and QtCore.Qt.ShiftModifier:
			if self.keyboard.scale > 10.0 :
				self.keyboard.scale -= 10
				self.displayMessage("Transform scale is set to {0}".format(self.keyboard.scale))
		elif event.key() == QtCore.Qt.Key_Minus:
			if self.keyboard.scale > 1.0 :
				self.keyboard.scale -= 1
				self.displayMessage("Transform scale is set to {0}".format(self.keyboard.scale))
		elif event.key() == QtCore.Qt.Key_1:
			self.keyboard = self.keyboards[0]
			self.displayMessage("Seleccted first keyboard - Forward")
		elif event.key() == QtCore.Qt.Key_2:
			self.keyboard = self.keyboards[1]
			self.displayMessage("Selected second keyboard - Reverse")
		elif event.key() == QtCore.Qt.Key_3:
			self.keyboard = self.keyboards[2]
			self.displayMessage("Selected third keyboard - Select")
		elif event.key() == QtCore.Qt.Key_4:
			self.keyboard = self.keyboards[3]
			self.displayMessage("Selected fourth keyboard - Direction toggle")
		else:
			PyQGLViewer.QGLViewer.keyPressEvent(self, event)
	
	def compute_keyboard_transformation(self):
		""" Compute the keyboard transform from the corner points. """
		
		def unitize(v):
			return v / np.linalg.norm(v)
			
		translation = self.kb_corners[:, 0]	

		x_axis = np.subtract(self.kb_corners[:, 1], self.kb_corners[:, 0])
		scale = np.linalg.norm(x_axis)	# Length of keyboard	   

		planar_vec = np.subtract(self.kb_corners[:, 2], self.kb_corners[:, 0])
		z_axis = unitize(np.cross(x_axis, planar_vec)) * scale
		y_axis = -unitize(np.cross(x_axis, z_axis)) * scale			

		rot_scale = np.vstack((x_axis, y_axis, z_axis)).T
		
		# H stores the computed transform
		H = np.eye(4)
		H[0:3, 0:3] = rot_scale
		H[0:3, 3] = translation
		
		self.keyboard.set_transform(H)
	
	def select(self, event):
		""" Handler for mouse select event. """
		pos = event.pos()		
		pt, ok = self.camera().pointUnderPixel(pos)
		if(ok):
			cnr_txt = self.kbt[self.kb_corner_index]
			self.displayMessage('{0} corner is set'.format(cnr_txt))
			self.kb_corners[:, self.kb_corner_index] = list(pt)			
			self.compute_keyboard_transformation()

	def helpString(self):
		""" Text shown in help window. """
		output = "<h2>keyboard-anywhere</h2>"
		output += "<p>Press ENTER to start/stop live display of Kinect Data.</p>"
		output += "<p>Press F1, F2 or F3 to set the keyboard anchor points.</p>"
		output += "<p>Press the virtual keys to play!</p>"
		return output
