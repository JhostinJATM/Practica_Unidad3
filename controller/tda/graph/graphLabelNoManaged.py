from controller.tda.graph.graphLabelManaged import GraphLabelManaged
from controller.exception.arrayPositionException import ArrayPositionException
from controller.supermercado.SupermercadoControl import SuperMercadoControl
from math import nan
import os
import json
from controller.tda.linked.linkedList import LinkedList

class GraphLabelNoManaged(GraphLabelManaged):
    def __init__(self, num_vert):
        super().__init__(num_vert)

    def insertar_arista_peso_E(self, label1, label2, weight):
        v1 = self.getVertex(label1)
        v2 = self.getVertex(label2)

        if v1 == -1:
            v1 = self.num_vertex
            self.setNumVertex(self.num_vertex + 1)  
            self.label_vertex(v1, label1)

        if v2 == -1:
            v2 = self.num_vertex
            self.setNumVertex(self.num_vertex + 1) 
            self.label_vertex(v2, label2)

        self.insert_edges_weight(v1, v2, weight)
        self.insert_edges_weight(v2, v1, weight)
