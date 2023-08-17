import xml.etree.ElementTree as ET

from ListaSimple import ListaSimple
from Elemento import Elemento
from Item import Item

# Cargando el XML desde el archivo
tree = ET.parse('datos.xml')
root = tree.getroot()


elementos = ListaSimple()


# Recorriendo el árbol XML
for elemento in root.findall('elemento'):
    nombre = elemento.get('nombre')
    id_val = elemento.get('id')
    elemento_nuevo = Elemento(nombre, id_val)

    for item in elemento.findall('item'):
        row = int(item.get('row'))
        col = int(item.get('col'))
        text = item.text
        item_nuevo = Item(row, col, text)
        elemento_nuevo.items.agregar_al_final(item_nuevo)
        
    elementos.agregar_al_final(elemento_nuevo)

elementos.mostrar()