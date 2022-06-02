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
 """

from App.model import Analyzer
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de viajes

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.Analyzer()
    return analyzer

# Funciones para la carga de datos
def loadServices(analyzer: model.Analyzer, servicesfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.
    """
    servicesfile = cf.data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")

                                
    for trip in input_file:
        analyzer.loadTrip(trip)
    analyzer.order()
    return analyzer


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def StationNeedsBikes(analyzer: Analyzer):
    return model.StationNeedsBikes(analyzer)

def optionThree(analyzer, nombre, dispo_usuario, minru, maxru):
    return model.optionThree(analyzer, nombre, dispo_usuario, minru, maxru)

def optionFour(analyzer):
    return model.optionFour(analyzer)


def optionFive(analyzer, nombreO, nombreD):
    return model.shortestPath(analyzer, nombreO, nombreD)


def optionSix(analyzer, fechaI, fechaF):
    return model.optionSix(analyzer, fechaI, fechaF)


def optionSeven(analyzer, bikeID):
    return model.optionSeven(analyzer, bikeID)

def optionEight(analyzer,estacion, fyhI, fyhF):
    return model.optionEight(analyzer,estacion, fyhI, fyhF)