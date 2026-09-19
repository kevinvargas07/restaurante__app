"""Vista principal del sistema con gestión de productos y usuarios."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional
from servicios import RestauranteServicio
from modelos import Usuario, Producto


class MainView:
    """Vista principal con pestañas de Productos y Usuarios."""
    
    def __init__(
        self,
        contenedor: tk.Frame,
        servicio: RestauranteServicio,
        usuario: Usuario,
        al_cerrar_sesion
    ) -> None:
        self.contenedor = contenedor
        self.servicio = servicio
        self.usuario = usuario
        self.al_cerrar_sesion = al_cerrar_sesion
        self._construir()
    
    def _construir(self) -> None:
        """Construye la vista principal."""
        self.frame = ttk.Frame(self.contenedor)
        self.frame.pack(fill="both", expand=True)
        
        self._construir_encabezado()
        self._construir_notebook()
        self._cargar_tabla_productos()
        self._cargar_tabla_usuarios()
    
    # ========== ENCABEZADO ==========
    def _construir_encabezado(self) -> None:
        """Construye el encabezado con información del usuario."""
        encabezado = tk.Frame(self.frame, bg="#2c3e50", height=60)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)
        
        tk.Label(
            encabezado,
            text="🍽️ Panel Principal",
            font=("Arial", 16, "bold"),
            bg="#2c3e50", fg="white"
        ).pack(side="left", padx=15)
        
        tk.Label(
            encabezado,
            text=f"👤 {self.usuario.nombre}",
            font=("Arial", 11),
            bg="#2c3e50", fg="#ecf0f1"
        ).pack(side="left", padx=15)
        
        tk.Button(
            encabezado,
            text="Cerrar sesión",
            command=self._cerrar_sesion,
            bg="#e74c3c", fg="white",
            relief="flat", padx=15, pady=5,
            cursor="hand2"
        ).pack(side="right", padx=15, pady=10)
    
    # ========== NOTEBOOK (PESTAÑAS) ==========
    def _construir_notebook(self) -> None:
        """Construye el notebook con las pestañas."""
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña de Productos
        self.tab_productos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_productos, text="📦 Productos")
        self._construir_tab_productos()
        
        # Pestaña de Usuarios
        self.tab_usuarios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_usuarios, text="👥 Usuarios")
        self._construir_tab_usuarios()
    
    # ========== TAB PRODUCTOS ==========
    def _construir_tab_productos(self) -> None:
        """Construye la pestaña de productos con formulario y tabla."""
        # Contenedor superior: formulario (izquierda) + acciones (derecha)
        frame_superior = ttk.Frame(self.tab_productos)
        frame_superior.pack(fill="x", padx=10, pady=10)
        
        # --- Formulario de producto ---
        self._construir_formulario_producto(frame_superior)
        
        # --- Panel de acciones ---
        self._construir_panel_acciones(frame_superior)
        
        # --- Tabla de productos ---
        self._construir_tabla_productos()
    
    def _construir_formulario_producto(self, padre: ttk.Frame) -> None:
        """Construye el formulario de productos."""
        frame_form = ttk.LabelFrame(
            padre,
            text="Datos del Producto",
            padding=15
        )
        frame_form.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Fila 0: Código
        ttk.Label(frame_form, text="Código:").grid(
            row=0, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_codigo = ttk.Entry(frame_form, width=25)
        self.entry_codigo.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        # Fila 1: Nombre
        ttk.Label(frame_form, text="Nombre:").grid(
            row=1, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_nombre = ttk.Entry(frame_form, width=25)
        self.entry_nombre.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        # Fila 2: Categoría
        ttk.Label(frame_form, text="Categoría:").grid(
            row=2, column=0, sticky="w", pady=5, padx=5
        )
        self.combo_categoria = ttk.Combobox(
            frame_form,
            values=["comida", "bebida", "postre", "entrada"],
            width=23,
            state="readonly"
        )
        self.combo_categoria.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        self.combo_categoria.current(0)
        
        # Fila 3: Precio
        ttk.Label(frame_form, text="Precio:").grid(
            row=3, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_precio = ttk.Entry(frame_form, width=25)
        self.entry_precio.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        
        # Fila 4: Stock
        ttk.Label(frame_form, text="Stock:").grid(
            row=4, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_stock = ttk.Entry(frame_form, width=25)
        self.entry_stock.grid(row=4, column=1, pady=5, padx=5, sticky="ew")
        
        # Fila 5: Botón limpiar
        ttk.Button(
            frame_form,
            text="🧹 Limpiar formulario",
            command=self._limpiar_formulario
        ).grid(row=5, column=0, columnspan=2, pady=10)
        
        frame_form.columnconfigure(1, weight=1)
    
    def _construir_panel_acciones(self, padre: ttk.Frame) -> None:
        """Construye el panel de botones de acción."""
        frame_acciones = ttk.LabelFrame(
            padre,
            text="Acciones",
            padding=15
        )
        frame_acciones.pack(side="right", fill="y")
        
        # Botones de CRUD
        botones = [
            ("➕ Registrar", self._registrar_producto, "#27ae60"),
            ("🔍 Buscar", self._buscar_producto, "#2980b9"),
            ("✏️ Actualizar", self._actualizar_producto, "#f39c12"),
            ("🗑️ Eliminar", self._eliminar_producto, "#c0392b"),
            ("🔄 Recargar", self._cargar_tabla_productos, "#7f8c8d"),
        ]
        
        for texto, comando, color in botones:
            ttk.Button(
                frame_acciones,
                text=texto,
                command=comando,
                width=18
            ).pack(pady=4, fill="x")
    
    def _construir_tabla_productos(self) -> None:
        """Construye la tabla de productos."""
        frame_tabla = ttk.LabelFrame(
            self.tab_productos,
            text="Lista de Productos",
            padding=10
        )
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=10
        )
        
        # Encabezados
        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("categoria", text="Categoría")
        self.tabla_productos.heading("precio", text="Precio")
        self.tabla_productos.heading("stock", text="Stock")
        
        # Ancho de columnas
        self.tabla_productos.column("codigo", width=80, anchor="center")
        self.tabla_productos.column("nombre", width=200)
        self.tabla_productos.column("categoria", width=100, anchor="center")
        self.tabla_productos.column("precio", width=90, anchor="e")
        self.tabla_productos.column("stock", width=70, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Etiqueta de estado
        self.label_estado = ttk.Label(
            self.tab_productos,
            text="",
            font=("Arial", 9, "italic"),
            foreground="gray"
        )
        self.label_estado.pack(pady=(0, 5))
    
    def _cargar_tabla_productos(self) -> None:
        """Carga/recarga la tabla de productos desde el servicio."""
        # Limpiar tabla
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        
        # Insertar productos
        productos = self.servicio.listar_productos()
        for producto in productos:
            self.tabla_productos.insert("", "end", values=(
                producto.codigo,
                producto.nombre,
                producto.categoria,
                f"${producto.precio:.2f}",
                producto.stock
            ))
        
        self.label_estado.config(
            text=f"Total: {len(productos)} productos"
        )
    
    # ========== TAB USUARIOS ==========
    def _construir_tab_usuarios(self) -> None:
        """Construye la pestaña de usuarios (solo consulta)."""
        frame_tabla = ttk.LabelFrame(
            self.tab_usuarios,
            text="Usuarios Registrados",
            padding=10
        )
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        columnas = ("identificacion", "nombre", "correo")
        self.tabla_usuarios = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=15
        )
        
        self.tabla_usuarios.heading("identificacion", text="Identificación")
        self.tabla_usuarios.heading("nombre", text="Nombre")
        self.tabla_usuarios.heading("correo", text="Correo")
        
        self.tabla_usuarios.column("identificacion", width=150, anchor="center")
        self.tabla_usuarios.column("nombre", width=200)
        self.tabla_usuarios.column("correo", width=250)
        
        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_usuarios.yview
        )
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)
        
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _cargar_tabla_usuarios(self) -> None:
        """Carga la tabla de usuarios."""
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        
        for usuario in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert("", "end", values=(
                usuario.identificacion,
                usuario.nombre,
                usuario.correo
            ))
    
    # ========== OPERACIONES CRUD ==========
    def _obtener_datos_formulario(self) -> Optional[dict]:
        """Obtiene y valida los datos del formulario."""
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        categoria = self.combo_categoria.get().strip()
        precio_str = self.entry_precio.get().strip()
        stock_str = self.entry_stock.get().strip()
        
        if not all([codigo, nombre, categoria, precio_str, stock_str]):
            messagebox.showwarning(
                "Campos vacíos",
                "Todos los campos son obligatorios."
            )
            return None
        
        try:
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror(
                "Precio inválido",
                "El precio debe ser un número (ej: 5.50)."
            )
            return None
        
        try:
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror(
                "Stock inválido",
                "El stock debe ser un número entero."
            )
            return None
        
        return {
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
            "stock": stock
        }
    
    def _registrar_producto(self) -> None:
        """Registra un producto usando el servicio."""
        datos = self._obtener_datos_formulario()
        if datos is None:
            return
        
        try:
            exito = self.servicio.registrar_producto(**datos)
            if exito:
                messagebox.showinfo(
                    "Éxito",
                    f"Producto '{datos['codigo']}' registrado correctamente."
                )
                self._cargar_tabla_productos()
                self._limpiar_formulario()
            else:
                messagebox.showwarning(
                    "Duplicado",
                    f"Ya existe un producto con el código '{datos['codigo']}'."
                )
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))
    
    def _buscar_producto(self) -> None:
        """Busca un producto y carga sus datos en el formulario."""
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning(
                "Campo vacío",
                "Ingrese el código del producto a buscar."
            )
            return
        
        producto = self.servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showinfo(
                "No encontrado",
                f"No existe un producto con el código '{codigo}'."
            )
            return
        
        # Cargar datos en el formulario
        self.entry_codigo.delete(0, "end")
        self.entry_codigo.insert(0, producto.codigo)
        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, producto.nombre)
        self.combo_categoria.set(producto.categoria)
        self.entry_precio.delete(0, "end")
        self.entry_precio.insert(0, str(producto.precio))
        self.entry_stock.delete(0, "end")
        self.entry_stock.insert(0, str(producto.stock))
        
        messagebox.showinfo(
            "Encontrado",
            f"Producto '{producto.nombre}' cargado en el formulario."
        )
    
    def _actualizar_producto(self) -> None:
        """Actualiza un producto usando el servicio."""
        datos = self._obtener_datos_formulario()
        if datos is None:
            return
        
        try:
            exito = self.servicio.actualizar_producto(**datos)
            if exito:
                messagebox.showinfo(
                    "Éxito",
                    f"Producto '{datos['codigo']}' actualizado correctamente."
                )
                self._cargar_tabla_productos()
                self._limpiar_formulario()
            else:
                messagebox.showwarning(
                    "No encontrado",
                    f"No existe un producto con el código '{datos['codigo']}'."
                )
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))
    
    def _eliminar_producto(self) -> None:
        """Elimina un producto usando el servicio."""
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning(
                "Campo vacío",
                "Ingrese el código del producto a eliminar."
            )
            return
        
        producto = self.servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showinfo(
                "No encontrado",
                f"No existe un producto con el código '{codigo}'."
            )
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar el producto '{producto.nombre}' ({producto.codigo})?"
        )
        if not confirmar:
            return
        
        if self.servicio.eliminar_producto(codigo):
            messagebox.showinfo(
                "Éxito",
                f"Producto '{codigo}' eliminado correctamente."
            )
            self._cargar_tabla_productos()
            self._limpiar_formulario()
    
    def _limpiar_formulario(self) -> None:
        """Limpia todos los campos del formulario."""
        self.entry_codigo.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.combo_categoria.current(0)
        self.entry_precio.delete(0, "end")
        self.entry_stock.delete(0, "end")
        self.entry_codigo.focus_set()
    
    # ========== CERRAR SESIÓN ==========
    def _cerrar_sesion(self) -> None:
        """Cierra la sesión actual."""
        if messagebox.askyesno("Cerrar sesión", "¿Desea cerrar la sesión?"):
            self.al_cerrar_sesion()