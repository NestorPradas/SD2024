import tkinter as tk

class VentanaConexion:
    def __init__(self):
        self.nombre = ''
        self.ventana = tk.Tk()
        self.ventana.title("Ventana de Conexión")
        self.ventana.geometry("400x500")

        self.ventana.resizable(False, False)

        self.etiqueta_nombre = tk.Label(self.ventana, text="Tu nombre:")
        self.etiqueta_nombre.place(relx=0.3, rely=0.4, anchor=tk.CENTER)

        self.nombre_entry = tk.Entry(self.ventana)
        self.nombre_entry.place(relx=0.55, rely=0.4, anchor=tk.CENTER)
        self.nombre_entry.bind('<Return>', self.conectar)

        self.boton_conectar = tk.Button(self.ventana, text="Conectar", command=self.conectar)
        self.boton_conectar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def conectar(self, event=None):
        # Comprobar si ya existe el cliente mediante GRPC ¿?

        self.nombre = self.nombre_entry.get()
        self.ventana.destroy()

    def iniciar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    ventana_conexion = VentanaConexion()
    ventana_conexion.iniciar()
