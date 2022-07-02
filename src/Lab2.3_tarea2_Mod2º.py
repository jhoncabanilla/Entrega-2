import numpy as np
from numpy import PINF, product, random, rint
from pandas.core.indexing import convert_to_index_sliceable
from pandas.core.frame import DataFrame
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import math
import time
import sys

sys.setrecursionlimit(6000)

#Practica 2.3 
"********TAREA 2 --> 1º Modificacion: eliminar el calculo inicial de los valores de la matriz **********"

"Funcion que devuelve el valor de la funcion en el punto (x,y) para cada i,j"
def valorMatriz(x,y):
    return 2*(-math.sqrt(x*x+y*y)+(math.cos(y)+math.sin(x))*math.sin(y+x)) + 15*(math.sqrt((x+1)*(x+1)+y*y)-1)/((math.sqrt((x+1)*(x+1)+y*y)-1)*(math.sqrt(x*x+y*y)-1)+1)

"Funcion que calcula y devuelve los puntos colindantes de una matriz"
def getColindantes(matriz,x,y,n,m):
    dic = {}
    ite = 0
    x_or = x
    x -= 1

    while(ite<2):
        if(0<=x<n):
            valor1 = valorMatriz(-4 + y * 12 / (n-1), 8 + x * -12  / (m-1))
            matriz[x][y] = valor1
            dic[valor1] = [x,y]
        x += 2
        ite += 1

    y -= 1
    ite = 0
    while(ite<2):
        if(0<=y<m):
            valor2 = valorMatriz(-4 + y * 12 / (n-1), 8 + x_or * -12  / (m-1))
            matriz[x_or][y] = valor2
            dic[valor2] = [x_or,y]
        y += 2
        ite += 1

    return dic


def hillClimbing(matriz,punto,n,m,x,y,lista_puntosX,lista_puntosY,explorado):
    #Obtemos los puntos colindantes del valor
    continuar = False
    colindantes = getColindantes(matriz,x,y,n,m)

    #Recorremos los valores del diccionario para saber si hay un colindante mayor que el punto
    for item in colindantes.keys():
        if punto < item:
            punto = item
            continuar = True

    #Comprobamos si se encuentra en un camino explorado
    if colindantes.get(punto) != None or colindantes.get(punto) != None:
        new_x = colindantes.get(punto)[0]
        new_y = colindantes.get(punto)[1]

        if [new_x,new_y] in explorado:
            continuar = False #Detenemos esa busqueda

    #Significa que hemos encontrado un colindante mayor que el valor, por lo cual continuamos
    if continuar:
        #Añadimos las coordenadas del colindante
        lista_puntosX.append(colindantes.get(punto)[0]) #Coordenada x
        lista_puntosY.append(colindantes.get(punto)[1]) #Coordenada y
        punto_X = lista_puntosX[len(lista_puntosX)-1]
        punto_Y = lista_puntosY[len(lista_puntosY)-1]
        #Añadimos el punto al camino explorado
        explorado.append([punto_X, punto_Y])

        hillClimbing(matriz,punto,n,m,punto_X,punto_Y,lista_puntosX,lista_puntosY,explorado)

    #maximo_global = np.max(matriz)

    return lista_puntosX, lista_puntosY, punto, explorado

def busquedaMonteCarlo(matriz,n,m, valor_max):
    "Implementacion metodo Monte-Carlo"
    explorado = []
    equis = []
    ye = []
    #Escogemos el numero de paracaidistas que tienen un punto de partida aleatorio
    paracaidistas = 150
    encontrado = False
    np.random.seed(0) #Semilla para poder reproducir los experimentos
    while paracaidistas > 0 and encontrado == False:
        x = random.randint(n)
        y = random.randint(m)

        #Comprobar si el camino esta explorado
        if [x,y] in explorado: #Pasamos a la siguiente busqueda
            pass
        else:
            #Guardamos las coordenadas del camino que estamos explorando
            explorado.append([x,y])
            valor = valorMatriz(-4 + y * 12 / (n-1), 8 + x * -12  / (m-1))
            matriz[x][y] = valor
            puntoComienzo = valor #Multiples puntos de inicio escogidos al azar
            equis, ye, max_p, explorado = hillClimbing(matriz,puntoComienzo,n,m,x,y,[],[],explorado)
            #Comprobamos si con el paracaidista ha encontrado el maximo global
            if max_p == valor_max:
                encontrado = True

        paracaidistas -= 1
    return equis, ye

def main():
    #Comenzamos creando la matriz
    n = 1000
    m = 1000
    #Tengo que rellenar la matriz con el valor maximo que duvuelve la funcion
    valor_max = abs(valorMatriz(-4 + (m-1) * 12 / (n-1), 8 + (n-1) * -12  / (m-1)))
    #matrix = np.zeros((n,m)) #Creo una matriz llena de 0`s
    matrix = np.full((n,m), 111)
    t1 = time.time()
    valoresX, valoresY = busquedaMonteCarlo(matrix,n,m, valor_max)
    t2 = time.time()
    print("Busqueda Monte-Carlo con la modificacion de eliminar los valores iniciales:", t2-t1)
    print(valoresX)
    print()
    print(valoresY)

if __name__ == "__main__":
    main()