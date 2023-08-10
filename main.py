import xml.etree.ElementTree as ET

# Cargando el XML desde el archivo
tree = ET.parse('datos.xml')
root = tree.getroot()


#HOLAAAAAA

# Recorriendo el árbol XML
for elemento in root.findall('elemento'):
    nombre = elemento.get('nombre')
    id_val = elemento.get('id')
    print(f'Elemento: Nombre={nombre}, ID={id_val}')

    for item in elemento.findall('item'):
        value = item.get('value')
        text = item.text
        print(f'    Item: Value={value}, Text={text}')

