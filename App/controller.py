
import config as cf
from DISClib.ADT import map as m
from DISClib.ADT.graph import gr
from App import model
import csv

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos del analyzer
# ___________________________________________________

def loadCities(analyzer, citiesFile):
    citiesFile = cf.data_dir + citiesFile
    input_file = csv.DictReader(open(citiesFile, encoding="utf-8"),
                                delimiter=",")
    for city in input_file:
        model.addCity(analyzer, city)
        
    return analyzer


def loadAirports(analyzer, airportsFile):
    airportsFile = cf.data_dir + airportsFile
    input_file = csv.DictReader(open(airportsFile, encoding="utf-8"),
                                delimiter=",")
    for airport in input_file:
        model.addAirport(analyzer, airport)
        
    return analyzer


def loadAirportsGraphs(analyzer, routesFile):
    routesFile = cf.data_dir + routesFile
    input_file = csv.DictReader(open(routesFile, encoding="utf-8"),
                                delimiter=",")
    aeropuertosConectados = 0                            
    for route in input_file:
        departure = route['Departure']
        departureVertex = m.get(analyzer['airports'], departure)['key']
        destination = route['Destination']
        destinationVertex = m.get(analyzer['airports'], destination)['key']
        distance = float(route['distance_km'])
        model.addAirportsConnection(analyzer, departureVertex, destinationVertex, distance)
        aeropuertosConectados += 1
  
    analyzer['Aeropuertos conectados grafo'] = gr.numVertices(analyzer['No Directed airports'])
    analyzer['Aeropuertos conectados digrafo'] = gr.numVertices(analyzer['Directed airports'])

    return analyzer


def loadNoConnectedAirports(analyzer):
    return model.addNoconnectedAirports(analyzer)    

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def mostConnectedAirports(analyzer):
    return model.mostConnectedAirports(analyzer)

def cantidadClusteres(iata1, iata2, analyzer):
    return model.cantidadClusteres(iata1, iata2, analyzer)  

def rutaMasCorta(ciudad1, ciudad2, analyzer):
    return model.rutaMasCorta(ciudad1, ciudad2, analyzer)   

def millasViajero(analyzer, ciudadOrigen):
    return model.millasViajero(analyzer, ciudadOrigen)  

def aeropuertosAfectados(analyzer, aeropuertoEliminado):
    return model.aeropuertosAfectados(analyzer, aeropuertoEliminado)       

# ___________________________________________________
#  Funciones para ordenar
# ___________________________________________________

def sortAirportsConnections(list):
    return model.sortAirportsConnections(list)

def ac(latitudCiudad, longitudCiudad, analyzer):
    return model.aerepuertosCercanos(latitudCiudad, longitudCiudad, analyzer)  

# ==============================================
# Funciones axiliares para funciones de consulta
# ==============================================

def mapCiudades(analyzer):
    return model.mapCiudades(analyzer)
