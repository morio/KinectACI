from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal
from keyboard import Keyboard
from append import Append

class Connector(QtCore.QObject):
	sendkey = pyqtSignal(int, int, name="sendkey")
	def __init__(self, ui, typewriter):
		QtCore.QObject.__init__(self)
		self.ui = ui
		self.typewriter = typewriter
		self.append = Append(ui)
		self.direction_forward = True
	def connect(self):
		self.ui.pushButton_A.clicked.connect(self.append.addA)
		self.ui.pushButton_B.clicked.connect(self.append.addB)
		self.ui.pushButton_C.clicked.connect(self.append.addC)
		self.ui.pushButton_D.clicked.connect(self.append.addD)
		self.ui.pushButton_E.clicked.connect(self.append.addE)
		self.ui.pushButton_F.clicked.connect(self.append.addF)
		self.ui.pushButton_G.clicked.connect(self.append.addG)
		self.ui.pushButton_H.clicked.connect(self.append.addH)
		self.ui.pushButton_I.clicked.connect(self.append.addI)
		self.ui.pushButton_J.clicked.connect(self.append.addJ)
		self.ui.pushButton_K.clicked.connect(self.append.addK)
		self.ui.pushButton_L.clicked.connect(self.append.addL)
		self.ui.pushButton_M.clicked.connect(self.append.addM)
		self.ui.pushButton_N.clicked.connect(self.append.addN)
		self.ui.pushButton_O.clicked.connect(self.append.addO)
		self.ui.pushButton_P.clicked.connect(self.append.addP)
		self.ui.pushButton_Q.clicked.connect(self.append.addQ)
		self.ui.pushButton_R.clicked.connect(self.append.addR)
		self.ui.pushButton_S.clicked.connect(self.append.addS)
		self.ui.pushButton_T.clicked.connect(self.append.addT)
		self.ui.pushButton_U.clicked.connect(self.append.addU)
		self.ui.pushButton_V.clicked.connect(self.append.addV)
		self.ui.pushButton_W.clicked.connect(self.append.addW)
		self.ui.pushButton_X.clicked.connect(self.append.addX)
		self.ui.pushButton_Y.clicked.connect(self.append.addY)
		self.ui.pushButton_Z.clicked.connect(self.append.addZ)
		self.ui.pushButton_Comma.clicked.connect(self.append.addComma)
		self.ui.pushButton_Enter.clicked.connect(self.append.addEnter)
		self.ui.pushButton_Exclamation.clicked.connect(self.append.addExclamation)
		self.ui.pushButton_QuestionMark.clicked.connect(self.append.addQuestionmark)
		self.ui.pushButton_Backspace1.clicked.connect(self.append.backspace)
		self.ui.pushButton_Backspace2.clicked.connect(self.append.backspace)
		self.ui.pushButton_Period1.clicked.connect(self.append.addPeriod)
		self.ui.pushButton_Period2.clicked.connect(self.append.addPeriod)
		self.ui.pushButton_Period3.clicked.connect(self.append.addPeriod)
		self.ui.pushButton_Space1.clicked.connect(self.append.addSpace)
		self.ui.pushButton_Space2.clicked.connect(self.append.addSpace)
		self.ui.pushButton_Space3.clicked.connect(self.append.addSpace)

	def typewriterSlot(self, type, number):
		print "got to typewriter slot:", type, number
		if(type == Keyboard.TYPE_SELECT):
			self.typewriter.focusWidget().click()
		elif(type == Keyboard.TYPE_FORWARD):
			if(self.direction_forward) :
				self.typewriter.focusNextChild()
			else :
				self.typewriter.focusPreviousChild()
		elif type == Keyboard.TYPE_REVERSE:
			if(self.direction_forward) :
				self.typewriter.focusPreviousChild()
			else :
				self.typewriter.focusNextChild()
		elif type == Keyboard.TYPE_DIRECTION_TOGGLE:
			self.direction_forward = not self.direction_forward