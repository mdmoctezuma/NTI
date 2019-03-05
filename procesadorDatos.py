import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go


nodosIndices = {'0002':0, '0004':1, '0005':2, '0006':3, '0008':4, '0010':5, '0014':6}

# LQI - Recibe 2 nodos para seleccionar el enlace {0002, 0004, 0005, 0006, 0008, 0010, 0010} y un archivo abierto.
# Devuelve el lqi con respecto al tiempo, máx, min, promedio y varianza.
def grafLqi(nodo1, nodo2, data):
	lqi = list()
	indx = nodosIndices[nodo1]
	indy = nodosIndices[nodo2]
	indLin = indx*7+indy  # Data es matrix x,y por línea - se obtiene índice de dato del nodo
	for line in data: # Se obtienen los datos por línea
		fields = line.split()
		lqi.append(float(fields[indLin]))
	# Gráfica
	time = np.linspace(0,len(lqi),len(lqi))
	plotly.offline.plot({
		"data": [go.Scatter(x=time, y=lqi)],
		"layout": go.Layout(
			title="Lqi de enlace de " + nodo1 + " con " + nodo2,
			xaxis=dict(title='Tiempo [5s]'),
			yaxis=dict(title='Lqi'))},
		filename='Lqi.html',
		auto_open=True, )
	max = np.max(lqi)
	min = np.min(lqi)
	mean = np.mean(lqi)
	var = np.var(lqi)
	print('Lqi de enlace de ' + nodo1 + ' con ' + nodo2)
	print('Lqi máximo es: ', max)
	print('Lqi mínimo es: ', min)
	print('Lqi promedio es: ', mean)
	print('Varianza de lqi es: ', var)

# RSSI - Recibe 2 nodos para seleccionar el enlace {0002, 0004, 0005, 0006, 0008, 0010, 0010} y un archivo abierto.
# Devuelve el rssi con respecto al tiempo, máx, min, promedio, varianza y porcentaje de desconexión.
def grafRssi(nodo1, nodo2, data):
	rssi = list()
	indx = nodosIndices[nodo1]
	indy = nodosIndices[nodo2]
	indLin = indx*7+indy # Data es matrix x,y por línea - se obtiene índice de dato del nodo
	for line in data: # Se obtienen los datos por línea
		fields = line.split()
		rssi.append(float(fields[indLin]))
	# Gráfica
	time = np.linspace(0,len(rssi),len(rssi))
	plotly.offline.plot({
		"data": [go.Scatter(x=time, y=rssi)],
		"layout": go.Layout(
			title="Rssi de enlace de " + nodo1 + " con " + nodo2,
			xaxis=dict(title='Tiempo [5s]'),
			yaxis=dict(title='Rssi [dBm]'))},
		filename='Rssi.html',
		auto_open=True,)
	max = np.max(rssi)
	min = np.min(rssi)
	mean = np.mean(rssi)
	var = np.var(rssi)
	print('RSSI de enlace de ' + nodo1 + ' con ' + nodo2)
	print('Rssi máximo es: ', max)
	print('Rssi mínimo es: ', min)
	print('Rssi promedio es: ', mean)
	print('Varianza de rssi es: ', var)

# Latencia - Recibe un nodo {0002, 0004, 0005, 0006, 0008, 0010, 0010} y un archivo abierto.
# Devuelve latencia con respecto al tiempo, máx, min, promedio, varianza y porcentaje de desconexión.
def grafLat(nodo,data):
	lat = list()
	ind = nodosIndices[nodo]
	desc = 0;
	for line in data: # Se obtienen los datos por línea
		fields = line.split()
		lat.append(float(fields[ind]))
		if fields[ind] == 0:
			desc += 1
	# Gráfica
	time = np.linspace(0,len(lat),len(lat))
	plotly.offline.plot({
		"data": [go.Scatter(x=time,y=lat)],
		"layout": go.Layout(
			title = "Latencia de nodo " + nodo,
			xaxis=dict(title='Tiempo [5s]'),
			yaxis=dict(title='Latencia [ms]'))},
		filename='Lat.html',
		auto_open = True,)

	max = np.max(lat)
	min = np.min(lat)
	mean = np.mean(lat)
	var = np.var(lat)
	print('Latencia de nodo ' + nodo)
	print('Latencia máxima es: ', max, ' ms')
	print('Latencia mínima es: ', min, ' ms')
	print('Latencia promedio es: ', mean, ' ms')
	print('Varianza de latencia es: ', var, ' ms')
	print('Porcentaje de desconexión: ', (desc/len(lat)*100), ' %')

def grafTodosRssi(data):
	rssi = []
	for i in range(9):
		rssi.append(list())
	ind = [2,3,4,6,10,12,17,18,20] # Índices lineales de nodos con enlaces - se sabe que enlaces estan a veces activos

	for line in data:  # Se obtienen los datos por línea
		for k in range(len(ind)):
			fields = line.split()
			rssi[k].append(float(fields[ind[k]]))

	print(len(rssi[0]))
	# Gráfica
	time = np.linspace(0, len(rssi[0]), len(rssi[0]))
	plt.title("RSSI")
	plt.xlabel("Tiempo [5s])")
	plt.ylabel("RSSI [dBm]")
	for m in range(len(ind)):
		plt.plot(time, rssi[m])
		plt.legend(['0002-0005', '0002-0006', '0002-0008', '0002-0014', '0004-0006', '0005-0006', '0005-0008', '0005-0014'], loc='upper right')
	plt.show()

def grafTodosLqi(data):
	lqi = []
	ind = [2, 3, 4, 6, 10, 12, 17, 18, 20] # Índices lineales de nodos con enlaces - se sabe que enlaces estan a veces activos
	for i in range(len(ind)):
		lqi.append(list())


	for line in data:  # Se obtienen los datos por línea
		for k in range(len(ind)):
			fields = line.split()
			lqi[k].append(float(fields[ind[k]]))


	# Gráfica
	time = np.linspace(0, len(lqi[0]), len(lqi[0]))
	#plt.figure(2)
	plt.title("LQI")
	plt.xlabel("Tiempo [5s])")
	plt.ylabel("LQI")
	for m in range(len(ind)):
		plt.plot(time, lqi[m])
		plt.legend(['0002-0005', '0002-0006', '0002-0008', '0002-0014', '0004-0006', '0005-0006', '0005-0008', '0005-0014'], loc='upper right')
	plt.show()

def grafTodoLat(data):
	lat = []
	 # Índices lineales de nodos con enlaces - se sabe que enlaces estan a veces activos
	for i in range(7):
		lat.append(list())

	for line in data:  # Se obtienen los datos por línea
		fields = line.split()
		for n in range(7):
			lat[n].append(fields[n])

	# Gráfica
	time = np.linspace(0, len(lat[0]), len(lat[0]))
	# plt.figure(2)
	plt.title("Latencia")
	plt.xlabel("Tiempo [5s])")
	plt.ylabel("Latencia [ms]")
	for m in range(7):
		plt.plot(time, lat[m])
		plt.legend(
			['0002', '0004', '0005', '0006', '0008', '0010', '0014'],
			loc='upper left')
	plt.show()


# Para leer el archivo de texto
try:
	frssi = open('todosRssi.txt', 'r')
	flqi = open('todosLqi.txt', 'r')
	flat = open('todosLat.txt', 'r')
# La función a continuación se escoge dependiendo del dato que se quiere {rssi, lqi, lat}

# grafRssi(nodo1, nodo2, archivo abierto) - Recibe 2 nodos para especificar un enlace y frssi
# Devuelve el rssi con respecto al tiempo, máx, min, promedio, varianza y porcentaje de desconexión.

# grafLqi(nodo1, nodo2, archivo abierto) - Recibe 2 nodos para especificar un enlace y flqi
# Devuelve el rssi con respecto al tiempo, máx, min, promedio y varianza.

# grafLat(nodo, archivo abierto) - Recibe 1 nodo y flat
# Devuelve latencia con respecto al tiempo, máx, min, promedio, varianza.

# grafTodosRssi(archivo abierto)
# Devuelve gráfica de rssi de todos los enlaces que normalmente están activos

# grafTodosLqi(archivo abierto)
# Devuelve gráfica de lqi de todos los enlaces que normalmente están activos

# grafTodosRssi(archivo abierto)
# Devuelve gráfica de latencia de todos los nodos

# Solo se puede usar una función a la vez - descomentar para usar
# Si todos los valores salen en cero, es porque no exise un enlace directo entre los 2 nodos seleccionados.

	# grafRssi('0002','0005',frssi)
	# grafLqi('0002','0005',flqi)
	# grafLat('0010', flat)
	plt.figure(1)
	grafTodosRssi(frssi)
	plt.figure(2)
	grafTodosLqi(flqi)
	plt.figure(3)
	grafTodoLat(flat)

finally:
	frssi.close()
	flqi.close()
	flat.close()


