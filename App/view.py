"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from ast import Pass
from itertools import count
from re import A
import sys
from typing import final
import config
import threading
from App import controller
from DISClib.ADT import stack
assert config


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


servicefile = 'Bikeshare-ridership-2021-utf8-small.csv'
initialStation = None
searchMethod = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2-REQ 1: Comprar bicicletas para las estaciones con más viajes")
    print("3-REQ 2: Planear paseos turísticos por la ciudad")
    print("4-REQ 3: Reconocer los comopnentes fuertemente conectados del sistema")
    print("5-REQ 4: Planear una ruta rápida")
    print("6-REQ 5: Reportar rutas en un rango de fechas para los usuarios anuales")
    print("7-REQ 6: Planear el mantenimiento preventivo de bicicletas")
    print("8-REQ 7: La estación más frecuentada por visitantes")
    print("0- Salir")
    print("*******************************************")


def optionTwo(cont):
    lst = controller.StationNeedsBikes(cont)
    for e in lst:
        print('[',e.id, e.name, e.InTrips,']')

def optionThree(cont, nombre, dispo_usuario, minru, maxru):
    pass

def optionFour(cont):
    number, components = controller.connectedComponents(cont)
    print('El número de componentes conectados es: ' + str(number))
    return components


def optionFive(cont, nombreO, nombreD):
    path = controller.optionFive(cont, nombreO, nombreD)
    if path is not None:
        pathlen = stack.size(path)
        print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print(stop)
    else:
        print('No hay camino')


def optionSix(analyzer, fechaI, fechaF):
    return controller.optionSix(analyzer, fechaI, fechaF)


def optionSeven(cont, bikeID):

    pass

def optionEight(cont,estacion, fyhI, fyhF):
    pass


"""
Menu principal
"""


def thread_cycle():
    cont = None
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')
        if int(inputs) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            cont = controller.init()
            controller.loadServices(cont, servicefile)
        elif int(inputs) == 2:
            optionTwo(cont)

        elif int(inputs) == 3:

            optionThree(cont)

        elif int(inputs) == 4:
            optionFour(cont)

        elif int(inputs) == 5:
            orgStation = input("Estación origen (Ej: Fort York  Blvd / Capreol Ct): ")
            destStation = input("Estación destino (Ej: Yonge St / St Clair Ave): ")
            optionFive(cont, orgStation, destStation)
            
        elif int(inputs) == 6:
            inicio = input("Fecha de inicio (Ej: 02/24/2021): ")
            final = input("Fecha de final (Ej: 07/09/2021): ")
            print(optionSix(cont, inicio,final))

        elif int(inputs) == 7:
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionSeven(cont, destStation)

        elif int(inputs) == 8:
            destStation = input("Estación destino (Ej: 15151-10): ")
            destStation = input("Estación destino (Ej: 15151-10): ")
            destStation = input("Estación destino (Ej: 15151-10): ")
            destStation = input("Estación destino (Ej: 15151-10): ")

            optionEight(cont)
        else:
            break
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()