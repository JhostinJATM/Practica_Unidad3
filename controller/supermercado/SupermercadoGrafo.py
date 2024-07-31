from controller.supermercado.SupermercadoControl import SuperMercadoControl
from controller.tda.graph.graphLabelNoManaged import GraphLabelNoManaged
import json
import os 
import time

class SuperMercadoGrafo:
        
    def __init__(self):
        self.__grafo = None
        self._nado = SuperMercadoControl()
        
    def create_graph(self):
        ruta_json = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/data/grafo.json"
        
        with open(ruta_json, 'r') as file:
            data = json.load(file)
        
        nodes = data['nodes']
        num_vertices = len(nodes)
        self.__grafo = GraphLabelNoManaged(num_vertices)
        
        for node in nodes:
            vertex = node['id'] 
            vertex_or = vertex - 1
            self.__grafo.label_vertex(vertex_or, str(vertex_or))
        
        edges = data['edges']
        for edge in edges:
            source = edge['source'] 
            source_or = source - 1
            target = edge['target'] 
            target_or = target - 1
            distance = edge['distance']
            self.__grafo.insertar_arista_peso_E(source_or, target_or, float(distance))
        
        self.__grafo.paint_graph_obj(self._nado._lista.toArray)
        
    def camino_floyd(self, start, end):
        self.create_graph()
        if self.__grafo is None:
            raise ValueError("El grafo no ha sido inicializado.")
        
        num_vertices = self.__grafo.num_vertex  
        
        inicial = time.time()
        
        dist = [[float('inf')] * num_vertices for _ in range(num_vertices)]
        next_node = [[-1] * num_vertices for _ in range(num_vertices)]
        
        
        for u in range(num_vertices):
            dist[u][u] = 0
            for adj in self.__grafo.adjacent_E(u).toArray: 
                v = adj._destination
                weight = adj._weight
                if weight is None:
                    weight = float('inf')
                dist[u][v] = weight
                next_node[u][v] = v
        
        for k in range(num_vertices):
            for i in range(num_vertices):
                for j in range(num_vertices):
                    if dist[i][k] < float('inf') and dist[k][j] < float('inf'):
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
                            next_node[i][j] = next_node[i][k]

        final = time.time()
        tiempo = final - inicial
        
        camino_corto = []
        if next_node[start][end] == -1:
            return (float('inf'), [])  
        
        current = start
        while current != end:
            if current == -1:  
                return (float('inf'), [])
            camino_corto.append(current)
            current = next_node[current][end]
        
        camino_corto.append(end)
        
        # print(f"Aqui 1:{(camino_corto)}")
        return camino_corto, tiempo


    def camino_dijkstra(self, start, end):
        self.create_graph()
        if self.__grafo is None:
            raise ValueError("El grafo no ha sido inicializado.")
        
        inicial = time.time()
        
        num_vertices = self.__grafo.num_vertex
        dist = [float('inf')] * num_vertices  
        dist[start] = 0  
        pred = [-1] * num_vertices  
        visited = [False] * num_vertices 
        
        priority_queue = [(0, start)] 
        
        while priority_queue:
            priority_queue.sort()  
            current_dist, u = priority_queue.pop(0)  
            
            if visited[u]:
                continue
            
            visited[u] = True
            
            for adj in self.__grafo.adjacent_E(u).toArray:  
                v = adj._destination
                weight = adj._weight
                if not visited[v] and current_dist + weight < dist[v]:
                    dist[v] = current_dist + weight  
                    pred[v] = u 
                    priority_queue.append((dist[v], v))
        
        
        final = time.time()
        tiempo = final - inicial
        
        camino_corto = []
        if dist[end] == float('inf'): 
            return float('inf'), []  
        
        while end != -1:
            camino_corto.append(end)
            end = pred[end]
        
        camino_corto.reverse() 
        
        if camino_corto[0] == start:
            # print(f"aqui:  {camino_corto}")
            return camino_corto , tiempo


