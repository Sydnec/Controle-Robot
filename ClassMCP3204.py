"""
	Classe du convertisseur A/N MCP3204
	Relie sur le bux SPI (bus=0, device=1)
"""
import RPi.GPIO as GPIO
import spidev
import time

class MCP3204():
	#Constructeur
	def __init__(self):
		self.spi=spidev.SpiDev() #Cree l'objet spi
		self.spi.open(0,1)
		self.spi.max_speed_hz=1000000 #Definie la vitesse de la clock a 1MHz
	#Destructeur
	def __del__(self):
		self.close
	#Fermeture
	def close():
		if self.active:
			self.spi.close()
			self.active=False
	#Methode de lecture du convertisseur
	def read(self, channel=0):
		command=128+64+(channel<<3)
		result=self.spi.xfer2([command,0,0,0]) #Transmition de 4 octets
		value=(result[0]<<3)*256+(result[1]<<3)+(result[2]>>5)
		return value