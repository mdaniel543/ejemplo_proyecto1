import xml.etree.ElementTree as ET

import os
from ListaSimple import ListaSimple
from Elemento import Elemento
from Item import Item

elementos = ListaSimple()

def carga_datos():
    # Cargando el XML desde el archivo
    tree = ET.parse('datos.xml')
    root = tree.getroot()
    # Recorriendo el árbol XML
    for elemento in root.findall('elemento'):
        nombre = elemento.get('nombre')
        id_val = elemento.get('id')
        cols = int(elemento.get('cols'))
        rows = int(elemento.get('rows'))
        elemento_nuevo = Elemento(nombre, id_val, cols, rows)
        
        for item in elemento.findall('item'):
            row = int(item.get('row'))
            col = int(item.get('col'))
            text = item.text
            elemento_nuevo.items.agregar_al_final(Item(row, col, text))

        elementos.agregar_al_final(elemento_nuevo)
        
    print("Datos cargados exitosamente")
    
    
def graficar(elemento):
    dot_string = 'digraph G {\n'
    dot_string += elemento.to_dot()
    dot_string += "}\n"
    with open("matriz.dot", "w") as archivo:
        archivo.write(dot_string)
    os.system("dot -Tpng matriz.dot -o matriz.png")
    print("¡Gráfica generada en matriz.png!")

       
def menu():
    while True: 
        print("MENU PRINCIPAL")
        print("1. Cargar datos")
        print("2. Mostrar elementos")
        print("3. Buscar elemento por ID y generar imagen")
        print("4. Salir")
        opcion = input("Ingrese una opción: ")
        if opcion == "1":
            carga_datos()
        elif opcion == "2":
            elementos.mostrar()
        elif opcion == "3":
            elementos.mostrar()
            id_val = input("Ingrese el ID del elemento: ")
            elemento = elementos.buscar_por_id(id_val)
            if elemento:
                graficar(elemento)
            else:
                print(f"El elemento con ID {id_val} no existe")
        elif opcion == "4":
            break
        else:
            print("Opción inválida")
        input("Presione ENTER para continuar...")
        os.system('cls')

    
if __name__ == '__main__':
    menu()
        

