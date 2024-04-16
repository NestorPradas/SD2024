import tkinter as tk
from tkinter import ttk
from ChatWindow import ChatWindowMQ

import pika
from queue import Queue
import socket
import grpc
import Servicio_pb2
import Servicio_pb2_grpc
import threading
import requests

class VistaInicial(tk.Frame):
    def __init__(self, master, vista, NombreCliente):
        tk.Frame.__init__(self, master)
        master.geometry("400x500")
        master.resizable(False, False)
        self.nombre = NombreCliente
        alto_boton = int(master.winfo_screenheight() * 0.25)
        boton1 = tk.Button(self, text=f"Iniciar Chat Privado", command=vista[0], height=alto_boton, width=400)
        boton2 = tk.Button(self, text=f"Iniciar Chat Publico", command=vista[2], height=alto_boton, width=400)
        boton3 = tk.Button(self, text=f"Descubrir", command=vista[1], height=alto_boton, width=400)
        boton4 = tk.Button(self, text=f"Botón 4", command=vista[0], height=alto_boton, width=400)
        
        boton1.grid(row=0, column=0, sticky="nsew")
        boton2.grid(row=1, column=0, sticky="nsew")
        boton3.grid(row=2, column=0, sticky="nsew")
        boton4.grid(row=3, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        channel = grpc.insecure_channel("10.10.1.54:50051")
        stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
        response = stub.CerrarSesion(Servicio_pb2.Session(Nombre=self.nombre, IP=''))

        self.master.destroy()

# Chat privado
class VistaSecundaria(tk.Frame):
    def __init__(self, master, volver_vista_inicial, NombreCliente):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.geometry("400x500")
        self.master.resizable(False, False)

        self.nombre = NombreCliente

        boton_volver_atras = tk.Button(self, text="Volver a la Vista Inicial", command=volver_vista_inicial)
        boton_volver_atras.place(x=10, y=10)

        self.entry_texto = tk.Entry(self)
        self.entry_texto.place(relx=0.5, rely=0.4, anchor="center")

        boton_imprimir = tk.Button(self, text="Conexion a cliente", command=self.imprimir_texto)
        boton_imprimir.place(relx=0.5, rely=0.5, anchor="center")

        self.entry_texto.bind("<Return>", lambda event: self.imprimir_texto())

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        channel = grpc.insecure_channel("10.10.1.54:50051")
        stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
        response = stub.CerrarSesion(Servicio_pb2.Session(Nombre=self.nombre, IP=''))

        self.master.destroy()

    def obtener_ip(self):
        try:
            host_name = socket.gethostname()
            direccion_ip = socket.gethostbyname(host_name)
            return str(direccion_ip)
        except Exception as e:
            print("Error al obtener la dirección IP:", e)

    def imprimir_texto(self):

        texto = self.entry_texto.get()
        
        if texto:
            print(f"Texto introducido: {texto}")
            channel1 = grpc.insecure_channel('10.10.1.54:50051') ## servidor central
            stub1 = Servicio_pb2_grpc.ClienteServidorStub(channel1)

            response = stub1.SolicitarConexion(Servicio_pb2.Conectar(NombreSolicitante=self.nombre, NombreSolicitado=texto))
            print("Response received from server:", response)

            channel2 = grpc.insecure_channel(str(self.obtener_ip())+':50050') ## mi servidor
            stub = Servicio_pb2_grpc.ServidorServidorStub(channel2)
            response2 = stub.SolicitarConexionServidor(Servicio_pb2.Session(Nombre=texto, IP=response.IP)) 
            print("Respuesta de mi servidor: ", response2)

        self.entry_texto.delete(0, tk.END)

# Discover
class VistaTerciaria(tk.Frame):
    def __init__(self, root, vista_inicial, nombre, conexionMQ, chat_publicos):
        tk.Frame.__init__(self, root)
        root.resizable(False, False)
        self.nombre = nombre
        self.root = root
        self.root.geometry("400x500")
        self.root.title("Vista 3")

        self.vista_inicial = vista_inicial

        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)  
        self.grid_columnconfigure(0, weight=1)

        boton_volver = tk.Button(self, text="Volver", command=self.volver_a_principal)
        boton_volver.grid(row=0, column=0, sticky="nsew")

        self.grid_columnconfigure(1, weight=1)

        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=1, column=0, columnspan=2, sticky="nsew")  

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=1, column=2, sticky="ns")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame_contenedor = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_contenedor, anchor="nw")

        array_exchanges = self.pedir_exchanges()

        self.chat_publicos = chat_publicos
        self.conexionMQ = conexionMQ

        fila = 1
        for i in array_exchanges:
            self.agregar_fila(fila, f"{i}")
            fila += 1

        # Pedir informacion a RabbitMQ y añadirla en pantalla como "Publico:"

        self.frame_contenedor.columnconfigure(0, weight=10)

        self.frame_contenedor.bind("<Configure>", self.on_configure)

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        texto_superior = tk.Label(self, text="Texto Encima del Canvas", font=("Arial", 12))
        texto_superior.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=8)

    def on_closing(self):
        channel = grpc.insecure_channel("10.10.1.54:50051")
        stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
        response = stub.CerrarSesion(Servicio_pb2.Session(Nombre=self.nombre, IP=''))

        self.root.destroy()

    def pedir_exchanges(self):
        
        username = 'guest'
        password = 'guest'
        host = '10.10.1.54'
        port = '15672'  # Puerto para la API de RabbitMQ

        url = f'http://{host}:{port}/api/exchanges'

        # Realizar la solicitud HTTP
        response_exchanges = requests.get(url, auth=(username, password))

        array = []

        if response_exchanges.status_code == 200:
            exchanges = response_exchanges.json()
            for exchange in exchanges:
                if not exchange['name'].startswith("amq."):
                    if exchange['name'] != "":
                        array.append(exchange["name"])
        else:
            print("Error al obtener la lista de exchanges:", response_exchanges.status_code)
        
        return array
    
    def obtener_ip(self):
        try:
            host_name = socket.gethostname()
            direccion_ip = socket.gethostbyname(host_name)
            return str(direccion_ip)
        except Exception as e:
            print("Error al obtener la dirección IP:", e)

    def agregar_fila(self, numero_fila, dato):
        label_dato = tk.Label(self.frame_contenedor, text=dato)
        label_dato.grid(row=numero_fila - 1, column=0, sticky="nsew")
        label_dato.bind("<Button-1>", lambda event, value=dato: self.on_clic(value))

    def on_clic(self, valor : str):
        print("Dato clicado:", valor)
        tipo, nombreConexion = valor.split()
        if tipo == "Privado:":
            channel1 = grpc.insecure_channel('10.10.1.54:50051') ## servidor central
            stub1 = Servicio_pb2_grpc.ClienteServidorStub(channel1)

            response = stub1.SolicitarConexion(Servicio_pb2.Conectar(NombreSolicitante=self.nombre, NombreSolicitado=nombreConexion))
            print("Response received from server:", response)

            channel2 = grpc.insecure_channel(str(self.obtener_ip())+':50050') ## mi servidor
            stub = Servicio_pb2_grpc.ServidorServidorStub(channel2)
            response2 = stub.SolicitarConexionServidor(Servicio_pb2.Session(Nombre=nombreConexion, IP=response.IP)) 
            print("Respuesta de mi servidor: ", response2)
        elif tipo == "Publico:": 
            # RabbitMQ
            if f"{valor}" not in self.chat_publicos:
                self.chat_publicos[f"{valor}"] = Queue()
            try:
                self.conexionMQ.queue_bind(exchange=f"{valor}", queue=f"Privado: {self.nombre}")
            except Exception:
                print("Error al conectar con el servidor")

            chat_window = ChatWindowMQ(self.nombre, nombreConexion, self.chat_publicos[f"{valor}"])
            chat_window.start()

    def volver_a_principal(self):
        self.vista_inicial()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        if event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        else:
            pos = self.canvas.canvasy(0)
            if pos > 0:
                self.canvas.yview_scroll(-1, "units")

# Chat publico
class VistaQuarta(tk.Frame):
    def __init__(self, master, volver_vista_inicial, NombreCliente, conexionMQ, chat_publicos):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.geometry("400x500")
        self.master.resizable(False, False)

        self.conexionMQ = conexionMQ
        self.chat_publicos = chat_publicos
        self.nombre = NombreCliente

        boton_volver_atras = tk.Button(self, text="Volver a la Vista Inicial", command=volver_vista_inicial)
        boton_volver_atras.place(x=10, y=10)

        self.entry_texto = tk.Entry(self)
        self.entry_texto.place(relx=0.5, rely=0.4, anchor="center")

        boton_imprimir = tk.Button(self, text="Conexion a cliente", command=self.imprimir_texto)
        boton_imprimir.place(relx=0.5, rely=0.5, anchor="center")

        self.entry_texto.bind("<Return>", lambda event: self.imprimir_texto())

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        channel = grpc.insecure_channel("10.10.1.54:50051")
        stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
        response = stub.CerrarSesion(Servicio_pb2.Session(Nombre=self.nombre, IP=''))

        self.master.destroy()

    def recibir_mensaje(self, ch, method, properties, body):
        try:
            if method.exchange:
                print(f"[VistaCliente] {method.exchange}, {body.decode()} ")
                self.chat_publicos[method.exchange].put(body.decode())
        except Exception:
            pass

    def consume(self):
        self.conexionMQ.basic_consume(queue=f"Privado: {self.nombre}", on_message_callback=self.recibir_mensaje, auto_ack=True)
        print(f"[Vistas] reiniciando consume")
        self.conexionMQ.start_consuming()

    def reiniciar_consume(self):
        thread = threading.Thread(target=self.consume)
        thread.daemon = True
        thread.start()

    def obtener_ip(self):
        try:
            host_name = socket.gethostname()
            direccion_ip = socket.gethostbyname(host_name)
            return str(direccion_ip)
        except Exception as e:
            print("Error al obtener la dirección IP:", e)

    def imprimir_texto(self):

        texto = self.entry_texto.get()
        
        if texto:
            
            if f"Publico: {texto}" not in self.chat_publicos:
                self.chat_publicos[f"Publico: {texto}"] = Queue()
            # crear exchange
            self.conexionMQ.exchange_declare(exchange=f"Publico: {texto}", exchange_type='fanout')
            
            # añadir exchange a la queue, si no esta
            try:
                self.conexionMQ.queue_bind(exchange=f"Publico: {texto}", queue=f"Privado: {self.nombre}")
            except Exception:
                connection = pika.BlockingConnection(pika.ConnectionParameters('10.10.1.54'))
                self.conexionMQ = connection.channel()
                result = self.conexionMQ.queue_declare(queue=f"Privado: {self.nombre}", exclusive=True)
                self.conexionMQ.queue_bind(exchange=f"Privado: {self.nombre}", queue=f"Privado: {self.nombre}")
                for name, _ in self.chat_publicos.items():
                    self.conexionMQ.queue_bind(exchange=name, queue=f"Privado: {self.nombre}")
                self.reiniciar_consume()

            # abrir ChatWindowMQ
                
            chat_window = ChatWindowMQ(self.nombre, texto, self.chat_publicos[f"Publico: {texto}"])
            chat_window.start()

        self.entry_texto.delete(0, tk.END)
