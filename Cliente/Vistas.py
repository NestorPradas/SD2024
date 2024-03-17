import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from ChatWindow import ChatWindow

import grpc
import Servicio_pb2
import Servicio_pb2_grpc

class VistaInicial(tk.Frame):
    def __init__(self, master, vista_secundaria, NombreCliente):
        tk.Frame.__init__(self, master)
        master.geometry("400x500")
        self.nombre = NombreCliente
        alto_boton = int(master.winfo_screenheight() * 0.25)
        boton1 = tk.Button(self, text=f"Botón 1", command=vista_secundaria, height=alto_boton, width=400)
        boton2 = tk.Button(self, text=f"Botón 2", command=vista_secundaria, height=alto_boton, width=400)
        boton3 = tk.Button(self, text=f"Botón 3", command=self.mostrar_lista, height=alto_boton, width=400)
        boton4 = tk.Button(self, text=f"Botón 4", command=vista_secundaria, height=alto_boton, width=400)
        
        boton1.grid(row=0, column=0, sticky="nsew")
        boton2.grid(row=1, column=0, sticky="nsew")
        boton3.grid(row=2, column=0, sticky="nsew")
        boton4.grid(row=3, column=0, sticky="nsew")

        # Configurar el layout de la ventana para que los botones se expandan con ella
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def mostrar_lista(self):
        nueva_ventana = Toplevel(self.master)
        vistaterciaria = VistaTerciaria(nueva_ventana)

class VistaSecundaria(tk.Frame):
    def __init__(self, master, volver_vista_inicial, NombreCliente):
        tk.Frame.__init__(self, master)
        master.geometry("400x500")

        self.nombre = NombreCliente

        # Botón para volver a la Vista Inicial en la parte superior izquierda
        boton_volver_atras = tk.Button(self, text="Volver a la Vista Inicial", command=volver_vista_inicial)
        boton_volver_atras.place(x=10, y=10)

        # Barra para introducir texto en el centro
        self.entry_texto = tk.Entry(self)
        self.entry_texto.place(relx=0.5, rely=0.4, anchor="center")

        # Botón para imprimir el texto y borrarlo, posicionado en el centro
        boton_imprimir = tk.Button(self, text="Conexion a cliente", command=self.imprimir_texto)
        boton_imprimir.place(relx=0.5, rely=0.5, anchor="center")

        # Enlace de la tecla "Enter" con la función imprimir_texto
        self.entry_texto.bind("<Return>", lambda event: self.imprimir_texto())

    def imprimir_texto(self):
        ##Funcion que pide conectarse

        texto = self.entry_texto.get()
        
        if texto:
        #nueva_ventana = Toplevel(self.master)
        #chat_window = ChatWindow(nueva_ventana, "Chat Window")
        # Conectarse al servidor
            print(f"Texto introducido: {texto}")
            channel1 = grpc.insecure_channel('localhost:50051') ## servidor central
            stub1 = Servicio_pb2_grpc.ClienteServidorStub(channel1)

            response = stub1.SolicitarConexion(Servicio_pb2.Conectar(NombreSolicitante=self.nombre, NombreSolicitado=texto))
            print("Response received from server:", response)
        
        # Borra el texto después de imprimirlo
        self.entry_texto.delete(0, tk.END)

class VistaTerciaria:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x500")
        self.root.title("Vista 3")

        # Configurar el gestor de geometría para la ventana
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=50)

        # Agregar un botón en la esquina superior izquierda
        boton_volver = tk.Button(root, text="Volver", command=self.volver_a_principal)
        boton_volver.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=2)  # 20% del ancho

        # Crear un lienzo (canvas) con barra de desplazamiento
        self.canvas = tk.Canvas(root)
        self.canvas.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Contenedor para los elementos
        self.frame_contenedor = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_contenedor, anchor="nw")

        # Agregar 16 valores a la columna
        for i in range(1, 17):
            self.agregar_fila(i, f"Dato {i}")

        # Configurar el gestor de geometría para el contenedor
        self.frame_contenedor.columnconfigure(0, weight=1)

        # Configurar el evento de desplazamiento del canvas
        self.frame_contenedor.bind("<Configure>", self.on_configure)

        # Hacer que el canvas sea desplazable con la rueda del ratón
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Agregar un texto encima del canvas
        texto_superior = tk.Label(root, text="Texto Encima del Canvas", font=("Arial", 12))
        texto_superior.grid(row=0, column=1, sticky="nsew")
        self.root.columnconfigure(1, weight=8)  # 80% del ancho

    def agregar_fila(self, numero_fila, dato):
        # Mostrar los datos en la columna respectiva
        label_dato = tk.Label(self.frame_contenedor, text=dato)
        label_dato.grid(row=numero_fila - 1, column=0, sticky="ew")
        label_dato.bind("<Button-1>", lambda event, value=dato: self.on_clic(value))

    def on_clic(self, valor):
        print("Dato clicado:", valor)
        
        nueva_ventana = Toplevel(self.root) 
        chat_window = ChatWindow(nueva_ventana, str(valor))
        

    def on_boton_clic(self):
        print("Botón clicado")

    def volver_a_principal(self):
        # Cerrar la ventana de la aplicación y llamar al callback para mostrar la ventana principal
        self.root.destroy()
        self.callback_volver()

    def on_configure(self, event):
        # Actualizar la región desplazable del canvas cuando cambia el tamaño del contenedor
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        # Desplazar el canvas con la rueda del ratón
        if event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        else:
            pos = self.canvas.canvasy(0)
            if pos > 0:
                self.canvas.yview_scroll(-1, "units")

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaTerciaria(root)
    root.mainloop()