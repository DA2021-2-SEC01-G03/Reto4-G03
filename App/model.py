﻿
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       ANALYZER
# -----------------------------------------------------


def newAnalyzer():
    """
    Inicializa el analizador
    """
    try:
        analyzer = {
                    'cities': None,
                    'airports': None,
                    'Directed airports': None,
                    'No Directed airports': None
                    }
       
        analyzer['cities'] = m.newMap(numelements=80000,
                                     maptype='PROBING')

        analyzer['airports'] = m.newMap(numelements=20000,
                                     maptype='PROBING')



        analyzer['Directed airports'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=180000,
                                              comparefunction=compareAirports)

        analyzer['No Directed airports'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareAirports)
        return analyzer

    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al analyzer

def addCity(analyzer, city):
    m.put(analyzer['cities'], city['city'], city)


def addAirport(analyzer, airport):
    airports = analyzer['airports']
    iso = airport['IATA']
    m.put(airports, iso, airport['IATA'])


def addAirportsConnection(analyzer, departure, destination, distance):
    airports = analyzer['Directed airports']
    noDirectedAirports = analyzer['No Directed airports']
    if gr.containsVertex(airports, departure) == False:
        gr.insertVertex(airports, departure)
    if gr.containsVertex(airports, destination) == False:
        gr.insertVertex(airports, destination)   
    if gr.getEdge(airports, destination, departure) != None:
        gr.insertVertex(noDirectedAirports, departure)
        gr.insertVertex(noDirectedAirports, destination)
        gr.addEdge(noDirectedAirports, departure, destination, distance)
                
    gr.addEdge(airports, departure, destination, distance)


# ==============================
# Funciones de consulta
# ==============================


def mostConnectedAirports(analyzer):
    airportsGraph = analyzer['Directed airports']
    airportsList = gr.vertices(airportsGraph)
    finalList = lt.newList('ARRAY_LIST')
    TotalAirports = gr.numVertices(airportsGraph)
    for airport in lt.iterator(airportsList):
        numDestinations = gr.outdegree(airportsGraph, airport)
        numDestinations2 = gr.indegree(airportsGraph, airport)
        airportNumDestinations = {'airport': airport, 'numConnections': numDestinations + numDestinations2, 'outBound': numDestinations, 'inBound': numDestinations2}
        lt.addLast(finalList, airportNumDestinations)

    return finalList, TotalAirports

def cantidadClusteres(iata1, iata2, analyzer):
    scc1= scc.KosarajuSCC(analyzer['Directed airports'])
    clusteresTotales = scc.connectedComponents(scc1)
    confirmIatas = scc.stronglyConnected(scc1, iata1, iata2)
    
    return clusteresTotales, confirmIatas
#

def minimumCostPaths(analyzer, initialStation):

    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def servedRoutes(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stops'])
    maxvert = None
    maxdeg = 0
    for vert in lt.iterator(lstvert):
        lstroutes = m.get(analyzer['stops'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg


# ==============================
# Funciones Helper
# ==============================

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name

# ==============================
# Funciones de Ordenamiento
# ==============================

def sortAirportsConnections(list):
    return ms.sort(list, compareConnections)



# ==============================
# Funciones de Comparacion
# ==============================


def compareAirports(airport, keyvalueairport):
    """
    Compara dos estaciones
    """
    airportcode = str(keyvalueairport['key'])
    if (str(airport) == airportcode):
        return 0
    elif (str(airport) > airportcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1
def compareConnections(airportNumConnections1, airportNumConnections2):
    return airportNumConnections1['numConnections'] > airportNumConnections2['numConnections']     
