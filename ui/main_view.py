import tkinter as tk
from tkinter import messagebox, ttk
from servicios import RestauranteServicio
from modelos import Usuario

class MainView:
    def __init__(self, contenedor: tk.Frame, servicio: RestauranteServicio,
                 usuario: Usuario, al_cerrar_sesion):
        self.contenedor = contenedor
        self.servicio = servicio
        self.usuario = usuario
        self.al_cerrar_sesion = al_cerrar_sesion
        self.frame = tk.Frame(contenedor)
        self.frame.pack(fill="both", expand=True)
        self._construir()

    def _construir(self) -> None:
        # Encabezado
        encabezado = tk.Frame(self.frame, bg="#333333")
        encabezado.pack(fill="x")

        tk.Label(encabezado, text="🍽️ Panel Principal", font=("Arial", 16, "bold"),
                 bg="#333333", fg="white").pack(side="left", padx=15, pady=10)

        tk.Label(encabezado, text=f"Bienvenido, {self.usuario.nombre}",
                 font=("Arial", 11), bg="#333333", fg="white").pack(side="left", padx=15)

        tk.Button(encabezado, text="Cerrar sesión", command=self._cerrar_sesion,
                  bg="#f44336", fg="white").pack(side="right", padx=15, pady=8)

        # Cuerpo con pestañas
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._crear_tab_productos()
        self._crear_tab_usuarios()
        self._crear_tab_ventas()

    def _crear_tab_productos(self) -> None:
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Productos")

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        tabla = ttk.Treeview(frame, columns=columnas, show="headings")
        tabla.heading("codigo", text="Código")
        tabla.heading("nombre", text="Nombre")
        tabla.heading("categoria", text="Categoría")
        tabla.heading("precio", text="Precio")
        tabla.heading("stock", text="Stock")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)

        tabla.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

        for p in self.servicio.listar_productos():
            tabla.insert("", "end", values=(
                p.codigo, p.nombre, p.categoria, f"${p.precio:.2f}", p.stock
            ))

    def _crear_tab_usuarios(self) -> None:
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Usuarios")

        columnas = ("identificacion", "nombre", "correo")
        tabla = ttk.Treeview(frame, columns=columnas, show="headings")
        tabla.heading("identificacion", text="Identificación")
        tabla.heading("nombre", text="Nombre")
        tabla.heading("correo", text="Correo")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)

        tabla.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

        for u in self.servicio.listar_usuarios():
            tabla.insert("", "end", values=(u.identificacion, u.nombre, u.correo))

    def _crear_tab_ventas(self) -> None:
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Ventas")

        tk.Label(frame, text="🚧 Módulo de ventas pendiente para próximas semanas.",
                 font=("Arial", 12, "italic"), fg="gray").pack(pady=50)

    def _cerrar_sesion(self) -> None:
        if messagebox.askyesno("Cerrar sesión", "¿Desea cerrar la sesión?"):
            self.al_cerrar_sesion()