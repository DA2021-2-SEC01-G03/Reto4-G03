
import json
import sys
import config
import threading
from App import controller
from DISClib.ADT import stack
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.ADT.graph import gr
assert config
from timeit import default_timer

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


airportsFile = 'airports-utf8-large.csv'
routesFile = 'routes-utf8-large.csv'
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
    print("Digrafo de aeropuertos: " )
    print("Total aeropuertos grafo dirigido: " + str(gr.numVertices(analyzer['Directed airports'])))
    print("Total rutas aereas grafo dirigido: " + str(gr.numEdges(analyzer['Directed airports'])))
    print("Primer aeropuerto grafo dirigido: ")
    print(str(lt.firstElement(gr.vertices(analyzer['Directed airports']))))
    print("último aeropuerto grafo dirigido: ")
    print(str(lt.lastElement(gr.vertices(analyzer['Directed airports']))))
    print("")
    print("Digrafo de aeropuertos: " )
    print("Total aeropuertos grafo no dirigido: " + str(gr.numVertices(analyzer['No Directed airports'])))
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
    listAirportsConnections = controller.mostConnectedAirports(analyzer)
    orderedList = controller.sortAirportsConnections(listAirportsConnections)
    print("Los aereopuertos mas interconectados son: ")
    top5MostConnectedAirports = lt.subList(orderedList, 1, 5)
    for airport in lt.iterator(top5MostConnectedAirports):
        print("Aereopuerto: " +  str(airport['airport']) + "Aereopuertos conectados: " + str(airport['numConnections']))
#

def optionFour(iata1, iata2, analyzer):
    clusteresTotales = controller.cantidadClusteres(iata1,iata2,analyzer)[0]
    confirmIatas = controller.cantidadClusteres(iata1,iata2,analyzer) [1]
    
    print("Número de SCC en red de aeropuertos: ")
    print(clusteresTotales)
    print("")
    print("Están los aeropuertos 1 y 2 con codigo Iata " + str(iata1) + " y " + str(iata2) + " en el mismo cluster: ")
    print(confirmIatas)


def optionFive(analyzer, destStation):
    haspath = controller.hasPath(analyzer, destStation)
    print('Hay camino entre la estación base : ' +
          'y la estación: ' + destStation + ': ')
    print(haspath)


def optionSix(analyzer, destStation):
    inicio = default_timer()
    path = controller.minimumCostPath(analyzer, destStation)
    if path is not None:
        pathlen = stack.size(path)
        print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print(stop)
    else:
        print('No hay camino')

    fin = default_timer()
    print("Tiempo de ejecución: " + str(fin -  inicio))   


def optionSeven(analyzer):
    maxvert, maxdeg = controller.servedRoutes(analyzer)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))


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
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionFive(analyzer, destStation)

        elif int(inputs[0]) == 6:
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionSix(analyzer, destStation)

        elif int(inputs[0]) == 7:
            optionSeven(analyzer)

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
