import tkinter as tk
from Vistas import VistaInicial, VistaSecundaria, VistaTerciaria, VistaQuarta, VistaQuinta
from tkinter import messagebox
import grpc
import Servicio_pb2
import Servicio_pb2_grpc
import pika
import threading
from queue import Queue

import yaml

class Client:
    def __init__(self, root, nombre, direccion_ip):
        self.root = root

        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        file.close()

        self.grpc_server_ip = config['grpc_server']['ip']
        self.grpc_server_port = config['grpc_server']['port']

        self.rabbit_ip = config['rabbit']['ip']

        self.root.resizable(False, False)
        self.nombre = nombre
        channel = grpc.insecure_channel(f'{self.grpc_server_ip}:{self.grpc_server_port}')
        stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
        print("Enviar Ip", direccion_ip)
        response = stub.InicioSesion(Servicio_pb2.Session(Nombre=nombre, IP=direccion_ip))
        print("Response received from server:", response.ok)

        # Crea la connexcion con RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(f'{self.rabbit_ip}', heartbeat=60))
        self.channelMQ = connection.channel()
        self.channelMQ.exchange_declare(exchange=f"Privado: {nombre}", exchange_type='fanout')
        result = self.channelMQ.queue_declare(queue=f"Privado: {nombre}", durable=True)
        self.channelMQ.basic_qos(prefetch_size=0)
        self.channelMQ.queue_bind(exchange=f"Privado: {nombre}", queue=f"Privado: {nombre}")

        self.chat_publicos = {}
        
        thread = threading.Thread(target=self.consume)
        thread.daemon = True
        thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.crearVistas()
        self.mostrar_vista_inicial()

    def consume(self):
        
        self.channelMQ.basic_consume(queue=f"Privado: {self.nombre}", on_message_callback=self.recibir_mensaje, auto_ack=True)
        self.channelMQ.start_consuming()

    def recibir_mensaje(self, ch, method, properties, body):
        try:
            print(f"{method.exchange}, {body.decode()}")
            
            if method.exchange == f"Privado: {self.nombre}":
                messagebox.showinfo("Insult Channel", body.decode())
                None
            elif method.exchange in self.chat_publicos:
                self.chat_publicos[method.exchange].put(body.decode())
            else: 
                self.chat_publicos[method.exchange] = Queue()
                self.chat_publicos[method.exchange].put(body.decode())
        except Exception:
            pass

    def crearVistas(self):
        self.crearVistaInicial()
        self.crearVistaSecundaria()
        self.vista_actual = None 

    def crearVistaInicial(self):
        vistas = (self.mostrar_vista_secundaria, self.mostrar_vista_terciaria, self.mostrar_vista_quarta, self.mostrar_vista_quinta)
        self.vista_inicial = VistaInicial(self.root, vistas, self.nombre)
        
    def crearVistaSecundaria(self):
        self.vista_secundaria = VistaSecundaria(self.root, self.mostrar_vista_inicial, self.nombre)
    
    def crearVistaTerciaria(self):
        self.vista_terciaria = VistaTerciaria(self.root, self.mostrar_vista_inicial, self.nombre, self.channelMQ, self.chat_publicos)

    def crearVistaQuarta(self):
        self.vista_quarta = VistaQuarta(self.root, self.mostrar_vista_inicial,  self.nombre, self.channelMQ, self.chat_publicos)

    def crearVistaQuinta(self):
        self.vista_quinta = VistaQuinta(self.root, self.mostrar_vista_inicial,  self.nombre, self.channelMQ)

    def mostrar_vista_inicial(self):
        if self.vista_actual:
            self.vista_actual.destroy() 

        self.crearVistaInicial()
        self.vista_inicial.pack(expand=True, fill=tk.BOTH)
        self.vista_actual = self.vista_inicial
        self.root.title("Menu")

    def mostrar_vista_secundaria(self):
        if self.vista_actual:
            self.vista_actual.destroy() 

        self.crearVistaSecundaria()

        self.vista_secundaria.pack(expand=True, fill=tk.BOTH)
        self.vista_actual = self.vista_secundaria
        self.root.title("Chat Privado")

    def mostrar_vista_terciaria(self):
        if self.vista_actual:
            self.vista_actual.destroy() 

        self.crearVistaTerciaria()

        self.vista_terciaria.pack(fill="both", expand=True)
        self.vista_actual = self.vista_terciaria
        self.root.title("Discover")

    def mostrar_vista_quarta(self):
        if self.vista_actual:
            self.vista_actual.destroy() 

        self.crearVistaQuarta()

        self.vista_quarta.pack(fill="both", expand=True)
        self.vista_actual = self.vista_quarta
        self.root.title("Chat Publico")

    def mostrar_vista_quinta(self):
        if self.vista_actual:
            self.vista_actual.destroy() 

        self.crearVistaQuinta()

        self.vista_quinta.pack(fill="both", expand=True)
        self.vista_actual = self.vista_quinta
        self.root.title("Insult Channel")

    def on_closing(self):
        channel = grpc.insecure_channel(f"{self.grpc_server_ip}:{self.grpc_server_port}")
        stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
        response = stub.CerrarSesion(Servicio_pb2.Session(Nombre=self.nombre, IP=''))

        self.root.destroy()