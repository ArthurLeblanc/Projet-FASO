# coding: utf-8
#à faire avant de lancer le programme
#i2cset -y 1 0x3e 0x80 0x01
#i2cset -y 1 0x3e 0x80 0x0F
#i2cset -y 1 0x3e 0x80 0x38

#Mémo branchement capteur
#TXD : Blanc
#RXD : Vert
#GND : Noir
#+5V : Rouge

import time
import grovepi
from driverI2C import *
from fingerprint import *

button = 2

grovepi.pinMode(button, "INPUT")

while True:
     try:
         if grovepi.digitalRead(button) == 1:
              chercherEmpreinte()
     except Exception as e:
         print(e)

#ajoutEmpreinte()
#supprimerEmpreinte()
#chercherEmpreinte()
#afficherEmpreintes()
#dlImage()
#setText("Test")

#setText("Salut Polytech! Test ecran LCD aaaaaaaaaa")

#setRGB(128,128,64)
#time.sleep(2)

#for c in range(0,200):
#	setRGB(c,200-c,0)
#	time.sleep(0.1)
#setRGB(0,255,0)
#setText("Bye!")
