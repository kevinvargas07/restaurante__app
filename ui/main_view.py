"""Vista principal del sistema con gestión de productos, usuarios y ventas."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional
from servicios import RestauranteServicio
from modelos import Usuario, Producto


class MainView:
    """Vista principal con pestañas de Productos, Usuarios y Ventas."""
    
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
        self._usuarios_venta = []
        self._productos_venta = []
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
        
        # Pestaña de Ventas
        self.tab_ventas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ventas, text="🛒 Ventas")
        self._construir_tab_ventas()
    
    # ========== TAB PRODUCTOS ==========
    def _construir_tab_productos(self) -> None:
        """Construye la pestaña de productos con formulario y tabla."""
        frame_superior = ttk.Frame(self.tab_productos)
        frame_superior.pack(fill="x", padx=10, pady=10)
        
        self._construir_formulario_producto(frame_superior)
        self._construir_panel_acciones(frame_superior)
        self._construir_tabla_productos()
    
    def _construir_formulario_producto(self, padre: ttk.Frame) -> None:
        """Construye el formulario de productos."""
        frame_form = ttk.LabelFrame(
            padre,
            text="Datos del Producto",
            padding=15
        )
        frame_form.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Código
        ttk.Label(frame_form, text="Código:").grid(
            row=0, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_codigo = ttk.Entry(frame_form, width=25)
        self.entry_codigo.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        # Nombre
        ttk.Label(frame_form, text="Nombre:").grid(
            row=1, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_nombre = ttk.Entry(frame_form, width=25)
        self.entry_nombre.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        # Categoría
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
        
        # Precio
        ttk.Label(frame_form, text="Precio:").grid(
            row=3, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_precio = ttk.Entry(frame_form, width=25)
        self.entry_precio.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        
        # Stock
        ttk.Label(frame_form, text="Stock:").grid(
            row=4, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_stock = ttk.Entry(frame_form, width=25)
        self.entry_stock.grid(row=4, column=1, pady=5, padx=5, sticky="ew")
        
        # Botón limpiar
        ttk.Button(
            frame_form,
            text="🧹 Limpiar formulario",
            command=self._limpiar_formulario
        ).grid(row=5, column=0, columnspan=2, pady=10)
        
        frame_form.columnconfigure(1, weight=1)
    
    def _construir_panel_acciones(self, padre: ttk.Frame) -> None:
        """Construye el panel de botones de acción."""
        frame_acciones = ttk.LabelFrame(padre, text="Acciones", padding=15)
        frame_acciones.pack(side="right", fill="y")
        
        botones = [
            ("➕ Registrar", self._registrar_producto),
            ("🔍 Buscar", self._buscar_producto),
            ("✏️ Actualizar", self._actualizar_producto),
            ("🗑️ Eliminar", self._eliminar_producto),
            ("🔄 Recargar", self._cargar_tabla_productos),
        ]
        
        for texto, comando in botones:
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
        
        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("categoria", text="Categoría")
        self.tabla_productos.heading("precio", text="Precio")
        self.tabla_productos.heading("stock", text="Stock")
        
        self.tabla_productos.column("codigo", width=80, anchor="center")
        self.tabla_productos.column("nombre", width=200)
        self.tabla_productos.column("categoria", width=100, anchor="center")
        self.tabla_productos.column("precio", width=90, anchor="e")
        self.tabla_productos.column("stock", width=70, anchor="center")
        
        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.label_estado = ttk.Label(
            self.tab_productos,
            text="",
            font=("Arial", 9, "italic"),
            foreground="gray"
        )
        self.label_estado.pack(pady=(0, 5))
    
    def _cargar_tabla_productos(self) -> None:
        """Carga/recarga la tabla de productos."""
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        
        productos = self.servicio.listar_productos()
        for producto in productos:
            self.tabla_productos.insert("", "end", values=(
                producto.codigo,
                producto.nombre,
                producto.categoria,
                f"${producto.precio:.2f}",
                producto.stock
            ))
        
        self.label_estado.config(text=f"Total: {len(productos)} productos")
    
        # ========== TAB USUARIOS (Semana 16) ==========
    def _construir_tab_usuarios(self) -> None:
        """Construye la pestaña de usuarios con formulario y tabla."""
        # Contenedor superior: formulario + acciones
        frame_superior = ttk.Frame(self.tab_usuarios)
        frame_superior.pack(fill="x", padx=10, pady=10)
        
        # --- Formulario de usuario ---
        self._construir_formulario_usuario(frame_superior)
        
        # --- Panel de acciones ---
        self._construir_panel_acciones_usuario(frame_superior)
        
        # --- Tabla de usuarios ---
        self._construir_tabla_usuarios()
    
    def _construir_formulario_usuario(self, padre: ttk.Frame) -> None:
        """Construye el formulario de usuarios."""
        frame_form = ttk.LabelFrame(
            padre,
            text="Datos del Usuario",
            padding=15
        )
        frame_form.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Identificación
        ttk.Label(frame_form, text="Identificación:").grid(
            row=0, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_identificacion = ttk.Entry(frame_form, width=30)
        self.entry_identificacion.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        # Nombre
        ttk.Label(frame_form, text="Nombre:").grid(
            row=1, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_nombre_usuario = ttk.Entry(frame_form, width=30)
        self.entry_nombre_usuario.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        # Correo
        ttk.Label(frame_form, text="Correo:").grid(
            row=2, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_correo = ttk.Entry(frame_form, width=30)
        self.entry_correo.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        
        # Contraseña
        ttk.Label(frame_form, text="Contraseña:").grid(
            row=3, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_contrasena_usuario = ttk.Entry(frame_form, width=30, show="*")
        self.entry_contrasena_usuario.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        self.entry_contrasena_usuario.insert(0, "1234")
        
        # Rol
        ttk.Label(frame_form, text="Rol:").grid(
            row=4, column=0, sticky="w", pady=5, padx=5
        )
        self.combo_rol = ttk.Combobox(
            frame_form,
            values=["Administrador", "Empleado", "Cliente"],
            width=28,
            state="readonly"
        )
        self.combo_rol.grid(row=4, column=1, pady=5, padx=5, sticky="ew")
        self.combo_rol.current(2)  # Cliente por defecto
        
        # Etiqueta informativa del rol
        self.label_info_rol = ttk.Label(
            frame_form,
            text="Rol seleccionado: Cliente",
            font=("Arial", 9, "italic"),
            foreground="gray"
        )
        self.label_info_rol.grid(row=5, column=0, columnspan=2, pady=(5, 0))
        
        frame_form.columnconfigure(1, weight=1)
        
        # ========== EVENTOS ==========
        # <Return> en cualquier campo del formulario → registrar
        self.entry_identificacion.bind("<Return>", self._on_return_usuario)
        self.entry_nombre_usuario.bind("<Return>", self._on_return_usuario)
        self.entry_correo.bind("<Return>", self._on_return_usuario)
        self.entry_contrasena_usuario.bind("<Return>", self._on_return_usuario)
        
        # <Escape> → limpiar formulario
        self.entry_identificacion.bind("<Escape>", self._on_escape_usuario)
        self.entry_nombre_usuario.bind("<Escape>", self._on_escape_usuario)
        self.entry_correo.bind("<Escape>", self._on_escape_usuario)
        self.entry_contrasena_usuario.bind("<Escape>", self._on_escape_usuario)
        
        # <<ComboboxSelected>> → actualizar etiqueta informativa
        self.combo_rol.bind("<<ComboboxSelected>>", self._on_rol_seleccionado)
    
    def _construir_panel_acciones_usuario(self, padre: ttk.Frame) -> None:
        """Construye el panel de botones de acción para usuarios."""
        frame_acciones = ttk.LabelFrame(padre, text="Acciones", padding=15)
        frame_acciones.pack(side="right", fill="y")
        
        botones = [
            ("➕ Registrar", self._registrar_usuario),
            ("✏️ Actualizar", self._actualizar_usuario),
            ("🗑️ Eliminar", self._eliminar_usuario),
            ("🧹 Limpiar", self._limpiar_formulario_usuario),
        ]
        
        for texto, comando in botones:
            ttk.Button(
                frame_acciones,
                text=texto,
                command=comando,
                width=18
            ).pack(pady=4, fill="x")
        
        # Nota informativa
        ttk.Label(
            frame_acciones,
            text="Enter: registrar\nEsc: limpiar",
            font=("Arial", 8, "italic"),
            foreground="gray",
            justify="center"
        ).pack(pady=(10, 0))
    
    def _construir_tabla_usuarios(self) -> None:
        """Construye la tabla de usuarios."""
        frame_tabla = ttk.LabelFrame(
            self.tab_usuarios,
            text="Usuarios Registrados",
            padding=10
        )
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        columnas = ("identificacion", "nombre", "correo", "rol")
        self.tabla_usuarios = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=10
        )
        
        self.tabla_usuarios.heading("identificacion", text="Identificación")
        self.tabla_usuarios.heading("nombre", text="Nombre")
        self.tabla_usuarios.heading("correo", text="Correo")
        self.tabla_usuarios.heading("rol", text="Rol")
        
        self.tabla_usuarios.column("identificacion", width=130, anchor="center")
        self.tabla_usuarios.column("nombre", width=180)
        self.tabla_usuarios.column("correo", width=230)
        self.tabla_usuarios.column("rol", width=120, anchor="center")
        
        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_usuarios.yview
        )
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)
        
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Etiqueta de estado
        self.label_estado_usuarios = ttk.Label(
            self.tab_usuarios,
            text="",
            font=("Arial", 9, "italic"),
            foreground="gray"
        )
        self.label_estado_usuarios.pack(pady=(0, 5))
        
        # ========== EVENTO: <<TreeviewSelect>> ==========
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self._on_usuario_seleccionado)
    
    def _cargar_tabla_usuarios(self) -> None:
        """Carga/recarga la tabla de usuarios."""
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        
        usuarios = self.servicio.listar_usuarios()
        for usuario in usuarios:
            self.tabla_usuarios.insert("", "end", values=(
                usuario.identificacion,
                usuario.nombre,
                usuario.correo,
                usuario.rol
            ))
        
        self.label_estado_usuarios.config(
            text=f"Total: {len(usuarios)} usuarios registrados"
        )
    
    # ========== CALLBACKS DE EVENTOS (USUARIOS) ==========
    def _on_usuario_seleccionado(self, event=None) -> None:
        """Callback para <<TreeviewSelect>>: carga los datos del usuario."""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return
        
        # Obtener la identificación de la fila seleccionada
        item = self.tabla_usuarios.item(seleccion[0])
        valores = item.get("values", [])
        if not valores:
            return
        
        identificacion = valores[0]
        
        # Buscar el objeto Usuario mediante el servicio
        usuario = self.servicio.buscar_usuario(identificacion)
        if usuario is None:
            return
        
        # Cargar los datos en el formulario
        self.entry_identificacion.delete(0, "end")
        self.entry_identificacion.insert(0, usuario.identificacion)
        self.entry_identificacion.config(state="readonly")
        
        self.entry_nombre_usuario.delete(0, "end")
        self.entry_nombre_usuario.insert(0, usuario.nombre)
        
        self.entry_correo.delete(0, "end")
        self.entry_correo.insert(0, usuario.correo)
        
        self.entry_contrasena_usuario.delete(0, "end")
        self.entry_contrasena_usuario.insert(0, usuario.contrasena)
        
        self.combo_rol.set(usuario.rol)
        self.label_info_rol.config(text=f"Rol seleccionado: {usuario.rol}")
    
    def _on_return_usuario(self, event=None) -> None:
        """Callback para <Return>: registra un usuario reutilizando el método."""
        # Reutilizar el método existente (NO duplicar lógica)
        self._registrar_usuario()
    
    def _on_escape_usuario(self, event=None) -> None:
        """Callback para <Escape>: limpia el formulario y la selección."""
        self._limpiar_formulario_usuario()
    
    def _on_rol_seleccionado(self, event=None) -> None:
        """Callback para <<ComboboxSelected>>: actualiza la etiqueta del rol."""
        rol = self.combo_rol.get()
        self.label_info_rol.config(text=f"Rol seleccionado: {rol}")
    
    # ========== CRUD USUARIOS ==========
    def _obtener_datos_formulario_usuario(self) -> Optional[dict]:
        """Obtiene y valida los datos del formulario de usuarios."""
        identificacion = self.entry_identificacion.get().strip()
        nombre = self.entry_nombre_usuario.get().strip()
        correo = self.entry_correo.get().strip()
        contrasena = self.entry_contrasena_usuario.get().strip()
        rol = self.combo_rol.get().strip()
        
        if not all([identificacion, nombre, correo, contrasena, rol]):
            messagebox.showwarning(
                "Campos vacíos",
                "Todos los campos son obligatorios."
            )
            return None
        
        return {
            "identificacion": identificacion,
            "nombre": nombre,
            "correo": correo,
            "contrasena": contrasena,
            "rol": rol
        }
    
    def _registrar_usuario(self) -> None:
        """Registra un usuario usando el servicio."""
        datos = self._obtener_datos_formulario_usuario()
        if datos is None:
            return
        
        try:
            exito = self.servicio.registrar_usuario(**datos)
            if exito:
                messagebox.showinfo(
                    "Éxito",
                    f"Usuario '{datos['identificacion']}' registrado correctamente."
                )
                self._cargar_tabla_usuarios()
                self._limpiar_formulario_usuario()
            else:
                messagebox.showwarning(
                    "Duplicado",
                    f"Ya existe un usuario con identificación '{datos['identificacion']}'."
                )
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))
    
    def _actualizar_usuario(self) -> None:
        """Actualiza un usuario usando el servicio."""
        datos = self._obtener_datos_formulario_usuario()
        if datos is None:
            return
        
        # Proteger la cuenta del administrador autenticado
        if datos["identificacion"] == self.usuario.identificacion:
            if not messagebox.askyesno(
                "Modificar cuenta propia",
                "Está a punto de modificar su propia cuenta. ¿Continuar?"
            ):
                return
        
        try:
            exito = self.servicio.actualizar_usuario(**datos)
            if exito:
                messagebox.showinfo(
                    "Éxito",
                    f"Usuario '{datos['identificacion']}' actualizado correctamente."
                )
                self._cargar_tabla_usuarios()
                self._limpiar_formulario_usuario()
            else:
                messagebox.showwarning(
                    "No encontrado",
                    f"No existe un usuario con identificación '{datos['identificacion']}'."
                )
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))
    
    def _eliminar_usuario(self) -> None:
        """Elimina un usuario usando el servicio."""
        identificacion = self.entry_identificacion.get().strip()
        if not identificacion:
            messagebox.showwarning(
                "Campo vacío",
                "Seleccione un usuario de la tabla para eliminar."
            )
            return
        
        # Proteger la cuenta del administrador autenticado
        if identificacion == self.usuario.identificacion:
            messagebox.showerror(
                "Operación no permitida",
                "No puede eliminar su propia cuenta mientras está conectado."
            )
            return
        
        usuario = self.servicio.buscar_usuario(identificacion)
        if usuario is None:
            messagebox.showinfo(
                "No encontrado",
                f"No existe un usuario con identificación '{identificacion}'."
            )
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar el usuario '{usuario.nombre}' ({usuario.identificacion})?"
        )
        if not confirmar:
            return
        
        if self.servicio.eliminar_usuario(identificacion):
            messagebox.showinfo(
                "Éxito",
                f"Usuario '{identificacion}' eliminado correctamente."
            )
            self._cargar_tabla_usuarios()
            self._limpiar_formulario_usuario()
    
    def _limpiar_formulario_usuario(self) -> None:
        """Limpia el formulario y la selección del Treeview."""
        # Habilitar el campo identificación (puede estar readonly)
        self.entry_identificacion.config(state="normal")
        
        self.entry_identificacion.delete(0, "end")
        self.entry_nombre_usuario.delete(0, "end")
        self.entry_correo.delete(0, "end")
        self.entry_contrasena_usuario.delete(0, "end")
        self.entry_contrasena_usuario.insert(0, "1234")
        self.combo_rol.current(2)  # Cliente
        self.label_info_rol.config(text="Rol seleccionado: Cliente")
        
        # Limpiar selección del Treeview
        for item in self.tabla_usuarios.selection():
            self.tabla_usuarios.selection_remove(item)
        
        self.entry_identificacion.focus_set()
    
    # ========== TAB VENTAS ==========
    def _construir_tab_ventas(self) -> None:
        """Construye la pestaña de ventas."""
        frame_superior = ttk.Frame(self.tab_ventas)
        frame_superior.pack(fill="x", padx=10, pady=10)
        
        # Formulario de venta
        frame_form = ttk.LabelFrame(
            frame_superior,
            text="Registrar Nueva Venta",
            padding=15
        )
        frame_form.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Usuario
        ttk.Label(frame_form, text="Usuario:").grid(
            row=0, column=0, sticky="w", pady=5, padx=5
        )
        self.combo_usuario_venta = ttk.Combobox(
            frame_form, width=40, state="readonly"
        )
        self.combo_usuario_venta.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        # Producto
        ttk.Label(frame_form, text="Producto:").grid(
            row=1, column=0, sticky="w", pady=5, padx=5
        )
        self.combo_producto_venta = ttk.Combobox(
            frame_form, width=40, state="readonly"
        )
        self.combo_producto_venta.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        # Cantidad
        ttk.Label(frame_form, text="Cantidad:").grid(
            row=2, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_cantidad_venta = ttk.Entry(frame_form, width=40)
        self.entry_cantidad_venta.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        self.entry_cantidad_venta.insert(0, "1")
        
        frame_form.columnconfigure(1, weight=1)
        
        # Panel de acciones
        frame_acciones = ttk.LabelFrame(
            frame_superior,
            text="Acciones",
            padding=15
        )
        frame_acciones.pack(side="right", fill="y")
        
        ttk.Button(
            frame_acciones,
            text="🛒 Registrar venta",
            command=self._registrar_venta,
            width=20
        ).pack(pady=5, fill="x")
        
        ttk.Button(
            frame_acciones,
            text="🔄 Recargar",
            command=self._cargar_tabla_ventas,
            width=20
        ).pack(pady=5, fill="x")
        
        ttk.Button(
            frame_acciones,
            text="🧹 Limpiar",
            command=self._limpiar_formulario_venta,
            width=20
        ).pack(pady=5, fill="x")
        
        # Tabla de ventas
        frame_tabla = ttk.LabelFrame(
            self.tab_ventas,
            text="Ventas Registradas",
            padding=10
        )
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        columnas = ("codigo", "usuario", "producto", "cantidad", "fecha")
        self.tabla_ventas = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=10
        )
        
        self.tabla_ventas.heading("codigo", text="Código")
        self.tabla_ventas.heading("usuario", text="Usuario")
        self.tabla_ventas.heading("producto", text="Producto")
        self.tabla_ventas.heading("cantidad", text="Cantidad")
        self.tabla_ventas.heading("fecha", text="Fecha")
        
        self.tabla_ventas.column("codigo", width=80, anchor="center")
        self.tabla_ventas.column("usuario", width=150)
        self.tabla_ventas.column("producto", width=150)
        self.tabla_ventas.column("cantidad", width=80, anchor="center")
        self.tabla_ventas.column("fecha", width=160, anchor="center")
        
        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_ventas.yview
        )
        self.tabla_ventas.configure(yscrollcommand=scrollbar.set)
        
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.label_estado_ventas = ttk.Label(
            self.tab_ventas,
            text="",
            font=("Arial", 9, "italic"),
            foreground="gray"
        )
        self.label_estado_ventas.pack(pady=(0, 5))
        
        # Cargar datos iniciales
        self._cargar_combos_venta()
        self._cargar_tabla_ventas()
    
    def _cargar_combos_venta(self) -> None:
        """Carga los usuarios y productos en los Combobox."""
        # Usuarios
        self._usuarios_venta = self.servicio.listar_usuarios()
        valores_usuarios = [
            f"{u.identificacion} - {u.nombre}" for u in self._usuarios_venta
        ]
        self.combo_usuario_venta["values"] = valores_usuarios
        if valores_usuarios:
            self.combo_usuario_venta.current(0)
        
        # Productos
        self._productos_venta = self.servicio.listar_productos()
        valores_productos = [
            f"{p.codigo} - {p.nombre} (${p.precio:.2f}) - Stock: {p.stock}"
            for p in self._productos_venta
        ]
        self.combo_producto_venta["values"] = valores_productos
        if valores_productos:
            self.combo_producto_venta.current(0)
    
    def _cargar_tabla_ventas(self) -> None:
        """Carga/recarga la tabla de ventas."""
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)
        
        ventas = self.servicio.listar_ventas()
        for venta in ventas:
            self.tabla_ventas.insert("", "end", values=(
                venta.codigo,
                venta.identificacion_usuario,
                venta.codigo_producto,
                venta.cantidad,
                venta.fecha
            ))
        
        self.label_estado_ventas.config(
            text=f"Total: {len(ventas)} ventas registradas"
        )
    
    # ========== CALLBACK DE VENTA ==========
    def _registrar_venta(self) -> None:
        """Callback que se ejecuta al presionar 'Registrar venta'."""
        idx_usuario = self.combo_usuario_venta.current()
        idx_producto = self.combo_producto_venta.current()
        
        if idx_usuario < 0 or idx_producto < 0:
            messagebox.showwarning(
                "Selección requerida",
                "Debe seleccionar un usuario y un producto."
            )
            return
        
        if not self._usuarios_venta or not self._productos_venta:
            messagebox.showwarning(
                "Datos insuficientes",
                "Debe haber al menos un usuario y un producto registrados."
            )
            return
        
        identificacion = self._usuarios_venta[idx_usuario].identificacion
        codigo_producto = self._productos_venta[idx_producto].codigo
        cantidad_str = self.entry_cantidad_venta.get().strip()
        
        try:
            cantidad = int(cantidad_str)
        except ValueError:
            messagebox.showerror(
                "Cantidad inválida",
                "La cantidad debe ser un número entero."
            )
            return
        
        try:
            venta = self.servicio.registrar_venta(
                identificacion_usuario=identificacion,
                codigo_producto=codigo_producto,
                cantidad=cantidad
            )
            
            if venta is None:
                messagebox.showerror("Error", "No se pudo registrar la venta.")
                return
            
            messagebox.showinfo(
                "Venta registrada",
                f"✓ Venta {venta.codigo} registrada correctamente.\n\n"
                f"Usuario: {venta.identificacion_usuario}\n"
                f"Producto: {venta.codigo_producto}\n"
                f"Cantidad: {venta.cantidad}\n"
                f"Fecha: {venta.fecha}"
            )
            
            self._cargar_tabla_ventas()
            self._cargar_combos_venta()
            self._cargar_tabla_productos()
            self.entry_cantidad_venta.delete(0, "end")
            self.entry_cantidad_venta.insert(0, "1")
            
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))
    
    def _limpiar_formulario_venta(self) -> None:
        """Limpia los campos del formulario de ventas."""
        if self.combo_usuario_venta["values"]:
            self.combo_usuario_venta.current(0)
        if self.combo_producto_venta["values"]:
            self.combo_producto_venta.current(0)
        self.entry_cantidad_venta.delete(0, "end")
        self.entry_cantidad_venta.insert(0, "1")
    
    # ========== OPERACIONES CRUD PRODUCTOS ==========
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
                self._cargar_combos_venta()
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
                self._cargar_combos_venta()
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
            self._cargar_combos_venta()
            self._limpiar_formulario()
    
    def _limpiar_formulario(self) -> None:
        """Limpia todos los campos del formulario de productos."""
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