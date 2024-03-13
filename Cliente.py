import tkinter as tk
from Vistas import VistaInicial, VistaSecundaria

class Client:
    def __init__(self, root):
        self.root = root
        self.vista_inicial = VistaInicial(root, self.mostrar_vista_secundaria)
        self.vista_secundaria = VistaSecundaria(root, self.mostrar_vista_inicial)

        self.vista_actual = None  # Almacena la vista actual

        self.mostrar_vista_inicial()

    def mostrar_vista_inicial(self):
        if self.vista_actual:
            self.vista_actual.pack_forget()  # Oculta la vista actual en lugar de destruirla

        self.vista_inicial.pack(expand=True, fill=tk.BOTH)
        self.vista_actual = self.vista_inicial

    def mostrar_vista_secundaria(self):
        if self.vista_actual:
            self.vista_actual.pack_forget()  # Oculta la vista actual en lugar de destruirla

        self.vista_secundaria.pack(expand=True, fill=tk.BOTH)
        self.vista_actual = self.vista_secundaria

if __name__ == "__main__":
    root = tk.Tk()
    app = Client(root)
    root.mainloop()
