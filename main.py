import xml.etree.ElementTree as ET

import os
from ListaDoble import ListaDoble
from Elemento import Elemento
from Item import Item

elementos = ListaDoble()

def carga_datos():
    #solicitar la ruta del archivo
    ruta = input("Ingrese la ruta del archivo: ")
    #validar que el archivo exista
    if not os.path.isfile(ruta):
        print("El archivo no existe")
        return
    #validar que el archivo sea .xml
    if not ruta.endswith(".xml"):
        print("El archivo debe ser .xml")
        return
    elementos.inicializar()
    #cargar el archivo
    tree = ET.parse(ruta)
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

        elementos.insertarOrdenadoPorId(elemento_nuevo)
        
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
        print ("3. Mostar elementos al reves")
        print("4. Buscar elemento por ID y generar imagen")
        print ("5. Buscar elemento y eliminarlo")
        print ("6. Buscar elemento y cambiar su nombre")
        print ("7. Generar nuevo archivo XML")
        print("8. Salir")
        opcion = input("Ingrese una opción: ")
        if opcion == "1":
            carga_datos()
        elif opcion == "2":
            elementos.mostrar()
        elif opcion == "3":
            elementos.mostrar_inverso()
        elif opcion == "4":
            elementos.mostrar()
            id_val = input("Ingrese el ID del elemento: ")
            elemento = elementos.buscar_por_id(id_val)
            if elemento:
                graficar(elemento)
            else:
                print(f"El elemento con ID {id_val} no existe")
        elif opcion == "5":
            elementos.mostrar()
            id_val = input("Ingrese el ID del elemento: ")
            if elementos.eliminar(id_val):
                print(f"El elemento con ID {id_val} ha sido eliminado")
            else:
                print(f"El elemento con ID {id_val} no existe")
        elif opcion == "6":
            elementos.mostrar()
            id_val = input("Ingrese el ID del elemento: ")
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            if elementos.actualizar(id_val, nuevo_nombre):
                print(f"El elemento con ID {id_val} ha sido actualizado")
            else:
                print(f"El elemento con ID {id_val} no existe")
                
        elif opcion == "7":
            elementos.escribirXML()
            
        elif opcion == "8":
            break
        else:
            print("Opción inválida")
        input("Presione ENTER para continuar...")
        os.system('cls')

    
if __name__ == '__main__':
    menu()
        

