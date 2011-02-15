from espeak import espeak
class Append():
	def __init__(self, ui):
		self.ui = ui
	def add(self, letter):
		output = self.ui.plainTextEdit.toPlainText()
		self.ui.plainTextEdit.setPlainText(output + letter)
	def addA(self):
		self.add("A")
	def addB(self):
		self.add("B")
	def addC(self):
		self.add("C")
	def addD(self):
		self.add("D")
	def addE(self):
		self.add("E")
	def addF(self):
		self.add("F")
	def addG(self):
		self.add("G")
	def addH(self):
		self.add("H")
	def addI(self):
		self.add("I")
	def addJ(self):
		self.add("J")
	def addK(self):
		self.add("K")
	def addL(self):
		self.add("L")
	def addM(self):
		self.add("M")
	def addN(self):
		self.add("N")
	def addO(self):
		self.add("O")
	def addP(self):
		self.add("P")
	def addQ(self):
		self.add("Q")
	def addR(self):
		self.add("R")
	def addS(self):
		self.add("S")
	def addT(self):
		self.add("T")
	def addU(self):
		self.add("U")
	def addV(self):
		self.add("V")
	def addW(self):
		self.add("W")
	def addX(self):
		self.add("X")
	def addY(self):
		self.add("Y")
	def addZ(self):
		self.add("Z")
	def addComma(self) :
		self.add(",")
	def addPeriod(self):
		self.add(".")
		self.speak()
	def addExclamation(self):
		self.add("!")
		self.speak()
	def addQuestionmark(self):
		self.add("?")
		self.speak()			
	def addSpace(self):
		self.add(" ")		
	def addEnter(self):
		self.add("\n")
		self.speak()
	def backspace(self):
		output = self.ui.plainTextEdit.toPlainText()
		self.ui.plainTextEdit.setPlainText(output[0:-1])
	def speak(self):
		output = self.ui.plainTextEdit.toPlainText()
		espeak.synth(output.toAscii().data()) 
