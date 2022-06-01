"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import random
import time
import config as cf
import math
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""



# Funciones utilizadas para comparar elementos dentro de una estructura de datos

def compareHashMap(id, element):
    key = me.getKey(element)
    if (id == key):
        return 0
    elif (id > key):
        return 1
    else:
        return -1
def compareList(a1, a2):
    """
    Compara dos crimenes
    """
    if (a1 == a2):
        return 0
    elif a1 > a2:
        return 1
    else:
        return -1
def comparTreeMap(a1, a2):
    """
    Compara dos crimenes
    """
    if (a1 == a2):
        return 0
    elif a1 > a2:
        return 1
    else:
        return -1
def compareMapNumber(a1, a2):
    """
    Compara dos crimenes
    """
    a1 = a1 if a1 != '' else 0
    a2 = a2 if a2 != '' else 0
    if (a1 == a2):
        return 0
    elif float(a1) > float(a2):
        return 1
    else:
        return -1

# Construccion de modelos


class Analyzer():
    grafo = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareList)
    bikes = mp.newMap(numelements=14000,
                                    maptype='PROBING',
                                    comparefunction=compareHashMap)
    trips = om.newMap(omaptype='RBT',
                                    comparefunction=comparTreeMap)
    mst = om.newMap(omaptype='RBT',
                                    comparefunction=comparTreeMap)
    def genId():
        MAX = 1200
        sum = random.randint(0,MAX)
        id = random.randint(0,MAX)
        return hex(id)[2:]+hex(int(time.time() * 1000))[2:]+hex(sum)[2:]

    def loadTrip(rawTrip):
        trip = Trip(rawTrip["Trip Id"],rawTrip["Trip  Duration"],rawTrip["Start Time"],rawTrip["End Time"],rawTrip["Start Station Id"],rawTrip["Start Station Name"],rawTrip["End Station Id"],rawTrip["End Station Name"],rawTrip["Bike Id"],rawTrip["User Type"])
        bike = Bike(trip.bike_id,0,trip.start_station_id,trip.end_station_id )
        pass


class Trip:
    def _init_(self,id,duration,start_time,end_time,start_station_id,start_Station_name,end_station_id,end_station_name,bike_id,user_type) :
        self.id = id
        self.duration = duration
        self.start_time = start_time
        self.end_time = end_time
        self.start_station_id = start_station_id
        self.start_Station_name = start_Station_name
        self.end_station_id = end_station_id
        self.end_station_name = end_station_name
        self.bike_id = bike_id
        self.user_type = user_type

class Bike:
    def _init_(self,id,trips,hours,start_station,end_station) :
        self.id = id
        self.trips = trips
        self.hours = hours    
        self.start_station = start_station    
        self.end_station = end_station    

class Routes:
    def _init_(self,id,time) :
        self.id = id
        self.time = time

class Station:
    def _init_(self,id,name) :
        self.id = id
        self.name = name

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta



# Funciones de ordenamiento