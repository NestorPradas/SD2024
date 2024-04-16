from ServidorCliente import serve
from inicio import VentanaConexion
from VistaCliente import Client
import socket
import tkinter as tk
import threading

def obtener_ip():
    try:
        host_name = socket.gethostname()
        direccion_ip = socket.gethostbyname(host_name)
        return str(direccion_ip)
    except Exception as e:
        print("Error al obtener la dirección IP:", e)

def start_client_server():
    serve(obtener_ip(), ventana_conexion.nombre)
        

ventana_conexion = VentanaConexion()
ventana_conexion.iniciar()
if ventana_conexion.nombre != "":
    thread = threading.Thread(target=start_client_server)
    thread.daemon = True
    thread.start()

    root = tk.Tk()
    app = Client(root, nombre=ventana_conexion.nombre, direccion_ip=obtener_ip())
    root.mainloop()