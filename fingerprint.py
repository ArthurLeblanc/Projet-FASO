#coding: utf-8

import grovepi
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from driverI2C import *

relay = 3

grovepi.pinMode(relay, "OUTPUT")
#Initialise le capteur
def initialiserCapteur():
	try:
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

		if ( f.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')
		return f
	except Exception as e:
		print("Le capteur n'a pas été détecté !")
		setText("Le capteur n'a pas ete detecte !")
		setrGB(255, 0, 0)
		print('Erreur : ' + str(e))
		exit(1)	
			
#Ajoute une nouvelle empreinte
def ajoutEmpreinte():

	f = initialiserCapteur()
	#Affiche le nombres d'empreintes enregistrées
	print("Nombre d'empreintes enregistrées : " + str(f.getTemplateCount()) +"/"+ str(f.getStorageCapacity()))
	
	#Enregistrement d'une nouvelle empreinte
	try:
		print('Placer un doigt ...')
		setText("Placer un doigt...")
		#Attend que la lecture de l'image du doigt soit finie                                                                                                                                                                                                                                                               
		while ( f.readImage() == False ):
			pass
			

		#Convertis l'image lue précédemment et la stocke dans le charbuffer 1
		f.convertImage(0x01)

		#Recherche si l'empreinte est déjà enregistrée
		result = f.searchTemplate()
		positionNumber = result[0]
	
		if ( positionNumber >= 0 ):
			print('Empreinte déjà enregistrée à la position #' + str(positionNumber))
			setText('Empreinte deja enregistree')
			exit(0)

		print('Retirer le doigt...')
		setText('Retirer le doigt...')
		time.sleep(2)

		print('Replacer le même doigt...')
		setText('Replacer le même doigt...')

		#Attend que la lecture du même doigt soit finie
		while ( f.readImage() == False ):
			pass

		#Convertis l'image lue et la stocke dans le charbuffer 2
		f.convertImage(0x02)

		#Compare les 2 charbuffer
		if ( f.compareCharacteristics() == 0 ):
			raise Exception('Les doigts ne sont pas les mêmes !')
			setText('Les doigts ne sont pas les memes !')

		#Création de l'empreinte
		f.createTemplate()
	
		#Sauvegarde l'empreinte à une nouvelle position
		positionNumber = f.storeTemplate()
		print('Empreinte bien enregistrée! ')
		setText('Empreinte bien enregistree !')
		print('Nouvelle empreinte à la position #' + str(positionNumber))

	except Exception as e:
		print("Erreur, l'opération a échouée")
		setText("Erreur, l'operation a echouee")
		setrGB(255, 0, 0)
		print('Erreur : ' + str(e))
		exit(1)
	
#Supprime une empreinte	
def supprimerEmpreinte():

	f = initialiserCapteur()
	#Affiche le nombres d'empreintes enregistrées
	print("Nombre d'empreintes enregistrees : " + str(f.getTemplateCount()) +"/"+ str(f.getStorageCapacity()))

	#Supression de l'empreinte
	try:
		positionNumber = input("Numéro de l'empreinte à supprimer : ")
		positionNumber = int(positionNumber)

		if ( f.deleteTemplate(positionNumber) == True ):
			print('Empreinte supprimée !')
			setText('Empreinte supprimee !')

	except Exception as e:
		print("Erreur, l'opération a échouée")
		setText("Erreur, l'operation a echouee")
		setrGB(255, 0, 0)
		print('Erreur : ' + str(e))
		exit(1)

#Recherche et compare une empreinte		
def chercherEmpreinte():

	f = initialiserCapteur()
	try:
		print('Placer un doigt ...')
		setText("Placer un doigt...")

		#Attend que la lecture de l'image du doigt soit finie  
		while ( f.readImage() == False ):
			pass

		#Convertis l'image et la stocke dans le charbuffer 1
		f.convertImage(0x01)

		#Recherche l'empreinte
		result = f.searchTemplate()
	
		positionNumber = result[0]
		accuracyScore = result[1]

		if ( positionNumber == -1 ):
			print('Aucune empreinte trouvée !')
			setText('Acces refuse !')
		else:
			print('Empreinte trouvée à la position #' + str(positionNumber))
			setText('Acces autorise !')
			grovepi.digitalWrite(relay, 1)
			time.sleep(0.05)			
			grovepi.digitalWrite(relay, 0)
			print('Précision : ' + str(accuracyScore))

	except Exception as e:
		print("Erreur, l'opération a échouée")
		setText("Erreur, l'operation a echouee")
		setrGB(255, 0, 0)
		print('Erreur : ' + str(e))
		exit(1)

#Liste les empreintes stockées
def afficherEmpreintes():
	f = initialiserCapteur()
	try:
		page = input('Please enter the index page (0, 1, 2, 3) you want to see: ')
		page = int(page)

		tableIndex = f.getTemplateIndex(page)

		for i in range(0, len(tableIndex)):
			print('Position #' + str(i) + ' | Utilisée : ' + str(tableIndex[i]))
	except Exception as e:
		print("Erreur, l'opération a échouée")
		setText("Erreur, l'operation a echouee")
		setrGB(255, 0, 0)
		print('Erreur : ' + str(e))
		exit(1)

#Télécharge l'image de l'empreinte au format bmp
def dlImage():
	f = initialiserCapteur()
	try:
		print('Placer un doigt ...')
		setText("Placer un doigt ...")

		#Attend que la lecture du doigt soit finie
		while ( f.readImage() == False ):
			pass

		print("Téléchargement de l'image")
		setText("Telechargement de l'image")
		imageDestination = 'imagesEmpreintes/fingerprint.bmp'
		f.downloadImage(imageDestination)

		print("L'image a été sauvegardée à " + imageDestination + ".")
		setText("Telecharment terminé !")

	except Exception as e:
		print("Erreur, l'opération a échouée")
		setText("Erreur, l'opération a echouee")
		setrGB(255, 0, 0)
		print('Erreur : ' + str(e))
		exit(1)
