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
from msilib.schema import Component
import random
import time

from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
import config as cf
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
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
    components = None

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
            start_station = Station(trip.start_station_id, trip.start_station_name, 0,1)
            self.stations[start_station.id] = start_station
            gr.insertVertex(self.grafo,start_station.id)
        else:
            start_station = self.stations[trip.start_station_id]
            start_station.OutTrips += 1 
        if(not(gr.containsVertex(self.grafo,trip.end_station_id)) and not(trip.end_station_id in self.stations)):
            end_station = Station(trip.end_station_id, trip.end_station_name, 1,0)
            self.stations[end_station.id] = end_station
            gr.insertVertex(self.grafo,end_station.id)
        else:
            end_station = self.stations[trip.end_station_id]
            end_station.InTrips += 1 
        #Creates edges
        edge = gr.getEdge(self.grafo, start_station.id, end_station.id)
        if(edge == None ):
            #  TODO: Problema del promedio de los viajes
            gr.addEdge(self.grafo,start_station.id, end_station.id, trip.duration)
            edge = gr.getEdge(self.grafo, start_station.id, end_station.id)

        # print("["+start_station.name+"]---"+str(edge)+"---["+end_station.name+"]")
    def order(self):
        def get_date(element):
            return element['key']
        self.trips.sort(key=get_date)
        self.__ordered = True 

 
class Trip:
    def __init__(self,id,duration: str,start_time: str,end_time: str,start_station_id: str,start_station_name: str,end_station_id: str,end_station_name: str,bike_id: str,user_type: str) :
        self.id = id
        self.duration = int(duration)
        self.start_time = datetime.strptime(start_time, '%m/%d/%Y %H:%M')
        self.end_time = datetime.strptime(end_time, '%m/%d/%Y %H:%M')
        self.start_station_id = str(int(float(start_station_id))) if start_station_id else ''
        self.start_station_name = start_station_name
        self.end_station_id = str(int(float(end_station_id))) if end_station_id else ''
        self.end_station_name = end_station_name
        self.bike_id = bike_id
        self.user_type = user_type

class Bike:
    def __init__(self,id: str,trips: int,seconds: float,start_station: str,end_station: str) :
        self.id = id
        self.trips = trips
        self.seconds = seconds    
        self.start_station = start_station    
        self.end_station = end_station    


class Station:
    def __init__(self,id: str,name: str, InTrips: int, OutTrips: int) :
        self.id = id
        self.name = name
        self.InTrips = InTrips
        self.OutTrips = OutTrips

# Funciones para creacion de datos

# Funciones de consulta

def StationNeedsBikes(analyzer: Analyzer):
    st = analyzer.stations
    mostWantedKey = [0,0,0,0,0]
    mostWantedValue = [0,0,0,0,0]
    def putWanted(element):
        for i,x in enumerate(mostWantedKey):
            if(element.OutTrips > x):
                for v in reversed(range(i,len(mostWantedKey))):
                    mostWantedKey[v] = mostWantedKey[v-1]
                    mostWantedValue[v] = mostWantedValue[v-1]
                mostWantedKey[i] = element.OutTrips
                mostWantedValue[i] = element
                break

    for id in st:
        putWanted(st[id])
    return mostWantedValue

#mas visitada en un periso
def superStation(analyzer: Analyzer,station_id, fyhI, fyhF):
    tp = Analyzer.trips 
    pass

def optionSix(analyzer: Analyzer, fechaI, fechaF):
    inicio = datetime.strptime(fechaI, '%m/%d/%Y')
    final = datetime.strptime(fechaF, '%m/%d/%Y')
    if inicio > final : inicio, final = final,inicio
    start = end = None
    origin = destiny = 'None'
    duration = 0
    hourIn = hourOut = {'hour': None, 'value': 0 }
    OutStations = InStations = { 'None': 0}
    hoursIn = {0: 0,1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0,10: 0,11: 0,12: 0,13: 0,14: 0,15: 0,16: 0,17: 0,18: 0,19: 0,20: 0,21: 0,22: 0,23: 0}
    hoursOut = {0: 0,1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0,10: 0,11: 0,12: 0,13: 0,14: 0,15: 0,16: 0,17: 0,18: 0,19: 0,20: 0,21: 0,22: 0,23: 0}
    t : Trip
    for i,r in enumerate(analyzer.trips):
        t = r['value']
        if (t.start_time > inicio and start == None):
            start = i
        if  (t.end_time > final and end == None):
            end = i-1 if i >= 0 else 0
        if (start != None and end != None):
            break
    for i in range(start,end+1):
        t = analyzer.trips[i]['value']
        duration += t.duration
        if not( t.start_station_name in OutStations.keys()):
            OutStations[t.start_station_name] = 1
        else:
            OutStations[t.start_station_name] += 1
        if not( t.end_station_name in InStations.keys()):
            InStations[t.end_station_name] = 1
        else:
            InStations[t.end_station_name] += 1
        hoursIn[t.end_time.hour] += 1
        hoursOut[t.start_time.hour] += 1
    for i in range(0,24):
        hourIn = {'hour': i, 'value': hoursIn[i]  } if  hourIn['value'] < hoursIn[i]  else hourIn
        hourOut = {'hour': i, 'value': hoursOut[i]  } if  hourOut['value'] < hoursOut[i]  else hourOut
    for i in InStations.keys():
        origin = i if  InStations[i] > InStations[origin]  else origin
    for i in OutStations.keys():
        destiny = i if  OutStations[i] > OutStations[destiny]  else destiny
    return {'total': end-start,'duration': duration, 'OutStation': origin, 'InStation': destiny, 'hourIn': hourIn['hour'], 'hourOut': hourOut['hour']  }

def connectedComponents(analyzer: Analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer.components = scc.KosarajuSCC(analyzer.grafo)
    return scc.connectedComponents(analyzer.components), analyzer.components

def shortestPath(analyzer:Analyzer , origin_station_name, destination_station_name):
    start_station, end_station = None, None
    for i in analyzer.stations.values():
        if i.name ==  origin_station_name:
            start_station = i
        if i.name == destination_station_name:
            end_station = i
    if(start_station == None or end_station == None):
        return None
    djkgraph = djk.Dijkstra(analyzer.grafo,start_station.id)
    path = djk.pathTo(djkgraph,end_station.id)
    return path


# Funciones de ordenamiento