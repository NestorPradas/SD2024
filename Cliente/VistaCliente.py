import tkinter as tk
from Vistas import VistaInicial, VistaSecundaria

import grpc
import Servicio_pb2
import Servicio_pb2_grpc

import socket

class Client:
    def __init__(self, root, nombre):
        self.root = root
        self.vista_inicial = VistaInicial(root, self.mostrar_vista_secundaria, nombre)
        self.vista_secundaria = VistaSecundaria(root, self.mostrar_vista_inicial, nombre)

        self.vista_actual = None  # Almacena la vista actual

        channel = grpc.insecure_channel('localhost:50051')
        stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
        direccion_ip = self.obtener_ip()
        print("Enviar Ip", direccion_ip)
        response = stub.InicioSesion(Servicio_pb2.Session(Nombre=nombre, IP=str(direccion_ip)))
        print("Response received from server:", response.ok)

        self.mostrar_vista_inicial()

    def mostrar_vista_inicial(self):
        if self.vista_actual:
            self.vista_actual.pack_forget()  # Oculta la vista actual en lugar de destruirla

        self.vista_inicial.pack(expand=True, fill=tk.BOTH)
        self.vista_actual = self.vista_inicial
        self.root.title("Menu")

    def obtener_ip(self):
        try:
            # Obtener el nombre del host local
            host_name = socket.gethostname()
            # Obtener la dirección IP asociada al nombre del host
            direccion_ip = socket.gethostbyname(host_name)
            return direccion_ip
        except Exception as e:
            print("Error al obtener la dirección IP:", e)

    def mostrar_vista_secundaria(self):
        if self.vista_actual:
            self.vista_actual.pack_forget()  # Oculta la vista actual en lugar de destruirla

        self.vista_secundaria.pack(expand=True, fill=tk.BOTH)
        self.vista_actual = self.vista_secundaria
        self.root.title("Chat Privado")

if __name__ == "__main__":
    root = tk.Tk()
    app = Client(root, nombre="Cliente1")
    root.mainloop()
