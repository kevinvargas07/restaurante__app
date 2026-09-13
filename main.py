import tkinter as tk
import os
from servicios import RestauranteServicio
from ui import LoginView, MainView

class AplicacionRestaurante:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Restaurante App - Semana 13")
        self.root.geometry("800x550")

        # Contenedor principal que se reutiliza para cada vista
        self.contenedor = tk.Frame(root)
        self.contenedor.pack(fill="both", expand=True)

        # Servicio único compartido entre vistas
        self.servicio = RestauranteServicio()

        # Iniciar con login
        self.mostrar_login()

    def _limpiar_contenedor(self) -> None:
        """Destruye todos los widgets hijos del contenedor."""
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_login(self) -> None:
        self._limpiar_contenedor()
        LoginView(self.contenedor, self.servicio, self.mostrar_main)

    def mostrar_main(self, usuario) -> None:
        self._limpiar_contenedor()
        MainView(self.contenedor, self.servicio, usuario, self.mostrar_login)


def main() -> None:
    os.makedirs("datos", exist_ok=True)
    root = tk.Tk()
    AplicacionRestaurante(root)
    root.mainloop()


if __name__ == "__main__":
    main()