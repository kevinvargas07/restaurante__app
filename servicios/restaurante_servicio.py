"""Módulo que contiene el servicio principal del restaurante."""

from typing import List, Optional, Dict
from modelos import Producto, Usuario
from .archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Servicio que administra productos y usuarios del restaurante."""
    
    def __init__(self) -> None:
        """Inicializa el servicio y carga los datos desde JSON."""
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._archivo = ArchivoServicio()
        self._cargar_datos()
    
    def _cargar_datos(self) -> None:
        """Carga productos y usuarios desde los archivos JSON."""
        self._productos = self._archivo.cargar_productos()
        self._usuarios = self._archivo.cargar_usuarios()
    
    # ---------- USUARIOS ----------
    def validar_acceso(self, identificacion: str, contrasena: str) -> Optional[Usuario]:
        """Valida las credenciales del usuario."""
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion and usuario.contrasena == contrasena:
                return usuario
        return None
    
    def listar_usuarios(self) -> List[Usuario]:
        """Retorna la lista de usuarios."""
        return self._usuarios.copy()
    
    # ---------- PRODUCTOS ----------
    def listar_productos(self) -> List[Producto]:
        """Retorna la lista de productos."""
        return self._productos.copy()
    
    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """Busca un producto por código."""
        codigo = codigo.strip().upper()
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None
    
    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int = 0
    ) -> bool:
        """
        Registra un nuevo producto.
        
        Returns:
            True si se registró, False si ya existe.
        Raises:
            ValueError: Si los datos son inválidos.
        """
        codigo = codigo.strip().upper()
        if self.buscar_producto(codigo) is not None:
            return False
        
        producto = Producto(codigo, nombre, categoria, precio, stock)
        self._productos.append(producto)
        self._archivo.guardar_productos(self._productos)
        return True
    
    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> bool:
        """
        Actualiza un producto existente.
        
        Returns:
            True si se actualizó, False si no existe.
        Raises:
            ValueError: Si los datos son inválidos.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        
        # Validar los nuevos datos creando un producto temporal
        producto_validado = Producto(codigo, nombre, categoria, precio, stock)
        
        # Aplicar los cambios
        producto.nombre = producto_validado.nombre
        producto.categoria = producto_validado.categoria
        producto.precio = producto_validado.precio
        producto.stock = producto_validado.stock
        
        self._archivo.guardar_productos(self._productos)
        return True
    
    def eliminar_producto(self, codigo: str) -> bool:
        """
        Elimina un producto por código.
        
        Returns:
            True si se eliminó, False si no existe.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        
        self._productos.remove(producto)
        self._archivo.guardar_productos(self._productos)
        return True
    
    # ---------- ESTADÍSTICAS ----------
    def cantidad_productos(self) -> int:
        return len(self._productos)
    
    def cantidad_usuarios(self) -> int:
        return len(self._usuarios)