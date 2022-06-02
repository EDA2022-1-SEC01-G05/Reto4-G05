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


from datetime import datetime
from multiprocessing import set_forkserver_preload
import random
import time
from xmlrpc.client import Boolean

from pandas import set_eng_float_format
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

def compareGraph(id, element):
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
    __graph_loded: bool =False
    __ordered: bool =False
    grafo = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareGraph)
    #Map<id: Station>
    stations = {}
    #Map<id: Bike>
    bikes = {}
    #[{id: Trip}] ordered_by_date
    trips = []
    mst = om.newMap(omaptype='RBT',comparefunction=comparTreeMap)
    @staticmethod
    def genId():
        MAX = 1200
        sum = random.randint(0,MAX)
        id = random.randint(0,MAX)
        return hex(id)[2:]+hex(int(time.time() * 1000))[2:]+hex(sum)[2:]

    def loadTrip(self, rawTrip):
        # creates array of Trips
        trip = Trip(rawTrip["Trip Id"],rawTrip["Trip  Duration"],rawTrip["Start Time"],rawTrip["End Time"],rawTrip["Start Station Id"],rawTrip["Start Station Name"],rawTrip["End Station Id"],rawTrip["End Station Name"],rawTrip["Bike Id"],rawTrip["User Type"])
        self.trips.append({ 'key': trip.start_time, 'value': trip})

        # creates map: dict of Bikes
        if(not(trip.bike_id in self.bikes)):
            bike = Bike(trip.bike_id,1,trip.duration,trip.start_station_id,trip.end_station_id )
            self.bikes[bike.id] = bike
        else:
            bike = self.bikes[trip.bike_id]
            bike.trips += 1 
            bike.seconds += trip.duration
        # Creates Vertex (start and end)
        if(not(gr.containsVertex(self.grafo,trip.start_station_id)) and not(trip.start_station_id in self.stations)):
            start_station = Station(trip.start_station_id, trip.start_station_name)
            self.stations[start_station.id] = start_station
            gr.insertVertex(self.grafo,start_station.id)
        else:
            start_station = self.stations[trip.start_station_id]
        if(not(gr.containsVertex(self.grafo,trip.end_station_id)) and not(trip.end_station_id in self.stations)):
            end_station = Station(trip.end_station_id, trip.end_station_name)
            self.stations[end_station.id] = end_station
            gr.insertVertex(self.grafo,end_station.id)
        else:
            end_station = self.stations[trip.end_station_id]
        #Creates edges
        edge = gr.getEdge(self.grafo, start_station.id, end_station.id)
        if(edge == None ):
            #  TODO: Problema del promedio de los viajes
            gr.addEdge(self.grafo,start_station.id, end_station.id, trip.duration)
            edge = gr.getEdge(self.grafo, start_station.id, end_station.id)

        # print("["+start_station.name+"]---"+str(edge.weight)+"---["+end_station.name+"]")
    def order(self):
        def get_date(element):
            return element.get('key')
        self.trips.sort(key=get_date)
        self.__ordered = True 

 
class Trip:
    def __init__(self,id,duration,start_time,end_time,start_station_id,start_station_name,end_station_id,end_station_name,bike_id,user_type) :
        self.id = id
        self.duration = int(duration)
        self.start_time = datetime.strptime(start_time, '%m/%d/%Y %H:%M')
        self.end_time = datetime.strptime(end_time, '%m/%d/%Y %H:%M')
        self.start_station_id = start_station_id
        self.start_station_name = start_station_name
        self.end_station_id = end_station_id
        self.end_station_name = end_station_name
        self.bike_id = bike_id
        self.user_type = user_type

class Bike:
    def __init__(self,id,trips,seconds,start_station,end_station) :
        self.id = id
        self.trips = trips
        self.seconds = seconds    
        self.start_station = start_station    
        self.end_station = end_station    


class Station:
    def __init__(self,id,name) :
        self.id = id
        self.name = name

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta



# Funciones de ordenamiento