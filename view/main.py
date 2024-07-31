import sys
from tabulate import tabulate
sys.path.append('../')
from controller.supermercado.SupermercadoControl import SuperMercadoControl
from controller.supermercado.SupermercadoGrafo import SuperMercadoGrafo

if __name__ == "__main__":
    superme = SuperMercadoGrafo()

    start_vertex = 0
    end_vertex = 2
    
    camino_floyd, tiempo_floyd = superme.camino_floyd(start_vertex, end_vertex)
    camino_dijkstra, tiempo_dijkstra = superme.camino_dijkstra(start_vertex, end_vertex)

    tabla_datos = [
        ["Algoritmo", "Camino", "Tiempo (ns)"],
        ["Floyd-Warshall", camino_floyd, tiempo_floyd],
        ["Dijkstra", camino_dijkstra, tiempo_dijkstra]
    ]

    tabla = tabulate(tabla_datos, headers="firstrow", tablefmt="grid")

    print(tabla)
