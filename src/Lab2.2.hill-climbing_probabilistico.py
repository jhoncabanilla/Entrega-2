import numpy as np
from numpy import product, random
from pandas.core.indexing import convert_to_index_sliceable
from pandas.core.frame import DataFrame
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import math
import time
import sys

sys.setrecursionlimit(6000)

#Practica 2.2

"Funcion que devuelve el valor de la funcion en el punto (x,y) para cada i,j"
def valorMatriz(x,y):
    return y + math.sin(math.pi * math.sqrt(x*x + y*y))

"SIEMPRE DEVUELVE EL MAX.GLOBAL"
def f1(x,y): 
    return math.sin(x) + math.cos(y) + math.sin(x) * math.cos(y) + math.sin(x*2)

"DEPENDE DE LA POSICION INICIAL ESCOGIDA AL AZAR"
def f2(x,y):
    return 2 * math.sin(x) * math.cos(y/2) + x +  math.log(abs(y-math.pi/2))

"DEPENDE DE LA POSICION INICIAL ESCOGIDA AL AZAR"
def f3(x,y):
    return math.sin(x) * math.cos(y) + abs(math.sqrt(x*y))

"DEPENDE DE LA POSICION INICIAL ESCOGIDA AL AZAR"
def f4(x,y):
    return math.sin(x*7) + math.cos( (y+math.pi/4)*4 ) + (x+y)


"Funcion que nos crea la matriz"
def creaMatriz(n,m):
    matrix = np.zeros((n,m)) #Inicializamos el array con todo 0
    #Procedemos a calcular las X e Y correspondientes, y a partir de ellas obtener el valor adecuado de la funcion
    for i in range(n): #[0:pi]
        x = i * math.pi / (n-1)
        for j in range(m):
            #y = 0 + j * math.pi / (m-1)
            y = math.pi + j * (0 - math.pi) / (m-1)
            #matrix[j][i] = valorMatriz(x,y)
            matrix[j][i] = f1(x,y)
            #matrix[j][i] = f2(x,y)
            #matrix[j][i] = f3(x,y)
            #matrix[j][i] = f4(x,y)
    return matrix

"Funcion que calcula y devuelve los puntos colindantes de una matriz"
def getColindantes(matriz,x,y,n,m):
    dic = {}
    ite = 0
    x_or = x
    x -= 1

    while(ite<2):
        if(0<=x<n):
            dic[matriz[x][y]] = [x,y]
        x += 2
        ite += 1

    y -= 1
    ite = 0
    while(ite<2):
        if(0<=y<m):
            dic[matriz[x_or][y]] = [x_or,y]
        y += 2
        ite += 1

    return dic


def hillClimbing(matriz,punto,n,m,x,y,lista_puntosX,lista_puntosY):
    #Obtemos los puntos colindantes del valor
    continuar = False
    colindantes = getColindantes(matriz,x,y,n,m)

    #Recorremos los valores del diccionario para saber si hay un colindante mayor que el punto
    for item in colindantes.keys():
        if punto < item:
            punto = item
            continuar = True

    #Significa que hemos encontrado un colindante mayor que el valor, por lo cual continuamos
    if continuar:
        #Añadimos las coordenadas del colindante
        lista_puntosX.append(colindantes.get(punto)[0]) #Coordenada x
        lista_puntosY.append(colindantes.get(punto)[1]) #Coordenada y
        punto_X = lista_puntosX[len(lista_puntosX)-1]
        punto_Y = lista_puntosY[len(lista_puntosY)-1]
        hillClimbing(matriz,punto,n,m,punto_X,punto_Y,lista_puntosX,lista_puntosY)

    max_global = np.max(matriz)

    return lista_puntosX, lista_puntosY, punto, max_global

def main():
    #Comenzamos creando la matriz
    n = 100
    m = 100
    matriz = creaMatriz(n,m)

    "Implementacion metodo Monte-Carlo"
    p = 10
    np.random.seed(0)
    while p>0:
        x = random.randint(n)
        y = random.randint(m)
        puntoComienzo = matriz[x][y]
        trayectoria_Y, trayectoria_X, max, maximo_global= hillClimbing(matriz,puntoComienzo,n,m,x,y,[],[])
        p -= 1

        "Dibujo del HeapMap"
        sb.heatmap(matriz,cmap='hot',cbar=False)
        #Punto de origen
        primerPunto_X = trayectoria_X[0]
        primerPunto_Y = trayectoria_Y[0]
        primerPunto = {"col1":[primerPunto_X,primerPunto_X+0.0001], "col2":[primerPunto_Y,primerPunto_Y+0.0001]}
        df1 = DataFrame(data=primerPunto)
        sb.lineplot(x="col1",y="col2",data=df1,color='green',linewidth=8)

        #Punto final --> Maximo
        ultimoPunto_X = trayectoria_X[len(trayectoria_X)-1]
        ultimoPunto_Y = trayectoria_Y[len(trayectoria_Y)-1]
        ultimoPunto = {"col1":[ultimoPunto_X+0.0001,ultimoPunto_X], "col2":[ultimoPunto_Y+0.0001,ultimoPunto_Y]}
        df2 = DataFrame(data=ultimoPunto)

        if max == maximo_global:
            sb.lineplot(x="col1",y="col2",data=df2,color='yellow',linewidth=8)
        else:
            sb.lineplot(x="col1",y="col2",data=df2,color='blue',linewidth=8)

        #Recta que une ambos puntos
        sb.lineplot(x=trayectoria_X,y=trayectoria_Y,color='black',linewidth=4,markersize=12,
        estimator=None,palette='hls')

       
    #Nombre de los ejes
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.show()


if __name__ == "__main__":
    main()