# -*- coding:utf-8 -*-
"""

"""
import kivy
import socket, sys
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.video import Video

class threadReception(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		if app.connexion==0:
			app.socket.send(b"!#")
			msg_recu=app.socket.recv(1024)
			self.mess_str=msg_recu.decode()
			print("reception"+self.mess_str)
			app.lectureCapteur(self.mess_str)
			
class MyApp(App):
	def build(self):
		self.connexion=bool=1
		Window.size = (800,600)
		self.title = "Client ROBOT GEII"
		LayoutRobot=FloatLayout()

		self.ButtonQuit=Button(text='Quitter',size_hint=(.15,.07),pos_hint={'x':.83,'y':0.02})#Bouton pour Quitter
		self.ButtonRequete=Button(text='Requete Capteurs',size_hint=(.20,.07),pos_hint={'x':.25,'y':0.02})#Bouton pour Requete
		self.ButtonConnect=Button(text='Connexion',size_hint=(.15,.07),pos_hint={'x':.01,'y':0.02})#Bouton pour Connexion
		self.ButtonAuto=Button(text='Mode Auto',size_hint=(.15,.07),pos_hint={'x':.55,'y':0.02})#Bouton pour passer en mode auto
		self.ButtonG=Button(text='<-',size_hint=(.1,.1),pos_hint={'x':.59,'y':0.5})#Bouton pour Aller à Gauche
		self.ButtonD=Button(text='->',size_hint=(.1,.1),pos_hint={'x':.81,'y':0.5})#Bouton pour Aller à Droite
		self.ButtonAv=Button(text='Av',size_hint=(.1,.12),pos_hint={'x':.7,'y':0.61})#Bouton pour Avancer
		self.ButtonArr=Button(text='Arr',size_hint=(.1,.12),pos_hint={'x':.7,'y':0.37})#Bouton pour Reculer
		self.ButtonSTOP=Button(text='STOP',size_hint=(.1,.1),pos_hint={'x':.7,'y':0.5})#Bouton pour STOP
		self.slider1=Slider(size_hint=(.4,.1),pos_hint={'x':.5,'y':.8},min=0,max=100,value=50,orientation='horizontal')#Slider Vitesse
		self.LabelVitesse=Label(text='50',font_size=20,pos_hint={'x':.7-0.5,'y':.8-.5})#Affichage vitesse
		self.inputText=TextInput(text='Client non connecté',multiline=True,size_hint=(.40,.60),pos_hint={'x':.0,'y':.40})#Console
		self.inputPort=TextInput(text='Port: 2500',multiline=False,size_hint=(.10,.05),pos_hint={'x':.01,'y':.30})#Port
		self.inputIP=TextInput(text='IP: 10.3.141.1',multiline=False,size_hint=(.20,.05),pos_hint={'x':.12,'y':.30})#IP

		self.ButtonQuit.bind(on_press=self.actionButtonQuit)
		self.ButtonConnect.bind(on_press=self.actionButtonConnect)
		self.ButtonRequete.bind(on_press=self.actionButtonRequete)
		self.ButtonAuto.bind(on_press=self.actionButtonAuto)
		self.ButtonG.bind(on_press=self.actionButtonG)
		self.ButtonD.bind(on_press=self.actionButtonD)
		self.ButtonAv.bind(on_press=self.actionButtonAv)
		self.ButtonArr.bind(on_press=self.actionButtonArr)
		self.ButtonSTOP.bind(on_press=self.actionButtonSTOP)
		self.slider1.bind(value=self.actionSlider1)
		#self.camera=Video(source="http://10.3.141.1:8000/stream.mjpg",state='play',volume=100,options={'allow_stretch':False},size_hint=(.4,.3),pos_hint={'x':.3,'y':.2})

		LayoutRobot.add_widget(self.ButtonQuit)
		LayoutRobot.add_widget(self.ButtonRequete)
		LayoutRobot.add_widget(self.ButtonConnect)
		LayoutRobot.add_widget(self.ButtonAuto)
		LayoutRobot.add_widget(self.ButtonG)
		LayoutRobot.add_widget(self.ButtonD)
		LayoutRobot.add_widget(self.ButtonAv)
		LayoutRobot.add_widget(self.ButtonArr)
		LayoutRobot.add_widget(self.ButtonSTOP)
		LayoutRobot.add_widget(self.slider1)
		LayoutRobot.add_widget(self.LabelVitesse)
		LayoutRobot.add_widget(self.inputText)
		LayoutRobot.add_widget(self.inputPort)
		LayoutRobot.add_widget(self.inputIP)
		#LayoutRobot.add_widget(self.camera)

		return LayoutRobot

	def actionButtonQuit(self,instance):
		print("Fermeture de l'application")
		App.get_running_app().stop()

	def actionButtonConnect(self,instance):
		port=self.inputPort.text.replace('Port: ','')
		hote=self.inputIP.text.replace('IP: ','')
		if self.connexion==1:
			try:
				self.connexion=0
				self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #IPv4, TPC ici
				self.socket.connect((hote,int(port)))
				self.inputText.insert_text('\nConnexion établie avec le serveur.')
				self.ButtonConnect.text="Déconnexion"
			except:
				self.inputText.insert_text('\nLa connexion a échoué')
		else:
			try:
				self.connexion=1
				self.socket.send(b"!END#")
				self.inputText.insert_text('\nDéconnexion avec le serveur')
				self.ButtonConnect.text="Connexion"
			except:
				self.inputText.insert_text('\nDéconnexion avec le serveur échouée')

	def actionButtonRequete(self,instance):
		m=threadReception() #Créer le thread
		m.start()

	def actionButtonAuto(self,instance):
		if auto==1:
			commande="Mode CSV"
		else :
			commande="Mode Telecommande"
		self.socket.send(b"!AUTO#")
		self.inputText.insert_text('\n'+commande)
	def actionButtonG(self,instance):
		commande="Déplacement gauche"
		self.socket.send(b"!DEPLACEMENT,GAUCHE#")
		self.inputText.insert_text('\n'+commande)
	def actionButtonD(self,instance):
		commande="Déplacement droite"
		self.socket.send(b"!DEPLACEMENT,DROITE#")
		self.inputText.insert_text('\n'+commande)

	def actionButtonAv(self,instance):
		commande="Déplacement avant"
		self.socket.send(b"!DEPLACEMENT,AVANT#")
		self.inputText.insert_text('\n'+commande)

	def actionButtonArr(self,instance):
		commande="Déplacement arrière"
		self.socket.send(b"!DEPLACEMENT,ARRIERE#")
		self.inputText.insert_text('\n'+commande)

	def actionButtonSTOP(self,instance):
		commande="Déplacement stop"
		self.socket.send(b"!DEPLACEMENT,STOP#")
		self.inputText.insert_text('\n'+commande)

	def actionSlider1(self,instance,value):
		commande="!VITESSE="+str(int(value))+"#"	
		self.socket.send(commande.encode("Utf8"))
		self.inputText.insert_text('\n'+commande)
		self.LabelVitesse.text=str(int(value))

	def timer(self,dt): #Méthode du Timer
		self.inputText.insert_text('\nAttente réception serveur')
		msg_recu=self.socket.recv(1024)
		mess_str=msg_recu.decode()
		mess_str=mess_str.replace('#','',6)
		mess_str=mess_str.replace('!','\n',6)
		self.inputText.insert_text('\n'+mess_str)
		self.Clock1.cancel() #arrêt du Timer

	def lectureCapteur(self,message):
		self.inputText.insert_text('\n'+message)
		data=message.split('#')
		for line in data:
			print(line)
			"""if line.find('ANGLE')!=-1:
				pos=line.find('=')
				self.LabelAngle.text='ANGLE'+line[pos:len(line)]+'°'"""

if __name__ == "__main__":
	app=MyApp()
	app.run()