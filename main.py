"""Punto de entrada principal del sistema restaurante_app."""

import tkinter as tk
import os
from servicios import RestauranteServicio
from ui import LoginView, MainView


class AplicacionRestaurante:
    """Aplicación principal del restaurante."""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Restaurante App - Semana 16")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Contenedor principal reutilizable
        self.contenedor = tk.Frame(root)
        self.contenedor.pack(fill="both", expand=True)
        
        # Servicio único compartido entre vistas
        self.servicio = RestauranteServicio()
        
        # Iniciar con login
        self.mostrar_login()
    
    def _limpiar_contenedor(self) -> None:
        """Destruye todos los widgets del contenedor."""
        for widget in self.contenedor.winfo_children():
            widget.destroy()
    
    def mostrar_login(self) -> None:
        """Muestra la vista de login."""
        self._limpiar_contenedor()
        LoginView(self.contenedor, self.servicio, self.mostrar_main)
    
    def mostrar_main(self, usuario) -> None:
        """Muestra la vista principal."""
        self._limpiar_contenedor()
        MainView(self.contenedor, self.servicio, usuario, self.mostrar_login)


def main() -> None:
    """Función principal del programa."""
    os.makedirs("datos", exist_ok=True)
    root = tk.Tk()
    AplicacionRestaurante(root)
    root.mainloop()


if __name__ == "__main__":
    main()