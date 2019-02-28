#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import json
import time
import numpy as np
import math

it = 75 #Número de muestras a tomar
nodosIndices = {"0002":0, "0004":1, "0005":2, "0006":3, "0008":4, "0010":5, "0014":6} #Indices para nodos
for m in range(it):
    print("Inicié muestra " + str(m))
    #Crea matrices en donde guardar los datos
    rssi = np.zeros((len(nodosIndices), len(nodosIndices)))
    rssiMax = -1*math.inf*np.ones((len(nodosIndices), len(nodosIndices)))
    rssiMin = math.inf*np.ones((len(nodosIndices), len(nodosIndices)))
    rssiVar = np.zeros((len(nodosIndices), len(nodosIndices)))
    lqi = np.zeros((len(nodosIndices), len(nodosIndices)))
    lqiMin = math.inf*np.ones((len(nodosIndices), len(nodosIndices)))
    lqiMax = -1*math.inf*np.ones((len(nodosIndices), len(nodosIndices)))
    lqiVar = np.zeros((len(nodosIndices), len(nodosIndices)))
    lat = [0.0]* len(nodosIndices)
    latMin = [math.inf]* len(nodosIndices)
    latMax = [-1*math.inf]* len(nodosIndices)
    latVar = [-1*math.inf]* len(nodosIndices)
    desconexiones = [-1*math.inf]* len(nodosIndices)
    t1 = 0
    t2 = 0

    HOST, PORT = "148.205.37.122", 6000

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        for i in nodosIndices:
            wsnQuery = '{"id": "neighbours", "mac":"' + i + '"}'
            # Connect to server and send data
            t1 = time.clock()
            sock.sendall(wsnQuery.encode())
            # Receive data from the server and shut down
            received = sock.recv(1024)
            t2 = time.clock()
            lat[nodosIndices[i]] = (t2 - t1) * 1000  # ms
            lat[nodosIndices[i]] = round(lat[nodosIndices[i]], 4)
            if latMax[nodosIndices[i]] < lat[nodosIndices[i]]:
                latMax[nodosIndices[i]] = lat[nodosIndices[i]]
            if latMin[nodosIndices[i]] > lat[nodosIndices[i]]:
                latMin[nodosIndices[i]] = lat[nodosIndices[i]]
            while (received is None):
                t1 = time.clock()
                sock.sendall(wsnQuery.encode())
                # Receive data from the server and shut down
                received = sock.recv(1024)
                t2 = time.clock()
                lat[nodosIndices[i]] = (t2 - t1) * 1000  # ms
                lat[nodosIndices[i]] = round(lat[nodosIndices[i]], 4)
                if latMax[nodosIndices[i]] < lat[nodosIndices[i]]:
                    latMax[nodosIndices[i]] = lat[nodosIndices[i]]
                if latMin[nodosIndices[i]] > lat[nodosIndices[i]]:
                    latMin[nodosIndices[i]] = lat[nodosIndices[i]]
                time.sleep(15)
            jrec = json.loads(received)

            # print(i, jrec)
            while (jrec is None):
                t1 = time.clock()
                sock.sendall(wsnQuery.encode())
                # Receive data from the server and shut down
                received = sock.recv(1024)
                t2 = time.clock()
                lat[nodosIndices[i]] = (t2 - t1) * 1000  # ms
                lat[nodosIndices[i]] = round(lat[nodosIndices[i]], 4)
                if latMax[nodosIndices[i]] < lat[nodosIndices[i]]:
                    latMax[nodosIndices[i]] = lat[nodosIndices[i]]
                if latMin[nodosIndices[i]] > lat[nodosIndices[i]]:
                    latMin[nodosIndices[i]] = lat[nodosIndices[i]]

                time.sleep(15)
                jrec = json.loads(received)

            if(len(jrec) !=1 and "error" not in str(jrec[0])): #Nodo apagado
                for j in jrec:

                    if j['mac'] in nodosIndices:
                       # print(j)
                        rssi[nodosIndices[i],nodosIndices[j['mac']]] = j['rssi']
                        lqi[nodosIndices[i], nodosIndices[j['mac']]] = j['lqi']
                        if rssi[nodosIndices[i],nodosIndices[j['mac']]] > rssiMax[nodosIndices[i],nodosIndices[j['mac']]]:
                            rssiMax[nodosIndices[i], nodosIndices[j['mac']]] = rssi[nodosIndices[i],nodosIndices[j['mac']]]
                        if lqi[nodosIndices[i], nodosIndices[j['mac']]] > lqiMax[nodosIndices[i], nodosIndices[j['mac']]]:
                            lqiMax[nodosIndices[i], nodosIndices[j['mac']]] = lqi[nodosIndices[i], nodosIndices[j['mac']]]
                        if rssi[nodosIndices[i],nodosIndices[j['mac']]] < rssiMin[nodosIndices[i],nodosIndices[j['mac']]]:
                            rssiMin[nodosIndices[i], nodosIndices[j['mac']]] = rssi[nodosIndices[i],nodosIndices[j['mac']]]
                        if lqi[nodosIndices[i], nodosIndices[j['mac']]] < lqiMin[nodosIndices[i], nodosIndices[j['mac']]]:
                            lqiMin[nodosIndices[i], nodosIndices[j['mac']]] = lqi[nodosIndices[i], nodosIndices[j['mac']]]
            else:
                desconexiones[nodosIndices[i]] += 1
        # Se pasan los datos a txt para guardarlos
        with open('rssi.txt', 'a+') as f:
            for line in rssi:
                np.savetxt(f, line, fmt='%d', newline="  ")
            f.write("\n")
        with open('lqi.txt', 'a+') as g:
            for line in lqi:
                np.savetxt(g, line, fmt='%d', newline="  ")
            g.write( "\n")
        with open('latencia.txt', 'a+') as h:
            for item in lat:
                h.write("%s " % item)
            h.write("\n")
        print("Terminé muestra " + str(m))
        # Espera hasta el tiempo de la siguiente muestra
        time.sleep(300) #600=10 min
    finally:
        sock.close()

