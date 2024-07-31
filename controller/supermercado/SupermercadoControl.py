from typing import Type
from controller.dao.daoAdapter import DaoAdapter
from model.supermercado import SuperMercado 

class SuperMercadoControl(DaoAdapter):
    def __init__(self):
        super().__init__(SuperMercado)
        self.__supermercado = None

    @property
    def _supermercado(self):
        if self.__supermercado == None:
            self.__supermercado = SuperMercado()
        return self.__supermercado

    @_supermercado.setter
    def _supermercado(self, value):
        self.__supermercado = value

    @property
    def _lista(self):
        return self._list()
    
    def merge(self, pos):
        self._merge(self._supermercado, pos)
    
    @property
    def save(self):
        try:
            self._supermercado._id = self._lista._length + 1
            self._save(self._supermercado)
        except Exception as e:
            print(e)

