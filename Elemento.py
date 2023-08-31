from Nodo import Nodo
from ListaSimple import ListaSimple

class Elemento(Nodo):
    def __init__(self, nombre, id, cols, rows):
        super().__init__()
        self.nombre = nombre
        self.id = id
        self.cols = cols
        self.rows = rows
        self.items = ListaSimple()
        
    def imprimir(self):
        print(f'Elemento --- Nombre: {self.nombre}, ID: {self.id}')
        #self.showItemsConsole()
        
        
    def to_dot(self):
        # Nodo principal del elemento
        nodo_id = f'elemento_{self.id}'
        cadena = f'"{nodo_id}" [label="{self.nombre}", shape=ellipse, color=blue];\n'
        
        # Nodos para rows y cols
        nodo_rows = f"{nodo_id}_rows"
        nodo_cols = f"{nodo_id}_cols"
        cadena += f'"{nodo_rows}" [label="Rows: {self.rows}", shape=ellipse, color=lightblue];\n'
        cadena += f'"{nodo_cols}" [label="Cols: {self.cols}", shape=ellipse, color=lightblue];\n'
        cadena += f'"{nodo_id}" -> "{nodo_rows}";\n'
        cadena += f'"{nodo_id}" -> "{nodo_cols}";\n'

        # Nodos para los items
        nodo_items = f"{nodo_id}_items"
        cadena += f'"{nodo_items}" [label="Items", shape=ellipse, color=green];\n'
        cadena += f'"{nodo_id}" -> "{nodo_items}";\n'

        # recorriendo los items
        for c in range(1, self.cols + 1):
            prev_item = nodo_items
            for r in range(1, self.rows + 1):
                item = self.get_item(r, c)
                item_nodo_id = f"{nodo_id}_item_{r}_{c}"
                cadena += f'"{item_nodo_id}" [label="{item.text if item else "-"}", shape=ellipse];\n'
                
                # Conectando el nodo "Items" solo a los items de la primera fila
                if r == 1:
                    cadena += f'"{nodo_items}" -> "{item_nodo_id}";\n'
                
                # Conectando los demás items
                else:
                    cadena += f'"{prev_item}" -> "{item_nodo_id}";\n'
                    
                prev_item = item_nodo_id
        return cadena
        
        
    def showItemsConsole(self):
        for r in range(1, self.rows + 1):
            for c in range (1, self.cols + 1):
                item = self.get_item(r, c)
                if item:
                    print(item.text, end="\t")
                else:
                    print("-", end="\t")
            print()
            
            
    def to_xml(self): 
        cadena = f'<elemento nombre="{self.nombre}" id="{self.id}" cols="{self.cols}" rows="{self.rows}">\n'
        actual = self.items.inicio
        while actual:
            cadena += f'\t<item row="{actual.row}" col="{actual.col}">{actual.text}</item>\n'
            actual = actual.siguiente
        cadena += "</elemento>\n"
        return cadena
    
    
    def get_item(self, row, col):
        actual = self.items.inicio
        while actual: 
            if actual.row == row and actual.col == col:
                return actual
            actual = actual.siguiente
        return None
        
        
    