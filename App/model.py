
from DISClib.DataStructures.arraylist import addLast
import config
from DISClib.ADT.graph import getEdge, gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim 
from DISClib.Utils import error as error
assert config
import math

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
                    'Tabla rutas': None,
                    'Aeropuertos conectados digrafo': None,
                    'Aeropuertos conectados grafo': None,
                    'Rutas cargadas digrafo':  0,
                    'Rutas cargadas grafo': 0
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

        analyzer['Tabla rutas'] = m.newMap(numelements=40000,
                                     maptype='PROBING')   

        return analyzer

    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# =================================================
# Funciones de para agregar información al analyzer
# =================================================

def addCity(analyzer, city):
    m.put(analyzer['cities'], city['id'], city)

def addAirport(analyzer, airport):
    airports = analyzer['airports']
    iso = airport['IATA']
    m.put(airports, iso, airport)  


def addAirportsDigraph(analyzer, departure, destination, distance):  
    if gr.containsVertex(analyzer['Directed airports'], departure) == False:
        gr.insertVertex(analyzer['Directed airports'], departure)
    if gr.containsVertex(analyzer['Directed airports'], destination) == False:
        gr.insertVertex(analyzer['Directed airports'], destination)
        
    if gr.containsVertex(analyzer['Directed airports'], departure) and gr.containsVertex(analyzer['Directed airports'], destination):
        analyzer['Rutas cargadas digrafo'] += 1
        if gr.getEdge(analyzer['Directed airports'], departure, destination) == None:       
           gr.addEdge(analyzer['Directed airports'], departure, destination, distance)
  


def addAirportsGraph(analyzer, departure, destination, distance, aerolinea):
    if m.get(analyzer['Tabla rutas'], destination + "_" + departure) != None:
     bucket2 = m.get(analyzer['Tabla rutas'], destination+ "_" +departure)['value']
     if lt.isPresent(bucket2, aerolinea):
        analyzer['Rutas cargadas grafo'] += 1

    if m.contains(analyzer['Tabla rutas'], departure + "_" + destination):
        bucket = m.get(analyzer['Tabla rutas'], departure + "_" + destination)['value']
        if lt.isPresent(bucket, aerolinea) == False:
         lt.addLast(bucket, aerolinea)
         m.put(analyzer['Tabla rutas'], departure + "_" + destination, bucket)

    else:
        bucket = lt.newList('ARRAY_LIST')
        lt.addLast(bucket, aerolinea)
        m.put(analyzer['Tabla rutas'], departure + "_" + destination, bucket)       

    if gr.containsVertex(analyzer['No Directed airports'], departure) == False:
        gr.insertVertex(analyzer['No Directed airports'], departure)
    if gr.containsVertex(analyzer['No Directed airports'], destination) == False:
        gr.insertVertex(analyzer['No Directed airports'], destination)

    if gr.getEdge(analyzer['Directed airports'], destination, departure) != None: 
        if gr.getEdge(analyzer['No Directed airports'], departure, destination) == None:
         gr.addEdge(analyzer['No Directed airports'], departure, destination, distance)

     
def addNoconnectedAirports(analyzer):
    airportsList = m.valueSet(analyzer['airports'])
    for airport in lt.iterator(airportsList):
      iso = airport['IATA']
      if gr.containsVertex(analyzer['Directed airports'], iso) == False:
        gr.insertVertex(analyzer['Directed airports'], iso)
      if gr.containsVertex(analyzer['No Directed airports'], iso) == False:  
        gr.insertVertex(analyzer['No Directed airports'], iso)  

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

def aerepuertosCercanos(latitudCiudad,longitudCiudad, analyzer):
    aereopuertos = analyzer['airports'] 
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

    distanciaMinima = djk.Dijkstra(aeropuertos, origen) 
    ruta = djk.distTo(distanciaMinima, destino)
    camino = djk.pathTo(distanciaMinima, destino)

    i = 0
    tam = st.size(camino)
    listaCamino = lt.newList('ARRAY_LIST')
    listaParadas = lt.newList('ARRAY_LIST')

    while i < tam:
     xd = st.pop(camino)
     lt.addLast(listaCamino, xd)
     lt.addLast(listaParadas, xd['vertexB'])
     i += 1


    if ruta == math.inf:
      ruta = "No existe camino"
      rutaTotal = "No existe camino"
    else:    
      rutaTotal = float(distanciaDestino) + float(distanciaOrigen) + float(ruta)    

    return origen, destino, ruta, listaCamino, listaParadas


def millasViajero(analyzer, ciudadOrigen):
    aeropuertos = analyzer['No Directed airports']
    xd = prim.PrimMST(aeropuertos)
    origen = prim.prim(aeropuertos, xd, ciudadOrigen)
    
    return xd

def aeropuertosAfectados(analyzer, aeropuertoEliminado):
    degreeAeropuertoDirigido = 0
    degreeAeropuertoNoDirigido = 0
    for ruta in lt.iterator(m.keySet(analyzer['Tabla rutas'])):    
        if aeropuertoEliminado in ruta:
            bucketAerolineas = m.get(analyzer['Tabla rutas'], ruta)['value']
            degreeAeropuertoDirigido += lt.size(bucketAerolineas)
            for aerolinea in lt.iterator(bucketAerolineas):
             rutaVuelta = ruta[4] + ruta[5] + ruta[6] + "_" + ruta[0] + ruta[1] + ruta[2]
             if m.get(analyzer['Tabla rutas'], rutaVuelta) != None:
                if lt.isPresent(m.get(analyzer['Tabla rutas'], rutaVuelta)['value'], aerolinea): 
                  degreeAeropuertoNoDirigido += 0.5

    numAeropuertosNuevoDigrafo = gr.numVertices(analyzer['Directed airports']) - 1
    numAeropuertosNuevoGrafo = gr.numVertices(analyzer['Directed airports']) - 1

    numRutasNuevoDigrafo = analyzer['Rutas cargadas digrafo'] - degreeAeropuertoDirigido
    numRutasNuevoGrafo = analyzer['Rutas cargadas grafo'] - degreeAeropuertoNoDirigido

    afectados = gr.adjacents(analyzer['Directed airports'], aeropuertoEliminado)

    return numAeropuertosNuevoDigrafo, numRutasNuevoDigrafo, numAeropuertosNuevoGrafo, numRutasNuevoGrafo, afectados


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


# ==============================================
# Funciones axiliares para funciones de consulta
# ==============================================

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
