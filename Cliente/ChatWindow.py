import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button, END
import threading
import time
from queue import Queue
import grpc
import Servicio_pb2
import Servicio_pb2_grpc
import socket
import pika

class ChatWindowGRPC(threading.Thread, Servicio_pb2_grpc.ClienteServidor):
    def __init__(self, minombre, nombre, message_queue, IP):
        super().__init__()
        self.message_queue = message_queue
        self.Ip = IP + ":50050"
        self.NombreConectado = nombre
        self.minombre = minombre
        self.running = True
        self.conectado = True

    def run(self):
        self.start_gui_loop()

    def start_gui_loop(self):
        self.root = tk.Tk()
        self.root.title("Chat de " + self.NombreConectado)
        self.root.geometry("400x500")

        self.root.resizable(False, False)

        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both")

        self.chat_area = Text(main_frame, wrap="word", height=20, width=50, state='disabled')
        self.chat_area.pack(side="left", expand=True, fill="both")

        scrollbar = Scrollbar(main_frame, command=self.chat_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_area.config(yscrollcommand=scrollbar.set)

        self.input_entry = Entry(self.root, width=50)
        self.input_entry.pack(pady=10)

        send_button = Button(self.root, text="Enviar", command=self.send_message)
        send_button.pack()

        self.input_entry.bind("<Return>", lambda event: self.send_message())

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.thread = threading.Thread(target=self.check_messages)
        self.thread.daemon = True
        self.thread.start()
        self.root.mainloop()

    def check_messages(self):
        while self.running:
            try:
                message = self.message_queue.get()
                if message:
                    self.update_chat_area(message)
            except Exception:
                pass
            time.sleep(0.1)

    def update_chat_area(self, message):
        if  not self.conectado:
            self.chat_area.config(state='normal')
            self.chat_area.insert(END, f"{self.NombreConectado} ha cerrado la conexion\n")
            self.chat_area.yview(END)
            self.chat_area.config(state='disabled')
            self.running = False
        else:
            self.chat_area.config(state='normal')
            self.chat_area.insert(END, f"{self.NombreConectado}: {message}\n")
            self.chat_area.yview(END)
            self.chat_area.config(state='disabled')

    def send_message(self):
        message = self.input_entry.get()
        if message and self.conectado: 
            channel = grpc.insecure_channel(self.Ip)
            stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
            response = stub.EnvioMensaje(Servicio_pb2.Mensaje(NombreRemitente=self.minombre, MensajeRemitente=message))
            self.chat_area.config(state='normal') 
            self.chat_area.insert(END, f"Me: {message}\n")
            self.chat_area.yview(END)
            self.chat_area.config(state='disabled') 
            self.input_entry.delete(0, "end")

    def obtener_ip(self):
        try:
            host_name = socket.gethostname()
            direccion_ip = socket.gethostbyname(host_name)
            return str(direccion_ip)
        except Exception as e:
            print("Error al obtener la dirección IP:", e)

    def on_closing(self):
        if self.conectado:
            channel = grpc.insecure_channel(self.Ip)
            stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
            response = stub.CerrarSesion(Servicio_pb2.Session(Nombre=self.minombre, IP=''))

        self.running = False  
        self.root.destroy()

class ChatWindowMQ(threading.Thread):
    def __init__(self, minombre, nombre, message_queue):
        super().__init__()
        self.message_queue = message_queue
        self.NombreConectado = nombre
        self.minombre = minombre
        self.running = True
        self.conectado = True
        
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.10.1.54'))
        self.channel = connection.channel()

    def run(self):
        self.start_gui_loop()

    def start_gui_loop(self):
        self.root = tk.Tk()
        self.root.title("Chat de " + self.NombreConectado)
        self.root.geometry("400x500")

        self.root.resizable(False, False)

        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both")

        self.chat_area = Text(main_frame, wrap="word", height=20, width=50, state='disabled')
        self.chat_area.pack(side="left", expand=True, fill="both")

        scrollbar = Scrollbar(main_frame, command=self.chat_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_area.config(yscrollcommand=scrollbar.set)

        self.input_entry = Entry(self.root, width=50)
        self.input_entry.pack(pady=10)

        send_button = Button(self.root, text="Enviar", command=self.send_message)
        send_button.pack()

        self.input_entry.bind("<Return>", lambda event: self.send_message())

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.channel.basic_publish(exchange=f"Publico: {self.NombreConectado}", routing_key='', body=f"{self.minombre} se ha conectado al chat")

        self.thread = threading.Thread(target=self.check_messages)
        self.thread.daemon = True
        self.thread.start()
        self.root.mainloop()

    def check_messages(self):
        while self.running:
            try:
                message = self.message_queue.get()
                if message:
                    self.update_chat_area(message)
            except Exception:
                pass
            time.sleep(0.1)

    def update_chat_area(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(END, f"{message}\n")
        self.chat_area.yview(END)
        self.chat_area.config(state='disabled')

    def send_message(self):
        message = self.input_entry.get()
        if message and self.conectado: 
            # enviar mensaje al exchange f"Publico: {self.nombreconectado}"
            self.channel.basic_publish(exchange=f"Publico: {self.NombreConectado}", routing_key='', body=f"{self.minombre}: {message}")
            # con mi nombre delante
            self.input_entry.delete(0, "end")
            None

    def on_closing(self):
        self.channel.basic_publish(exchange=f"Publico: {self.NombreConectado}", routing_key='', body=f"{self.minombre} ha salido del chat")
        self.running = False  
        self.root.destroy()

if __name__ == "__main__":
    message_queue = Queue()

    chat_window = ChatWindowGRPC("nestor", "nestor", message_queue, "10.10.1.54")
    chat_window.start()
    
    time.sleep(0.1)
    chat_window.join()
