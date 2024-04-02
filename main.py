import eclairage_solaire as ec
import numpy as np


import time
 

## VARIABLES ##
#Date de départ de la simulation:
jour=1
mois=7
annee=2024
heure=10 #format heure et heure la plus proche (10h30=>10h)

temps_simul=10 # temps de la simulation en jour
pas_temps=3600 # discrétisation chaque 'pas_temps' secondes => PAR DEFAULT = 1h

temps_simul=3600*24*temps_simul #conversion en secondes

#FLUIDE
rho=1000 #masse volumique (kg/m3)
Cp=4200 #cp (J/(kg.K))
t_froid=10 #temperature d'arrivee de l'eau froide

#Caracteristique panneau
a=0.8
b=2.5
surf=0 #en m2
t_inf=10 
debit_circul=200 #debit circulation d'un panneau (l/h/m2) 

m=debit_circul*(10**(-3))*(3600) *rho*surf #conversion en kg/s

#POSITION DU PANNEAU
lat=45 
azi_surf=0 #azumut du PANNEAU
incli_surf=90 #inclinaison du PANNEAU

#caractéristique ambiante
Kt_value=0.4 #Traduction de l'impacte de l'atmosphère
rho_value=10 #Réflectivité du sol

#CARACTERISTIQUE BALLON
T_max_in_tank=100 # en °C
Vol=300E-3 #volume du ballon (m3)
T_0=20 #température dans le ballon à i=0s
e=0.8 #rendement echangeur 
K=0.1 #constante convection
t_int=20 #temperature interieur de l'emplacment du ballon (°C)

#PUISAGE
#DEBIT DE PUISAGE sur 24h
m_puisage=np.zeros((2,24))
m_puisage[1,0]=0  #combien puisée à 0h
m_puisage[1,1]=0   #combien puisée à 1h ....
m_puisage[1,2]=0
m_puisage[1,3]=0
m_puisage[1,4]=0
m_puisage[1,5]=0
m_puisage[1,6]=1
m_puisage[1,7]=7
m_puisage[1,8]=2
m_puisage[1,9]=1
m_puisage[1,10]=0  #... combien puisée à 10h
m_puisage[1,11]=1  #combien puisée à 11h ....
m_puisage[1,12]=3
m_puisage[1,13]=1
m_puisage[1,14]=0
m_puisage[1,15]=0
m_puisage[1,16]=1
m_puisage[1,17]=0
m_puisage[1,18]=0
m_puisage[1,19]=1
m_puisage[1,20]=6
m_puisage[1,21]=5
m_puisage[1,22]=3
m_puisage[1,23]=0   #... combien puisée à 23h

#Combien d'eau puisée sur 24h:
qte_puisage_24=200E-3 #en m3/j/pers

#combien de personne ?
nbr_personne=3

#a quelle température l'eau est-elle puisée ?
temp_puisage=45 #NORME = 45°C

#placement des heures dans le tableau
for i in range(len(m_puisage[1,:])):
    m_puisage[0,i]=int(i)

#RATIONNAGE
somme=0
for i in m_puisage[1,:]:
    somme+=i
for i in range(len(m_puisage[1,:])):
    m_puisage[1,i]=m_puisage[1,i]/somme

#qte reelle
for i in range(len(m_puisage[1,:])):
    m_puisage[1,i]=m_puisage[1,i]*(qte_puisage_24*nbr_personne*rho)

#AFFICHAGE
#plt.plot(m_puisage[0,:],m_puisage[1,:])
#plt.xlabel("Temps (en h)")
#plt.ylabel("Puisage (en kg)")
#plt.title("Puisage en fonction du temps (sur 24h)")
#plt.show()
#xinput("")

## MAIN CODE ##
temperature=np.zeros(int(temps_simul/pas_temps)+1)

#INITIALISATION
temperature[0]=T_0 
flux_s=np.zeros(int(temps_simul/pas_temps))
tmax=0
tmin=0
eta=0
Getoile=np.zeros(int(temps_simul/pas_temps))
flux_p=np.zeros(int(temps_simul/pas_temps))
flux_c=np.zeros(int(temps_simul/pas_temps))
m_adv=0
puissance=np.zeros(int(temps_simul/pas_temps))
temps=np.zeros(int(temps_simul/pas_temps))
temps_s=np.zeros(int(temps_simul/pas_temps))
temps_h=np.zeros(int(temps_simul/pas_temps))
temps_j=np.zeros(int(temps_simul/pas_temps))
temps_m=np.zeros(int(temps_simul/pas_temps))
temps_a=np.zeros(int(temps_simul/pas_temps))
heure=int(heure) #au cas ou l'utilisateur a mal rentré les données 
t1=time.time()
for i in range(0,int(temps_simul/pas_temps)):
    #input("")
    print("Calcul en cours.")
    t=i*pas_temps
    temps[i]=t
    temps_h[i]=(heure+(temps[i]/3600))%24

    if temps_h[i]==0:#NOUVEAU JOUR
        jour+=1
    if jour == 32: #SUPPOSONS tous les mois sont de 31j
        mois+=1
        jour=1
    if mois == 13:
        mois=1
        annee+=1

    temps_j[i]=jour
    temps_m[i]=mois
    temps_a[i]=annee

    #FLUX S
    #print("")
    #print("jour",ec.n_jour(jour,mois))
    #print("heure",temps_h[i])

    Getoile[i]=ec.Getoile(N=ec.n_jour(jour,mois),
               H=temps_h[i],
               latitude=lat,
               Kt=Kt_value,
               a_surf=azi_surf,
               i_surf=incli_surf,
               rho=rho_value)
    tmax=(a*surf*Getoile[i] - b*surf* ( (e*temperature[i]-2*t_inf)/(2) ) + e*m*Cp) / (e*m*Cp + b*surf* ( (2-e)/(2) ) )
    tmin=e*(tmax-temperature[i])

    if surf == 0 : #si surface du capteur =0 => aucune captation possible
        Getoile[i] = 0
    
    if Getoile[i] == 0: #si aucun soleil sur le capteur
        eta=0 #alors aucun rendement possible
    else :#sinon
        eta=a-b*( ( ((tmin+tmax)/(2)) - t_inf )/(Getoile[i]) ) #rendement possible car soleil
    
    if temperature[i]>= T_max_in_tank : #si la température dans le ballon est plus grande que la temp. max demandé par l'utilisateur
        flux_s[i]=0 #alors on considère aucun nouvel apport du soleil
    else : #sinon, le flux est calculé
        flux_s[i]=eta*Getoile[i]*surf
    
    #FLUX P
    flux_p[i]=K*(temperature[i]-t_int)
    
    #input("")
    print("Calcul en cours..")

    #FLUX C
    if temperature[i]<=temp_puisage:
        m_adv=m_puisage[1,int(t/3600)%24]/3600
        puissance[i]=m_puisage[1,int(t/3600)%24]/3600*Cp*(temp_puisage-temperature[i])
    else :
        m_adv=(m_puisage[1,int(t/3600)%24]/3600)*((temp_puisage-t_froid)/(temperature[i]-t_froid))
        puissance[i]=0

    flux_c[i]=m_adv*Cp*(temperature[i]-t_froid)
    

    print("Calcul en cours...")
    #input("")
    
    temperature[i+1]=temperature[i]+ ( (pas_temps)/(rho*Cp*Vol) ) * (flux_s[i]-flux_p[i]-flux_c[i])

t2=time.time()

#ecriture dans excel
import xlsxwriter

workbook = xlsxwriter.Workbook('datas.xlsx')
 
worksheet = workbook.add_worksheet()

worksheet.write(0,0, 'Temps de simulation (s)')
worksheet.write(0,1, 'Temps (h)')
worksheet.write(0,2, 'Jour')
worksheet.write(0,3, 'Mois')
worksheet.write(0,4, 'Année')

worksheet.write(0,6, 'Flux Solaire (W)')
worksheet.write(0,7, 'Flux Convectif (W)')
worksheet.write(0,8, 'Flux Advectif (W)')
worksheet.write(0,9, 'Temperature (°C)')
worksheet.write(0,10, 'Puissance supplémentaire (W)')

worksheet.write(0,12, 'Temps de simultaion :')
worksheet.write(0,13, t2-t1)
worksheet.write(0,14, 'secondes')
for i in range(1,len(flux_s)):
    worksheet.write(i,0, temps[i-1])
    worksheet.write(i,1, temps_h[i-1])
    worksheet.write(i,2, temps_j[i-1])
    worksheet.write(i,3, temps_m[i-1])
    worksheet.write(i,4, temps_a[i-1])

    worksheet.write(i,6, flux_s[i-1])
    worksheet.write(i,7, flux_p[i-1])
    worksheet.write(i,8, flux_c[i-1])
    worksheet.write(i,9, temperature[i-1])
    worksheet.write(i,10, puissance[i-1])

workbook.close()


print("Temps de calcul :",t2-t1,'secondes')
