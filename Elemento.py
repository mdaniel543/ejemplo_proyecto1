from Nodo import Nodo
from ListaSimple import ListaSimple

class Elemento(Nodo):
    def __init__(self, nombre, id):
        super().__init__()
        self.nombre = nombre
        self.id = id
        self.items = ListaSimple()
        
    def imprimir(self):
        print(f'Elemento --- Nombre: {self.nombre}, ID: {self.id}')
        self.items.mostrar()
        
        
    