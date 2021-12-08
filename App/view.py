

import sys
import config
import threading
from App import controller
from DISClib.Utils import error as error
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.ADT.graph import gr, numEdges
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


airportsFile = 'airports-utf8-small.csv'
routesFile = 'routes-utf8-small.csv'
citiesFile = 'worldcities-utf8.csv'


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")
    print("0- Salir")
    print("*******************************************")


def optionTwo(analyzer):
    print("\nCargando información de transporte de singapur ....")
    controller.loadAirports(analyzer, airportsFile)
    controller.loadAirportsGraphs(analyzer, routesFile)
    controller.loadCities(analyzer, citiesFile)
    controller.loadNoConnectedAirports(analyzer)
    print("Digrafo de aeropuertos: " )
    print("Total aeropuertos grafo dirigido: " + str(gr.numVertices(analyzer['Directed airports'])))
    print("Total rutas aereas grafo dirigido: " + str(gr.numEdges(analyzer['Directed airports'])))
    print("Primer aeropuerto grafo dirigido: ")
    print(str(lt.firstElement(gr.vertices(analyzer['Directed airports']))))
    print("último aeropuerto grafo dirigido: ")
    print(str(lt.lastElement(gr.vertices(analyzer['Directed airports']))))
    print("")
    print("Grafo no dirigido de aeropuertos: " )
    print("Total aeropuertos grafo no dirigido: " +str(gr.numVertices(analyzer['No Directed airports'])))
    print("Total rutas aereas grafo no dirigido: " + str(gr.numEdges(analyzer['No Directed airports'])))
    print("Primer aeropuerto grafo no dirigido: ")
    print(str(lt.firstElement(gr.vertices(analyzer['Directed airports']))))
    print("último aeropuerto grafo no dirigido: ")
    print(str(lt.lastElement(gr.vertices(analyzer['No Directed airports']))))
    print("")
    print("Red de ciudades: ")
    print("Total de ciudades cargadas: " + str(m.size(analyzer['cities'])))
    print("La primera ciudad cargada fue: " + str(lt.lastElement(m.valueSet(analyzer['cities']))))
    print("La última ciudad cargada fue: " + str(lt.firstElement(m.valueSet(analyzer['cities']))))
    
    


def optionThree(analyzer):
    listAirportsConnections = controller.mostConnectedAirports(analyzer)[0]
    orderedList = controller.sortAirportsConnections(listAirportsConnections)
    print("Aeropuertos conectados dentro de la red: " + str(analyzer['Aeropuertos conectados digrafo']))
    print("Los aereopuertos mas interconectados son: ")
    top5MostConnectedAirports = lt.subList(orderedList, 1, 5)
    for airport in lt.iterator(top5MostConnectedAirports):
        print("Aereopuerto: " +  str(airport['airport']) + ", Conexiones: " + str(airport['numConnections']))
#

def optionFour(iata1, iata2, analyzer):
    clusteresTotales = controller.cantidadClusteres(iata1,iata2,analyzer)[0]
    confirmIatas = controller.cantidadClusteres(iata1,iata2,analyzer) [1]
    print("")
    print("Número de SCC en red de aeropuertos: " + str(clusteresTotales))
    print("")
    print("Están los aeropuertos 1 y 2 con codigo Iata " + str(iata1) + " y " + str(iata2) + " en el mismo cluster: ")
    print("Respuesta: " + str(confirmIatas))


def optionFive(ciudad1, ciudad2, analyzer):
    aeropuertoOrigen = controller.rutaMasCorta(ciudad1, ciudad2, analyzer)[0]
    aeropuertoDestino = controller.rutaMasCorta(ciudad1, ciudad2, analyzer)[1]

    ruta = controller.rutaMasCorta(ciudad1, ciudad2, analyzer)[2]
    camino = controller.rutaMasCorta(ciudad1, ciudad2, analyzer)[3]
    paradas = controller.rutaMasCorta(ciudad1, ciudad2, analyzer)[4]

    print("El aeropueto de origen es " + str(aeropuertoOrigen))
    print("El aeropuerto de destino es " + str(aeropuertoDestino))
    print("Distancia total: " + str(ruta))
    print("")
    print("Camino del viaje: ")
    for viaje in lt.iterator(camino):
        print('Origen: ' + str(viaje['vertexA']) + ', Destino: ' + str(viaje['vertexB']) + ', Distancia_km: ' + str(viaje['weight']))
    print("")
    print("Paradas del viaje")
    print(str(aeropuertoOrigen))
    for parada in lt.iterator(paradas):
        print(parada)



def optionSix(analyzer, ciudadOrigen):
    print(controller.millasViajero(analyzer, ciudadOrigen)) 


def optionSeven(analyzer, aeropuertoEliminado):
    aeropuertosDigrafo = controller.aeropuertosAfectados(analyzer, aeropuertoEliminado)[0]
    rutasDigrafo = controller.aeropuertosAfectados(analyzer, aeropuertoEliminado)[1]
    aeropuertosGrafo = controller.aeropuertosAfectados(analyzer, aeropuertoEliminado)[2]
    rutasGrafo = controller.aeropuertosAfectados(analyzer, aeropuertoEliminado)[3]
    listaAfectados = controller.aeropuertosAfectados(analyzer, aeropuertoEliminado)[4]

    print("Numero de aeropuertos Digrafo original: " + str(gr.numVertices(analyzer['Directed airports'])) + ', rutas: ' + str(gr.numEdges(analyzer['Directed airports'])))
    print("Numero de aeropuertos grafo original: " + str(gr.numVertices(analyzer['No Directed airports'])) + ', rutas: ' + str(gr.numEdges(analyzer['No Directed airports'])))
    print("")
    print("Numero de aeropuertos resultantes del digrafo: " + str(aeropuertosDigrafo) + ", rutas: " + str(rutasDigrafo))
    print("Numero de aeropuertos resultantes del grafo: " + str(aeropuertosGrafo) + ", rutas: " + str(rutasGrafo) )
    print("Aeropuertos afectados")
    for aeropuerto in lt.iterator(listaAfectados):
        print(aeropuerto)

"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            # analyzer es el controlador que se usará de acá en adelante
            analyzer = controller.init()

        elif int(inputs[0]) == 2:
            optionTwo(analyzer)

        elif int(inputs[0]) == 3:
            optionThree(analyzer)

        elif int(inputs[0]) == 4:
            iata1 = input("ingrese código Iata del aeropuerto 1: ")
            iata2 = input("ingrese código Iata del aeropuerto 2: ")
            optionFour(iata1,iata2 ,analyzer)
            
           

        elif int(inputs[0]) == 5:
            mapCiudades = controller.mapCiudades(analyzer)
            ciudadCorrectaOrigen = ciudadElegida(mapCiudades, "origen")
            ciudadCorrectaDestino = ciudadElegida(mapCiudades, "destino")
            optionFive(ciudadCorrectaOrigen, ciudadCorrectaDestino, analyzer)
            

        elif int(inputs[0]) == 6:
            ciudadOrigen = input("Ingrese ciudad de origen: ")
            optionSix(analyzer, ciudadOrigen)

        elif int(inputs[0]) == 7:
            aeropuertoEliminado = input("Codigo iata aeropuerto eliminado: ")
            optionSeven(analyzer, aeropuertoEliminado)


        elif int(inputs[0]) == 8:
            longitudCiudad = float(input("Longitud ciudad: "))
            latitudCiudad = float(input("Latitud ciudad: "))
            print(controller.ac(latitudCiudad, longitudCiudad, analyzer))
        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()

#Auxiliar

def ciudadElegida(mapCiudades, tipoCiudad):
    ciudadCargada = False
    while ciudadCargada == False:
     ciudad = input("Ingrese el nombre de la ciudad de " + str(tipoCiudad) + ": ")
     llaveCiudad = m.get(mapCiudades, ciudad)    
     if llaveCiudad == None:
        print('La ciudad elegida no existe en las ciudades cargadas')
     else:
        ciudadCargada = True   

    bucket = llaveCiudad['value']    
    if lt.size(bucket) > 1:
        print("Hay más de una ciudad con el mismo nombre, escoger una entre las siguientes ")
        i = 1
        for ciudad in lt.iterator(bucket):
            print("Opcion " + str(i) + "- " + str(ciudad))
            i += 1
        opcionElegida = int(input("Elija una opcion"))
        ciudad1Correcta = lt.getElement(bucket, opcionElegida)['id']
    elif lt.size(bucket) == 1:
        ciudad1Correcta = lt.getElement(bucket, 1)['id']
 
    return ciudad1Correcta 

