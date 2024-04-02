import math as m
import matplotlib.pyplot as plt
import numpy as np
from sun_position_calculator import SunPositionCalculator
from datetime import datetime, timezone
import sys




def cosd(x):
    return(m.cos(m.radians(x)))

def sind(x):
    return(m.sin(m.radians(x)))

def tand(x):
    return(m.tan(m.radians(x)))

def asind(x):
    return(m.degrees(m.asin(x)))

def acosd(x):
    return(m.degrees(m.acos(x)))

def atand(x):
    return(m.degrees(m.atan(x)))


# <----------Repérage d'une date---------->
### Repérage du jour dans l'année
def jour_annee(j:int=16,m:int=5): 
    if 1 <= j <= 31 :
        if  0<m<3 :
            N = j + 31*(m-1)
        elif m<=12 :
            N = j + 31*(m-1) - int(0.4*m+2.3)
        else:
            raise Exception("jour ou mois incorrect")
        return(N)

### Repérage dans la journée (angle horaire)
def angle_horaire(H:float):
    #H = TSV (0->24)
    if 0 <= H <= 24 :
        w=15*(H-12)
    else :
        raise Exception("Heure incorrecte")
    return(w)
    
    
### Conversion UNIXTIME

def convertir_en_unixtime(heure, jour, mois, annee=2023):
  """
  Converti une date en (heure, jour, mois) en Unixtime.

  Args:
    heure: Heure de la journée (0-23).
    jour: Jour du mois (1-31).
    mois: Mois de l'année (1-12).
    annee: Année (optionnel, par défaut 2023).

  Retourne:
    L'Unixtime de la date spécifiée.
  """
  date_naive = datetime(int(annee), int(mois), int(jour), int(heure))
  date_aware = date_naive.replace(tzinfo=timezone.utc)
  unixtime = date_aware.timestamp()
  return unixtime


# <----------Position des astres dans le ciel---------->   
### Trajectoire de la Terre autour du soleil (déclinaison)
def declinaison(N:int):
    # N jour de l'année
    d=23.45*sind( (360/365) * (N-81) )
    return(d)

### Elevation et Azimut
def elevation_azimuth(d,w,lat=43):
    """
    Args:
        d (float): déclinaison solaire 
        w (float): angle horaire 
        lat (float): latitude (degrés)
    Returns:
    retourne le tuple (élevation , azimut)
    """
    phi=np.radians(lat)
    if (abs(phi)>(66.55)):
        raise Exception("Erreur : Pas de lever ou coucher du Soleil dans cette région")
    e = np.degrees(m.sin(m.sin(np.radians(d))*m.sin(phi)+m.cos(np.radians(d))*m.cos(phi)*m.cos(np.radians(w))))
    a = np.degrees(m.atan(m.sin(np.radians(w))/(m.sin(lat)*m.cos(np.radians(w))-m.cos(phi)*m.tan(np.radians(d)))))
    if a<0 and w>0:
        a += 180 
    elif a>0 and w<0:
        a -= 180
    return (e,a)





def angle_horaire_coucher(l,d):
    """
    Args:
        l: latitude
        d: déclinaison
    L'angle horaire au moment du lever ou du coucher (azimut=0)
    """
    return acosd(- tand(l)*tand(d))
 

def h_culmination(l,d):
    """
    Retourne la hauteur de culmination
    Args:
        l (float): latitude
        d (float): déclinaison
    """
    return 90 - l +d


def duree_jour(l=43.3,n:int=10):  #Pau par défaut 
    
    """
    Affiche la durée du jour sur une année (!valable seulement hémisphère Nord!)
    Args:
        l: latitude du lieu
    """
    Jours = []
    Lever = []
    Coucher = []
    for n in range(0,366):
        # n jour dans l'année
        d = declinaison(n)
        w0 = angle_horaire_coucher(l,d)
        
        duree_j = 2 * w0 /15 
        #duree du jour
        
        lever = 12 - duree_j / 2 
        coucher = 12 + duree_j / 2 
        Jours.append(n)
        Lever.append(lever)
        Coucher.append(coucher)
        
    debut = np.zeros(len(Jours))
    fin = 24 * np.ones(len(Jours))
    plt.plot(Jours,Lever,label="Lever du Soleil", color='orange')
    plt.plot(Jours,Coucher, label="Coucher du Soleil", color='r')
    plt.ylim(0, 24)
    
    fill_1 = plt.fill_between(Jours, debut, Lever, color='gray', alpha=0.5)
    fill_2 = plt.fill_between(Jours, Coucher, fin, color='gray', alpha=0.5)
    plt.legend(handles=[fill_1, plt.gca().lines[0]], labels=['Nuit', 'Lever/Coucher'])  

    #equinoxes
    Y = np.linspace(0, 24, 24) #ligne verticale
    printemps = np.full(24, 88)
    automne = np.full(24, 266)
    plt.plot(printemps, Y, color='g', label="équinoxe printemps")
    plt.plot(automne, Y, color='pink', label="équinoxe automne")


    plt.title(f"Lever et Coucher du Soleil à la latitude {l}")
    plt.xlabel("Jour dans l'année")
    plt.ylabel('Heure de la journée')
    plt.legend(title='Légende', loc='upper right', fontsize=12, frameon=True)
    plt.show() 
    
    
 ##### DIAGRAMME SOLAIRE #####   

duree_jour()
def diagramme_solaire(latitude:float=23,nb_h:int=10):
    """
    Affiche un diagramme solaire cartésien du lieu
    Args:
        l: latitude du lieu
        nb_h: Nombre d'heures dans la boucle horaire
    """

    ### Creation des listes ###
    liste_declinaisons = np.arange(-180, 180, 0.1) 
    if nb_h!=0:
        pas=48/nb_h
    else:
        raise Exception("Erreur pas de temps invalide")
    liste_heures = np.linspace(-24,24,nb_h)
        
    ### Courbes de déclinaison ###
    for d in liste_heures:    #Boucle de déclinaisons
        liste_elevations=[]
        liste_azimuts=[]
        for w in liste_declinaisons:   #boucle d'angles horaires
        
            e,a = elevation_azimuth(d,w,latitude)
            liste_azimuts.append(a)
            liste_elevations.append(e)
        plt.plot(liste_azimuts,liste_elevations)    

    ### Courbes horaires ###
    Liste_declinaison = np.arange(-23.4, 23.4, 0.5)
    for w in np.arange(-180,  + 180, 15): # heures pleines
        liste_elevations=[]
        liste_azimuts=[]
        for d in Liste_declinaison:
            e,a = elevation_azimuth(d,w,latitude)
            if e>0:
                if a<0 and w>0:#test de l'azimut
                    a=a+180
                else:
                    if a>0 and w<0:
                        a=a-180
                    liste_azimuts.append(a)
                    liste_elevations.append(e)
        plt.plot(liste_azimuts,liste_elevations)


  
            

    
    Titre = 'Diagramme solaire cartésien à la latitude ' + str(latitude)
    plt.xlim(-180,180)
    plt.ylim(0, 90)
    
    plt.show()
    
    
diagramme_solaire(10)
    
    
    
    
    
    


def affichage(N,l=47,nb=100):
    if True:
        
        azimu=np.zeros(hours.shape)
        elevation=np.zeros(hours.shape)
        for i in range (nb):
            e,a = elevation_azimut(declinaison(N),angle_horaire(hours[i]),l)
            azimu[i]=a
            elevation[i]=e
        plt.figure() 
        plt.plot(azimu,elevation,".-")
        plt.axis([-180,180,0,90])
        plt.xlabel("Azimut (°)")
        plt.ylabel(" Élevation (°)")
        plt.title("Évolution de la trajectoire du soleil")
        plt.show()

    

####### Eclairement etc.... #######

def I0_etoile(N):
    import math as np

    #N est le jour de l'année
    i0_etoi=0
    #i0_etoi est flux surfacique recu par la terre depuis le soleil (hors atmosphère)
    i0_etoi=1367*(1+0.033*cosd(360/365*N))
    return(i0_etoi)

def Sh_etoile(I_etoile,elevation):
    import math as np

    #I_etoile est l'éclairement recu perpendi. au soleil
    #elevation est l'élévation
    Sh_etoi=0
    #sh_etoi est l'éclairement recu dans le plan de la surface d'étude
    Sh_etoi=I_etoile*sind(elevation)
    return(Sh_etoi)

def H0_barre(delta,w,l,I0_etoile):
    import math as np
    H0barre=(24/(3.14))*I0_etoile*(cosd(l)*cosd(delta)*sind(w) + sind(delta)*sind(l)*(3.14)/(180)*w)
    return(H0barre)


# Rapport Dh/Gh #
#Methode Lui Jordan#
def Dh_barreGh_barre_LuiJordan(Kt):
    #Kt est l'indice de clarté 
    DhGh=0
    #Dh/Gh est le rapport entre eclairement diffus et global
    DhGh=1.390-4.027*Kt+5.531*(Kt**2)-3.108*(Kt**3)
    return(DhGh)

#Methode Collares-Pereira#
def Dh_barreGh_barre_CpRabl(Kt,w):
    import math as np
    #Kt est l'indice de clarté
    #w est l'angle horaire 
    DhGh=0
    #Dh/Gh est le rapport entre eclairement diffus et global
    DhGh=0.775+0.00653*(w-90)-(0.505+0.00455*(w-90))*sind(115*Kt-103)
    return(DhGh)

#Methode Erbs#
def Dh_barreGh_barre_Erbs(Kt,w):
    #Kt est l'indice de clarté
    #w est l'angle horaire 
    DhGh=0
    #Dh/Gh est le rapport entre eclairement diffus et global
    if 0.3<=Kt<=0.8 :
        if w<=81.4:
            DhGh=1.391-3.560*Kt+4.189*(Kt**2)-2.137*(Kt**3)
            return(DhGh)
        elif w>81.4:
            DhGh=1.311-3.022*Kt+3.427*(Kt**2)-1.821*(Kt**3)
            return(DhGh)
    else :
        raise Exception("ERREUR ”Dh_barreGh_barre_Erbs” : La formule de Erbs ne fonctionne que pour Kt in [0.3;0.8]")
    
def Dhetoile(N,w,latitude,Dhbarre):
    rd=0
    delta=decli(N)
    w0 = (acosd( -tand(latitude)*tand(delta) ))*(180/3.14)
    rd=(3.14/24) * (cosd(w)-cosd(w0))/(sind(w0)-(w0*3.14/180)*cosd(w0))
    out_value=0
    out_value=(1/3600) *(rd*Dhbarre)
    return(out_value)

def Ghetoile(N,w,latitude,Ghbarre):
    r=0
    a=0
    b=0
    rd=0

    delta=decli(N)
    w0 = (acosd( -tand(latitude)*tand(delta) ))*(180/3.14)
    rd=(3.14/24) * (cosd(w)-cosd(w0))/(sind(w0)-(w0*3.14/180)*cosd(w0))
    a=0.409+0.5016*sind(w-60)
    b=0.6609+0.4767*sind(w-60)
    r=(a+b*cosd(w))*rd
    return((1/3600) *(r*Ghbarre))

def Getoile (N,H,latitude,Kt,a_surf,i_surf,rho):
    #N est le numéro du jour de l'année
    #H est l'heure de la journée
    #Latitude : explicit
    #Ghbarre global en moyenne
    #Dhbarre diffus en moyenne
    #a_surf est l'azimut de la surface du capteur
    #i_surf est l'inclinaison de la surface du capteur
    #rho est ###################################
    
    costeta=0
    #costeta est le cos de langle teta entre la normale de la surface et la driection du sole
    delta=0
    #delta est l'élévation du soleil
    omega=0
    #omega est l'angle horaire du soleil
    azi_sol=0
    #azisol est l'azimut du soleil
    Rs=0
    #Rs est le coef cos(teta)/sin(h) = Setoile/Sh etoile
    Sh_star=0
    #Sh_star est le l'éclairement global recu sur la surface
    Dh_star=0
    #
    Gh_star=0
    #
    G_star=0
    #

    delta=decli(N)
    omega=w_horaire(H)
    azi_sol=azimut(decli(N),w_horaire(H),latitude) 
    
    costeta=cosd( eleva(delta,omega,latitude) )* cosd( azi_sol - a_surf )*cosd(90-a_surf) + sind(90-i_surf)*sind( eleva(delta,omega,latitude) )

    if costeta < 0 :
        costeta=0
    else: #positif ou =0 => c'est OK
        costeta=costeta
    
    Rs=(costeta)/(sind(eleva(delta,omega,latitude)))

    rapport=Dh_barreGh_barre_Erbs(Kt,omega)

    ietoile=I0_etoile(N)
    h0=H0_barre(delta,omega,delta,ietoile)
    Ghbarre=Kt*h0
    Gh_star=Ghetoile(N,omega,latitude,Ghbarre)
    
    Dhbarre=Ghbarre*rapport
    Dh_star=Dhetoile(N,omega,latitude,Dhbarre)
    
    Sh_star=Gh_star-Dh_star

    #print(ietoile,h0,Ghbarre,Dhbarre,Dh_star,Sh_star)
    
    G_star=Rs*Sh_star+( (1+cosd(i_surf))/(2) ) * Dh_star + rho * Gh_star
    
    #print(G_star)
    
    return(G_star)