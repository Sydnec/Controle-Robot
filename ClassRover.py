import RPi.GPIO as GPIO
import time

class robot():
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(12,GPIO.OUT) #PWM1-Mot1
		GPIO.setup(32,GPIO.OUT) #PWM2-Mot1
		GPIO.setup(33,GPIO.OUT) #PWM1-Mot2
		GPIO.setup(35,GPIO.OUT) #PWM2-Mot2

		self.p1=GPIO.PWM(12,100)
		self.p2=GPIO.PWM(33,100)
		self.p1b=GPIO.PWM(32,100)
		self.p2b=GPIO.PWM(35,100)
		self.vitesse=100

	def Stop(self):
		self.p1.stop()
		self.p1b.stop()
		self.p2.stop()
		self.p2b.stop()

	def Avant(self):
		self.p1.start(self.vitesse)
		self.p1b.stop()
		self.p2.start(self.vitesse)
		self.p2b.stop()

	def Arriere(self):
		self.p1.stop()
		self.p1b.start(self.vitesse)
		self.p2.stop()
		self.p2b.start(self.vitesse)

	def Droite(self):
		self.p1.start(self.vitesse)
		self.p1b.stop()
		self.p2.stop()
		self.p2b.start(self.vitesse)

	def Gauche(self):
		self.p1.stop()
		self.p1b.start(self.vitesse)
		self.p2.start(self.vitesse)
		self.p2b.stop()

	def Vitesse(self, speed):
		self.vitesse=int(speed)

	def ObsDevant(self):
		Arriere()
		time.sleep(0.4)
		Stop()
		Droite()
		time.sleep(0.4)
		Stop()
