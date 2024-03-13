import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button, END

class ChatWindow:
    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.root.geometry("400x500")

        # Marco principal
        main_frame = tk.Frame(root)
        main_frame.pack(expand=True, fill="both")

        # Área de chat (estado 'disabled' para que sea solo de lectura)
        self.chat_area = Text(main_frame, wrap="word", height=20, width=50, state='disabled')
        self.chat_area.pack(side="left", expand=True, fill="both")

        # Barra de desplazamiento para el área de chat
        scrollbar = Scrollbar(main_frame, command=self.chat_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_area.config(yscrollcommand=scrollbar.set)

        # Entrada de texto para escribir mensajes
        self.input_entry = Entry(root, width=50)
        self.input_entry.pack(pady=10)

        # Botón para enviar mensajes
        send_button = Button(root, text="Enviar", command=self.send_message)
        send_button.pack()

        # Vincular la tecla "Enter" a la función send_message
        self.input_entry.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        message = self.input_entry.get()
        if message:
            self.chat_area.config(state='normal')  # Habilitar el área de chat para escribir
            self.chat_area.insert(END, f"You: {message}\n")
            self.chat_area.yview(END)
            self.chat_area.config(state='disabled')  # Deshabilitar el área de chat después de escribir
            self.input_entry.delete(0, "end")
    
    def receive_message(self, sender, message):
        self.chat_area.config(state='normal')  # Habilitar el área de chat para escribir
        self.chat_area.insert(END, f"{sender}: {message}\n")
        self.chat_area.yview(END)
        self.chat_area.config(state='disabled')  # Deshabilitar el área de chat después de escribir
