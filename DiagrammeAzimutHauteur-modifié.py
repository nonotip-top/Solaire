
import matplotlib.pyplot as plt
import numpy as np
from math import sin,  cos,  tan, asin, atan, acos



############CALCUL DES MAX"""""


latitude = 35  # latitude
phi=np.radians(latitude)



 # ------------------------FONCTIONS
 
def elevation(D,H):
    return np.degrees(asin(sin(np.radians(D))*sin(phi)+cos(np.radians(D))*cos(phi)*cos(np.radians(H))))

hauteur_vect = np.vectorize(elevation)

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
plt.xlim(-180, 180)

plt.ylim(0, 90)
plt.xlabel("Azimut (°)")
plt.ylabel("Hauteur (°)")

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




#Tracé des lignes horaires :-------------------------------------------------

decl = np.arange(-23.4, 23.4, 0.05)
for H in np.arange(-180,  + 180, 15): # heures pleines
    A = azimut_vect(decl, H)
    h = hauteur_vect(decl, H)
    plt.plot(A, h)

        



#courbes de déclinaison ::-------------------------------------------------
H = np.arange(-180, 180, 0.1)
for D in [22, 11,0,-11,-22]:
    A = azimut_vect(D, H)
    h = hauteur_vect(D, H)
    plt.plot(A, h)








plt.show()

