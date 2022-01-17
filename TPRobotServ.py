import socket
import time
import ClassRover
import ClassMCP3204

robot=ClassRover.robot()
capt=ClassMCP3204.MCP3204()

hote = ''
port = 2500

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur ecoute a present sur le port {}".format(port))
connexion_avec_client, infos_connexion = connexion_principale.accept()

msg_recu = b""
memoire = 0
cache=0
Vbat=0

while msg_recu != b"!END#":
	msg_recu = connexion_avec_client.recv(1024)
	# L'instruction ci-dessous peut lever une exception si le message
	# Receptionne comporte des accents
	if msg_recu.decode() [1] == "V":
		mess_str=msg_recu.decode()
		mess_str=mess_str.replace('!VITESSE=','',6)
		mess_str=mess_str.replace('#','',6)
		robot.Vitesse(mess_str)
		time.sleep(0.4)
		memoire=cache
	print(msg_recu.decode())
	if msg_recu==b"!DEPLACEMENT,AVANT#" or memoire==1:
		robot.Avant()
		cache=1
		memoire=0
	if msg_recu==b"!DEPLACEMENT,ARRIERE#" or memoire==2:
		robot.Arriere()
		cache=2
		memoire=0
	if msg_recu==b"!DEPLACEMENT,GAUCHE#" or memoire==3:
		robot.Gauche()
		cache=3
		memoire=0
	if msg_recu==b"!DEPLACEMENT,DROITE#" or memoire==4:
		robot.Droite()
		cache=4
		memoire=0
	if msg_recu==b"!DEPLACEMENT,STOP#":
		robot.Stop()
	if msg_recu==b"!#":
		Vbat=capt.read(3)/443.3
		D1=1/(((capt.read(0)/1241.0)-0.1681)/21.36)
		D2=1/(((capt.read(1)/1241.0)-0.1681)/21.36)
		D3=1/(((capt.read(2)/1241.0)-0.1681)/21.36)
		print('Vbat=',Vbat)
		print('IR1=',D1)
		print('IR2=',D2)
		print('IR3=',D3)
		connexion_avec_client.send(b"!IR1="+str(D1)+"#")
		connexion_avec_client.send(b"!IR2="+str(D2)+"#")
	   	connexion_avec_client.send(b"!IR3="+str(D3)+"#")
	   	connexion_avec_client.send(b"!Ubat="+str(Vbat)+"#")
	if(msg_recu=="!AUTO#"):
		while(True):
			D1=1/(((capt.read(0)/1241.0)-0.1681)/21.36)
			D2=1/(((capt.read(1)/1241.0)-0.1681)/21.36)
			D3=1/(((capt.read(2)/1241.0)-0.1681)/21.36)
			robot.Avant()
			if(D1<=30.0):
				robot.Stop()
				while(D1<30.0):
					robot.Droite()
					D1=1/(((capt.read(0)/1241.0)-0.1681)/21.36)
				robot.Stop()
			if(D2<=30.0):
				robot.Stop()
				while(D2<30.0):
					robot.Droite()
					D2=1/(((capt.read(1)/1241.0)-0.1681)/21.36)
				robot.Stop()
			if(D3<=30.0):
				robot.Stop()
				while(D3<30.0):
					robot.Gauche()
					D3=1/(((capt.read(2)/1241.0)-0.1681)/21.36)
				robot.Stop()
print("Fermeture de la connexion")
connexion_avec_client.close()
connexion_principale.close()