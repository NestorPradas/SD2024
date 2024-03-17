import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button, END
import threading
import time
from queue import Queue
import grpc
import Servicio_pb2
import Servicio_pb2_grpc

## implementar envio mensaje a ip pasada por parametro

class ChatWindow(threading.Thread, Servicio_pb2_grpc.ClienteServidor):
    def __init__(self, minombre, nombre, message_queue, IP):
        super().__init__()
        self.message_queue = message_queue
        self.Ip = IP + ":50050"
        self.NombreConectado = nombre
        self.minombre = minombre
        self.running = True

    def run(self):
        self.start_gui_loop()

    def start_gui_loop(self):
        self.root = tk.Tk()
        self.root.title("Chat de " + self.NombreConectado)
        self.root.geometry("400x500")

        # Marco principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both")

        # Área de chat (estado 'disabled' para que sea solo de lectura)
        self.chat_area = Text(main_frame, wrap="word", height=20, width=50, state='disabled')
        self.chat_area.pack(side="left", expand=True, fill="both")

        # Barra de desplazamiento para el área de chat
        scrollbar = Scrollbar(main_frame, command=self.chat_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_area.config(yscrollcommand=scrollbar.set)

        # Entrada de texto para escribir mensajes
        self.input_entry = Entry(self.root, width=50)
        self.input_entry.pack(pady=10)

        # Botón para enviar mensajes
        send_button = Button(self.root, text="Enviar", command=self.send_message)
        send_button.pack()

        # Vincular la tecla "Enter" a la función send_message
        self.input_entry.bind("<Return>", lambda event: self.send_message())

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start a separate thread to check for new messages
        self.thread = threading.Thread(target=self.check_messages)
        self.thread.daemon = True
        self.thread.start()
        self.root.mainloop()

    def check_messages(self):
        while self.running:
            try:
                # Get the message from the queue
                message = self.message_queue.get()
                if message:
                    # Update the chat area with the new message
                    self.update_chat_area(message)
            except Exception:
                pass
            # Sleep for a short duration to avoid high CPU usage
            time.sleep(0.1)

    def update_chat_area(self, message):
        # Enable the chat area for writing, update, and disable it again
        self.chat_area.config(state='normal')
        self.chat_area.insert(END, f"{self.NombreConectado}: {message}\n")
        self.chat_area.yview(END)
        self.chat_area.config(state='disabled')

    def send_message(self):
        message = self.input_entry.get()
        if message:
            channel = grpc.insecure_channel(self.Ip)
            stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
            response = stub.EnvioMensaje(Servicio_pb2.Mensaje(NombreRemitente=self.minombre, MensajeRemitente=message))
            print("Respuesta del cliente: ", response.ok)
            self.chat_area.config(state='normal')  # Habilitar el área de chat para escribir
            self.chat_area.insert(END, f"Me: {message}\n")
            self.chat_area.yview(END)
            self.chat_area.config(state='disabled')  # Deshabilitar el área de chat después de escribir
            self.input_entry.delete(0, "end")

    def on_closing(self):
        channel = grpc.insecure_channel(self.Ip)
        stub = Servicio_pb2_grpc.ClienteServidorStub(channel)
        response = stub.CerrarSesion(Servicio_pb2.Session(Nombre=self.minombre, IP=''))
        print("Respuesta del cliente: ", response.ok)
        
        self.running = False  # Establecer la bandera para salir del bucle
        self.root.destroy()   # Destruir la ventana principal

    def close(self):
        self.running = False  # Establecer la bandera para salir del bucle
        self.root.destroy()   # Destruir la ventana principal

if __name__ == "__main__":
    message_queue = Queue()

    chat_window = ChatWindow(message_queue)
    chat_window.start()
    
    time.sleep(0.1)
    chat_window.join()
