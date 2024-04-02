from math import *
import numpy as np
for latitude in range(1,90):
    phi=np.radians(latitude)

    hauteurmax=90+23.4-np.degrees(phi)#hauteur méridienne au 21 juin, pour l'échelle de hauteur
    cosmaxH=-tan(phi)*tan(np.radians(23.4))#angle horaire maxi au 21 juin, pour les heures de lever/coucher

    if abs(cosmaxH) <=1:
        maxH = np.degrees(acos(cosmaxH))
    else:
        maxH = 180
    maxH=int(maxH/15)*15

    print(cosmaxH)