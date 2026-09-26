"""Módulo que contiene el servicio principal del restaurante."""

from datetime import datetime
from typing import List, Optional
from modelos import Producto, Usuario, Venta
from .archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Servicio que administra productos, usuarios y ventas."""
    
    def __init__(self) -> None:
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._ventas: List[Venta] = []
        self._archivo = ArchivoServicio()
        self._cargar_datos()
    
    def _cargar_datos(self) -> None:
        self._productos = self._archivo.cargar_productos()
        self._usuarios = self._archivo.cargar_usuarios()
        self._ventas = self._archivo.cargar_ventas()
    
    # ---------- USUARIOS ----------
    def validar_acceso(self, identificacion: str, contrasena: str) -> Optional[Usuario]:
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion and usuario.contrasena == contrasena:
                return usuario
        return None
    
    def listar_usuarios(self) -> List[Usuario]:
        return self._usuarios.copy()
    
    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None
    
    # ---------- PRODUCTOS ----------
    def listar_productos(self) -> List[Producto]:
        return self._productos.copy()
    
    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        codigo = codigo.strip().upper()
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None
    
    def registrar_producto(
        self, codigo: str, nombre: str, categoria: str,
        precio: float, stock: int = 0
    ) -> bool:
        codigo = codigo.strip().upper()
        if self.buscar_producto(codigo) is not None:
            return False
        producto = Producto(codigo, nombre, categoria, precio, stock)
        self._productos.append(producto)
        self._archivo.guardar_productos(self._productos)
        return True
    
    def actualizar_producto(
        self, codigo: str, nombre: str, categoria: str,
        precio: float, stock: int
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        producto_validado = Producto(codigo, nombre, categoria, precio, stock)
        producto.nombre = producto_validado.nombre
        producto.categoria = producto_validado.categoria
        producto.precio = producto_validado.precio
        producto.stock = producto_validado.stock
        self._archivo.guardar_productos(self._productos)
        return True
    
    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        self._archivo.guardar_productos(self._productos)
        return True
    
    # ---------- VENTAS ----------
    def listar_ventas(self) -> List[Venta]:
        return self._ventas.copy()
    
    def buscar_venta(self, codigo: str) -> Optional[Venta]:
        codigo = codigo.strip().upper()
        for venta in self._ventas:
            if venta.codigo == codigo:
                return venta
        return None
    
    def generar_codigo_venta(self) -> str:
        """Genera un código de venta único tipo V001, V002, ..."""
        numero = len(self._ventas) + 1
        while True:
            codigo = f"V{numero:03d}"
            if self.buscar_venta(codigo) is None:
                return codigo
            numero += 1
    
    def registrar_venta(
        self, identificacion_usuario: str, codigo_producto: str,
        cantidad: int = 1
    ) -> Optional[Venta]:
        """
        Registra una venta relacionando usuario y producto.
        
        Returns:
            La Venta creada si tuvo éxito, None en caso contrario.
        Raises:
            ValueError: Si los datos no son válidos.
        """
        # Validar que el usuario existe
        usuario = self.buscar_usuario(identificacion_usuario)
        if usuario is None:
            raise ValueError(f"No existe un usuario con identificación '{identificacion_usuario}'")
        
        # Validar que el producto existe
        producto = self.buscar_producto(codigo_producto)
        if producto is None:
            raise ValueError(f"No existe un producto con código '{codigo_producto}'")
        
        # Validar cantidad
        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            raise ValueError("La cantidad debe ser un número entero")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        # Validar stock
        if producto.stock < cantidad:
            raise ValueError(
                f"Stock insuficiente. Disponible: {producto.stock}, "
                f"solicitado: {cantidad}"
            )
        
        # Descontar stock
        producto.stock -= cantidad
        
        # Crear y guardar la venta
        codigo_venta = self.generar_codigo_venta()
        venta = Venta(
            codigo=codigo_venta,
            identificacion_usuario=identificacion_usuario,
            codigo_producto=codigo_producto,
            cantidad=cantidad,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self._ventas.append(venta)
        
        # Persistir
        self._archivo.guardar_ventas(self._ventas)
        self._archivo.guardar_productos(self._productos)
        
        return venta
    
    # ---------- ESTADÍSTICAS ----------
    def cantidad_productos(self) -> int:
        return len(self._productos)
    
    def cantidad_usuarios(self) -> int:
        return len(self._usuarios)
    
    def cantidad_ventas(self) -> int:
        return len(self._ventas)