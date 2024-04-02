#Grille :
minor_xticks = np.arange(-maxAz, maxAz, 10)#espaces de la grille
minor_yticks = np.arange(0, int(hauteurmax+7), 1)#espaces de la grille
ax.set_xticks(minor_xticks, minor=True)
ax.set_yticks(minor_yticks, minor=True)
ax.grid(which='minor', alpha=0.2)
plt.grid()















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

