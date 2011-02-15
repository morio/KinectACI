import pygame
from PyQt4.QtCore import QObject, QEvent
AUDIO_PATH = "../audio"
class onFocusManager(QObject):
	def __init__(self):
		QObject.__init__(self)
		self.sA = pygame.mixer.Sound(AUDIO_PATH+"/A.wav")
		self.sB = pygame.mixer.Sound(AUDIO_PATH+"/B.wav")
		self.sC = pygame.mixer.Sound(AUDIO_PATH+"/C.wav")
		self.sD = pygame.mixer.Sound(AUDIO_PATH+"/D.wav")
		self.sE = pygame.mixer.Sound(AUDIO_PATH+"/E.wav")
		self.sF = pygame.mixer.Sound(AUDIO_PATH+"/F.wav")
		self.sG = pygame.mixer.Sound(AUDIO_PATH+"/G.wav")
		self.sH = pygame.mixer.Sound(AUDIO_PATH+"/H.wav")
		self.sI = pygame.mixer.Sound(AUDIO_PATH+"/I.wav")
		self.sJ = pygame.mixer.Sound(AUDIO_PATH+"/J.wav")
		self.sK = pygame.mixer.Sound(AUDIO_PATH+"/K.wav")
		self.sL = pygame.mixer.Sound(AUDIO_PATH+"/L.wav")
		self.sM = pygame.mixer.Sound(AUDIO_PATH+"/M.wav")
		self.sN = pygame.mixer.Sound(AUDIO_PATH+"/N.wav")
		self.sO = pygame.mixer.Sound(AUDIO_PATH+"/O.wav")
		self.sP = pygame.mixer.Sound(AUDIO_PATH+"/P.wav")
		self.sQ = pygame.mixer.Sound(AUDIO_PATH+"/Q.wav")
		self.sR = pygame.mixer.Sound(AUDIO_PATH+"/R.wav")
		self.sS = pygame.mixer.Sound(AUDIO_PATH+"/S.wav")
		self.sT = pygame.mixer.Sound(AUDIO_PATH+"/T.wav")
		self.sU = pygame.mixer.Sound(AUDIO_PATH+"/U.wav")
		self.sV = pygame.mixer.Sound(AUDIO_PATH+"/V.wav")
		self.sW = pygame.mixer.Sound(AUDIO_PATH+"/W.wav")
		self.sX = pygame.mixer.Sound(AUDIO_PATH+"/X.wav")
		self.sY = pygame.mixer.Sound(AUDIO_PATH+"/Y.wav")
		self.sZ = pygame.mixer.Sound(AUDIO_PATH+"/Z.wav")
		self.sComma = pygame.mixer.Sound(AUDIO_PATH+"/comma.wav")
		self.sClear = pygame.mixer.Sound(AUDIO_PATH+"/clear.wav")
		self.sEnter = pygame.mixer.Sound(AUDIO_PATH+"/enter.wav")
		self.sExclamation = pygame.mixer.Sound(AUDIO_PATH+"/exclamation.wav")
		self.sPeriod = pygame.mixer.Sound(AUDIO_PATH+"/period.wav")
		self.sSpace = pygame.mixer.Sound(AUDIO_PATH+"/space.wav")
		self.sQuestion = pygame.mixer.Sound(AUDIO_PATH+"/question.wav")
		self.sBackspace = pygame.mixer.Sound(AUDIO_PATH+"/backspace.wav")
	def eventFilter(self, obj, event):
		if(event.type() == QEvent.FocusIn):
			if(obj.objectName() == "pushButton_A"):
				self.sA.play()
			elif(obj.objectName() == "pushButton_B"):
				self.sB.play()	
			elif(obj.objectName() == "pushButton_C"):
				self.sC.play()	
			elif(obj.objectName() == "pushButton_D"):
				self.sD.play()	
			elif(obj.objectName() == "pushButton_E"):
				self.sE.play()	
			elif(obj.objectName() == "pushButton_F"):
				self.sF.play()	
			elif(obj.objectName() == "pushButton_G"):
				self.sG.play()	
			elif(obj.objectName() == "pushButton_H"):
				self.sH.play()	
			elif(obj.objectName() == "pushButton_I"):
				self.sI.play()	
			elif(obj.objectName() == "pushButton_J"):
				self.sJ.play()	
			elif(obj.objectName() == "pushButton_K"):
				self.sK.play()	
			elif(obj.objectName() == "pushButton_L"):
				self.sL.play()	
			elif(obj.objectName() == "pushButton_M"):
				self.sM.play()	
			elif(obj.objectName() == "pushButton_N"):
				self.sN.play()	
			elif(obj.objectName() == "pushButton_O"):
				self.sO.play()	
			elif(obj.objectName() == "pushButton_P"):
				self.sP.play()	
			elif(obj.objectName() == "pushButton_Q"):
				self.sQ.play()	
			elif(obj.objectName() == "pushButton_R"):
				self.sR.play()	
			elif(obj.objectName() == "pushButton_S"):
				self.sS.play()	
			elif(obj.objectName() == "pushButton_T"):
				self.sT.play()	
			elif(obj.objectName() == "pushButton_U"):
				self.sU.play()	
			elif(obj.objectName() == "pushButton_V"):
				self.sV.play()	
			elif(obj.objectName() == "pushButton_W"):
				self.sW.play()	
			elif(obj.objectName() == "pushButton_X"):
				self.sX.play()	
			elif(obj.objectName() == "pushButton_Y"):
				self.sY.play()	
			elif(obj.objectName() == "pushButton_Z"):
				self.sZ.play()	
			elif(obj.objectName() == "pushButton_Comma"):
				self.sComma.play()
			elif(obj.objectName() == "pushButton_Clear"):
				self.sClear.play()
			elif(obj.objectName() == "pushButton_Enter"):
				self.sEnter.play()
			elif(obj.objectName() == "pushButton_Exclamation"):
				self.sExclamation.play()
			elif(obj.objectName() == "pushButton_Period1" or \
				 obj.objectName() == "pushButton_Period2" or \
				 obj.objectName() == "pushButton_Period3"):
				self.sPeriod.play()
			elif(obj.objectName() == "pushButton_Space1" or \
				 obj.objectName() == "pushButton_Space2" or \
				 obj.objectName() == "pushButton_Space3"):
				self.sSpace.play()
			elif(obj.objectName() == "pushButton_QuestionMark"):
				self.sQuestion.play()
			elif(obj.objectName() == "pushButton_Backspace1" or \
				 obj.objectName() == "pushButton_Backspace2") :
				self.sBackspace.play()
		return False
