#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@auteur: david ALBERTO (www.astrolabe-science.fr)
# Diagramme solaire en azimut et hauteur
"""
import matplotlib.pyplot as plt
import numpy as np
from math import sin,  cos,  tan, asin, atan, acos

latitude = 5
couleur_lignes_H = 'indigo'
#Réglage du colormap pour les courbes de déclinaison :

# plt.rcParams["font.family"] = "Roboto" # ou autre police installée

plt.rcParams["font.size"] = 14

phi=np.radians(latitude)
Titre = 'diagramme_azimut_hauteur' + str(latitude)

hauteurmax=90+23.4-np.degrees(phi)#hauteur méridienne au 21 juin, pour l'échelle de hauteur

cosmaxH=-tan(phi)*tan(np.radians(23.4))#angle horaire maxi au 21 juin, pour les heures de lever/coucher
if abs(cosmaxH) <=1:
    maxH = np.degrees(acos(cosmaxH))
else:
    maxH = 180
maxH=int(maxH/15)*15

maxAz=np.degrees(acos(-sin(np.radians(23.4)/cos(phi))))#azimut maximal au lever/coucher, pour l'axe x
maxAz=int(maxAz/20+1)*20

 # ------------------------FONCTIONS
 
def calcul_hauteur(D,H):
    # renvoie la hauteur du Soleil, d'après la déclinaison D et l'angle horaire H
    return np.degrees(asin(sin(np.radians(D))*sin(phi)+cos(np.radians(D))*cos(phi)*cos(np.radians(H))))

hauteur_vect = np.vectorize(calcul_hauteur)

def calcul_azimut(D, H) :
    # renvoie l'azimut corrigé
    Az=np.degrees(atan(sin(np.radians(H))/(sin(phi)*cos(np.radians(H))-cos(phi)*tan(np.radians(D)))))
    if Az<0 and H>0:
        Az=Az+180
    elif Az>0 and H<0:
        Az=Az-180
    return Az

azimut_vect = np.vectorize(calcul_azimut)
# -------------------------------------------

#paramètres du graphique :
fig=plt.figure(figsize=(12, 9), tight_layout=True)
ax=plt.subplot()
plt.xticks(np.arange(-150, 200, 50))#graduations chiffrées en azimut
plt.xlim(-maxAz, maxAz)
plt.title(Titre)
plt.text(0.005, 0.993, r'Latitude $\mathbf{%.1f}$°'%(np.degrees(phi)),
         color='red', va='top', fontsize=16, transform=ax.transAxes,
         bbox=dict(facecolor='white', edgecolor='black'))
plt.ylim(0, int(hauteurmax+5))
plt.xlabel("Azimut (°)")
plt.ylabel("Hauteur (°)")
plt.yticks(np.arange(0, hauteurmax*1.1, 5))#graduations chiffrées en azimut

#pts cardinaux :
cardinaux={'N-E':-135,
           'Est': -90,
           'S-E': -45,
           'S-O': 45,
           'Ouest': 90,
           'N-O': 135}

for direction in cardinaux:
    plt.text(cardinaux[direction], -2.5, direction,
             va='top', ha='center', rotation=90)


#Grille :
minor_xticks = np.arange(-maxAz, maxAz, 10)#espaces de la grille
minor_yticks = np.arange(0, int(hauteurmax+7), 1)#espaces de la grille
ax.set_xticks(minor_xticks, minor=True)
ax.set_yticks(minor_yticks, minor=True)
ax.grid(which='minor', alpha=0.2)
plt.grid()

#Tracé des lignes horaires :-------------------------------------------------

decl = np.arange(-23.4, 23.4, 0.05)
for H in np.arange(-maxH, maxH + 15, 15): # heures pleines
    A = azimut_vect(decl, H)
    h = hauteur_vect(decl, H)
    plt.plot(A, h, c = couleur_lignes_H)
    #chiffres des heures

for H in np.arange(-maxH + 7.5, maxH + 7.5, 15): # demi-heures
    A = azimut_vect(decl, H)
    h = hauteur_vect(decl, H)
    plt.plot(A, h, c = couleur_lignes_H, alpha = 0.6, lw=0.8)

#courbes de déclinaison ::-------------------------------------------------
# couleursdecl=['crimson', 'blueviolet', 'royalblue','blue', 'green', 'orange',
#               'darkolivegreen']
datesdecl=['21 juin.', '21 mai et 23 juil.','20 avr. et 23 aou.',
            '20 mar. et 23 sept.', '19 fév. et 23 oct.', '20 jan. et 22 nov.',
            '21 déc']

H = np.arange(-maxH, maxH, 0.1)
for i,  D in enumerate([23.4, 20.15, 11.5, 0, -11.5, -20.15, -23.4]):
    A = azimut_vect(D, H)
    h = hauteur_vect(D, H)
    plt.plot(A, h,label=datesdecl[i])

#-------------------------------Courbes de date supplémentaire
"""
datesup=['10 nov.']
declsup=[-17.25]
for i,  D in enumerate(declsup):
    A = azimut_vect(D, H)
    h = hauteur_vect(D, H)
    plt.plot(A, h, c=couleursdecl[i], ls = '--', label=datesup[i])
"""
#------------------------------------------------
plt.legend()
plt.show()

