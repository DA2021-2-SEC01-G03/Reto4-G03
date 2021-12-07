
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim 

from DISClib.Utils import error as error
assert config
import math

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
                    'No Directed airports': None,
                    'paths': None
                    }
       
        analyzer['cities'] = m.newMap(numelements=80000,
                                     maptype='PROBING')


        analyzer['airports'] = m.newMap(numelements=20000,
                                     maptype='PROBING')

        analyzer['airports2'] = m.newMap(numelements=20000,
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
    m.put(analyzer['cities'], city['id'], city)


def addAirport(analyzer, airport):
    airports = analyzer['airports']
    airports2 = analyzer['airports2']
    iso = airport['IATA']
    m.put(airports, iso, airport['IATA'])
    m.put(airports2, iso, airport)
    if gr.containsVertex(analyzer['Directed airports'], iso) == False:
        gr.insertVertex(analyzer['Directed airports'], iso)
    if gr.containsVertex(analyzer['No Directed airports'], iso) == False:
        gr.insertVertex(analyzer['No Directed airports'], iso)    


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
    scc1 = scc.KosarajuSCC(analyzer['Directed airports'])
    clusteresTotales = scc.connectedComponents(scc1)
    confirmIatas = scc.stronglyConnected(scc1, iata1, iata2)
    
    return clusteresTotales, confirmIatas
#

def mapCiudades(analyzer):
    ciudades = analyzer['cities']
    ciuadesMismoNombre =  m.newMap(maptype='PROBING')
    listaCiudades = m.valueSet(ciudades)
    for ciudad in lt.iterator(listaCiudades):
        if m.contains(ciuadesMismoNombre, ciudad['city']):
         dict = {'id': ciudad['id'], 'Región': ciudad['admin_name'], 'Latitud': ciudad['lat'], 'Longitud': ciudad['lng'], 'País': ciudad['country'] }
         bucket = m.get(ciuadesMismoNombre, ciudad['city'])['value'] 
         lt.addLast(bucket, dict)
         m.put(ciuadesMismoNombre, ciudad['city'], bucket)  
        else:
         bucket = lt.newList('ARRAY_LIST')        
         dict = {'id': ciudad['id'], 'Región': ciudad['admin_name'], 'Latitud': ciudad['lat'], 'Longitud': ciudad['lng'], 'País': ciudad['country'] }
         lt.addLast(bucket, dict)
         m.put(ciuadesMismoNombre, ciudad['city'], bucket)

    return ciuadesMismoNombre     

def distanciaGeografica(latitud1:float, latitud2:float, longitud1:float, longitud2:float):
    return 6371*math.acos(math.cos(math.radians(90-latitud1))*math.cos(math.radians(90-latitud2))+math.sin(math.radians(90- latitud1))*math.sin(math.radians(90-latitud2))*math.cos(math.radians(longitud1-longitud2))) 


def aerepuertosCercanos(latitudCiudad,longitudCiudad, analyzer):
    aereopuertos = analyzer['airports2'] 
    listaAereopuertos = m.valueSet(aereopuertos)
    distanciaMenor = 10000000000000
    aereopuertoMenorDistancia = ""
    for aereopuerto in lt.iterator(listaAereopuertos):

        lonAereopuerto = float(aereopuerto['Longitude'])
        latAereopuerto = float(aereopuerto['Latitude'])
        distancia = distanciaGeografica(latitudCiudad, latAereopuerto, longitudCiudad, lonAereopuerto)
        if distancia <= distanciaMenor:
            distanciaMenor = distancia
            aereopuertoMenorDistancia = aereopuerto['IATA']

    return aereopuertoMenorDistancia, distanciaMenor


def rutaMasCorta(ciudad1, ciudad2, analyzer):
    mapCiudades = analyzer['cities']
    aeropuertos = analyzer['Directed airports']


    longitudCiudad1 = float(m.get(mapCiudades, ciudad1)['value']['lng'])
    latitudCiudad1 = float(m.get(mapCiudades, ciudad1)['value']['lat'])
    
    longitudCiudad2 = float(m.get(mapCiudades, ciudad2)['value']['lng'])
    latitudCiudad2 = float(m.get(mapCiudades, ciudad2)['value']['lat'])

    origen = aerepuertosCercanos(latitudCiudad1, longitudCiudad1, analyzer)[0]
    destino = aerepuertosCercanos(latitudCiudad2, longitudCiudad2, analyzer)[0]

    distanciaOrigen = aerepuertosCercanos(latitudCiudad1, longitudCiudad1, analyzer)[1]
    distanciaDestino = aerepuertosCercanos(latitudCiudad2, longitudCiudad2, analyzer)[1]

    xd = djk.Dijkstra(aeropuertos, origen) 
    ruta = djk.distTo(xd, destino)
    rutaTotal = float(distanciaOrigen) + float(distanciaDestino) + float(ruta)


    return origen, destino, ruta, rutaTotal


def millasViajero(analyzer, ciudadOrigen):
    aeropuertos = analyzer['No Directed airports']
    xd = prim.PrimMST(aeropuertos)
    origen = prim.prim(aeropuertos, xd, ciudadOrigen)
    
    return xd

def aeropuertosAfectados(analyzer, aeropuertoEliminado):
    digrafo = analyzer['Directed airports']    
    grafo = analyzer['No Directed airports'] 

    aeropuertos = analyzer['airports'] 

    gr.removeVertex(digrafo, aeropuertoEliminado)
    gr.removeVertex(grafo, aeropuertoEliminado)

    numAeropuertosNuevoDigrafo = m.size(aeropuertos)
    numAeropuertosNuevoGrafo = m.size(aeropuertos)

    numRutasNuevoDigrafo = gr.numEdges(digrafo)
    numRutasNuevoGrafo = gr.numEdges(grafo)

    return numAeropuertosNuevoDigrafo, numRutasNuevoDigrafo, numAeropuertosNuevoGrafo, numRutasNuevoGrafo








        






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
