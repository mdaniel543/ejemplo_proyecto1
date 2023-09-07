import xml.etree.ElementTree as ET

import os
from ListaDoble import ListaDoble
from Elemento import Elemento
from Item import Item

import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage

elementos = ListaDoble()

def carga_datos(ruta):
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
    
    

       
class App:
    def __init__(self, master):
        self.master = master
        self.master.title('Menú Principal')

        # Definiendo el tamaño de la ventana y centrándola en la pantalla
        window_width = 1280
        window_height = 720
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = (screen_width/2) - (window_width/2)
        y_coordinate = (screen_height/2) - (window_height/2)
        self.master.geometry(f'{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}')

        self.master.configure(bg='black')

        style_settings = {
            "bg": "lightgray",
            "fg": "black",
            "padx": 10,
            "pady": 5,
            "font": ("Helvetica", 10)
        }

        # Botones y widgets
        self.load_btn = tk.Button(master, text='Cargar datos', command=self.carga_datos_gui, **style_settings)
        self.load_btn.pack(pady=5)  # El padding 'pady' añade espacio entre los botones

        self.graph_btn = tk.Button(master, text='Buscar y generar imagen', command=self.search_and_graph, **style_settings)
        self.graph_btn.pack(pady=5)

        self.delete_btn = tk.Button(master, text='Eliminar elemento', command=lambda: self.eliminar(self.prompt_choice("Escoge un ID")), **style_settings)
        self.delete_btn.pack(pady=5)
        
        self.update_btn = tk.Button(master, text='Actualizar elemento', command=lambda: self.actualizar(self.prompt_choice("Escoge un ID"), self.prompt_choice("Escribe el nuevo nombre")), **style_settings)
        self.update_btn.pack(pady=5)
        
        # Inicializando el label
        self.elements_label = tk.Label(master, text="", **style_settings)
        self.elements_label.pack(pady=5)
        
        #imagen
        self.canvas = tk.Canvas(master, width=920, height=540, bg='black', scrollregion=(0,0,1000,1000))
        self.canvas.pack(side=tk.LEFT, pady=5)
        
        self.scroll_y = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side=tk.LEFT, fill="y")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        
        self.image_label = tk.Label(self.canvas, bg='black')
        self.canvas.create_window((0,0), window=self.image_label, anchor="nw")
        
        self.image_label.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
    def carga_datos_gui(self):
        filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filepath:
            carga_datos(filepath)
            messagebox.showinfo("Carga exitosa", "Los datos se han cargado exitosamente")
            self.show_elements()

    def show_elements(self):
        print(elementos.mostrar())
        self.elements_label.config(text=str(elementos.mostrar()))

    def search_and_graph(self):
        chosen_id = self.prompt_choice("Escoge un ID",)
        if chosen_id:
            elemento = elementos.buscar_por_id(chosen_id)
            if elemento:
                graficar(elemento)
                messagebox.showinfo("Gráfica generada", "La gráfica se ha generado exitosamente")
                # Cargando y mostrando la imagen
                img = PhotoImage(file='matriz.png')
                self.image_label.config(image=img)
                self.image_label.image = img  
            else:
                messagebox.showerror("Error", f"El elemento con ID {chosen_id} no existe")
                

    def prompt_choice(self, msg):
        # Una función para solicitar una elección al usuario
        choice = tk.simpledialog.askstring("Input", msg, parent=self.master)
        return choice
    
    def eliminar(self, id_val):
        if elementos.eliminar(id_val):
            messagebox.showinfo("Eliminado", f"El elemento con ID {id_val} ha sido eliminado")
            #limpiar la imagen y generar de nuevo el label1
            self.image_label.config(image=None)
            self.image_label.image = None
            self.show_elements()
        else:
            messagebox.showerror("Error", f"El elemento con ID {id_val} no existe")

    def actualizar(self, id_val, nuevo_nombre):
        if elementos.actualizar(id_val, nuevo_nombre):
            messagebox.showinfo("Actualizado", f"El elemento con ID {id_val} ha sido actualizado")
            self.show_elements()
            self.image_label.config(image=None)
            self.image_label.image = None
        else:
            messagebox.showerror("Error", f"El elemento con ID {id_val} no existe")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()

