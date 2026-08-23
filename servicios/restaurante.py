"""Módulo que contiene el servicio principal del restaurante."""

from typing import List, Optional, Dict, Any
from modelos.producto import Producto


class Restaurante:
    """Servicio que administra las operaciones del restaurante."""
    
    def __init__(self) -> None:
        """Inicializa el servicio con colecciones vacías."""
        self._productos: List[Producto] = []
    
    def cargar_productos(self, productos: List[Producto]) -> None:
        """
        Carga una lista de productos reemplazando los existentes.
        
        Args:
            productos: Lista de productos a cargar
        """
        self._productos = productos.copy()
    
    def obtener_productos(self) -> List[Producto]:
        """
        Obtiene una copia de la lista de productos.
        
        Returns:
            Lista de productos
        """
        return self._productos.copy()
    
    def registrar_producto(self, producto: Producto) -> bool:
        """
        Registra un nuevo producto.
        
        Args:
            producto: Producto a registrar
            
        Returns:
            True si se registró correctamente, False si ya existe
            
        Raises:
            ValueError: Si el producto no es válido
        """
        if not isinstance(producto, Producto):
            raise ValueError("El objeto no es un producto válido")
        
        # Verificar si ya existe un producto con el mismo nombre
        if producto in self._productos:
            return False
        
        self._productos.append(producto)
        return True
    
    def buscar_producto(self, nombre: str) -> Optional[Producto]:
        """
        Busca un producto por nombre.
        
        Args:
            nombre: Nombre del producto a buscar
            
        Returns:
            Producto encontrado o None
        """
        nombre = nombre.strip().lower()
        for producto in self._productos:
            if producto.nombre.lower() == nombre:
                return producto
        return None
    
    def buscar_productos_por_categoria(self, categoria: str) -> List[Producto]:
        """
        Busca productos por categoría.
        
        Args:
            categoria: Categoría a buscar
            
        Returns:
            Lista de productos de esa categoría
        """
        categoria = categoria.strip().lower()
        return [
            p for p in self._productos
            if p.categoria.lower() == categoria
        ]
    
    def actualizar_producto(
        self,
        nombre_actual: str,
        nuevo_nombre: Optional[str] = None,
        nuevo_precio: Optional[float] = None,
        nueva_categoria: Optional[str] = None,
        nueva_descripcion: Optional[str] = None
    ) -> bool:
        """
        Actualiza un producto existente.
        
        Args:
            nombre_actual: Nombre actual del producto
            nuevo_nombre: Nuevo nombre (opcional)
            nuevo_precio: Nuevo precio (opcional)
            nueva_categoria: Nueva categoría (opcional)
            nueva_descripcion: Nueva descripción (opcional)
            
        Returns:
            True si se actualizó correctamente, False si no existe
            
        Raises:
            ValueError: Si los nuevos valores no son válidos
        """
        producto = self.buscar_producto(nombre_actual)
        if not producto:
            return False
        
        # Si se cambia el nombre, verificar que no exista otro
        if nuevo_nombre is not None:
            nuevo_nombre = nuevo_nombre.strip()
            if nuevo_nombre:
                # Verificar que no exista otro producto con el nuevo nombre
                for p in self._productos:
                    if p.nombre.lower() == nuevo_nombre.lower() and p != producto:
                        raise ValueError(f"Ya existe un producto con el nombre '{nuevo_nombre}'")
                
                # Actualizar el nombre
                setattr(producto, '_nombre', producto._validar_nombre(nuevo_nombre))
        
        if nuevo_precio is not None:
            setattr(producto, '_precio', producto._validar_precio(nuevo_precio))
        
        if nueva_categoria is not None:
            setattr(producto, '_categoria', producto._validar_categoria(nueva_categoria))
        
        if nueva_descripcion is not None:
            if nueva_descripcion == "":
                producto.descripcion = None
            else:
                producto.descripcion = nueva_descripcion.strip()
        
        return True
    
    def eliminar_producto(self, nombre: str) -> bool:
        """
        Elimina un producto por nombre.
        
        Args:
            nombre: Nombre del producto a eliminar
            
        Returns:
            True si se eliminó, False si no existe
        """
        producto = self.buscar_producto(nombre)
        if not producto:
            return False
        
        self._productos.remove(producto)
        return True
    
    def listar_productos(self) -> str:
        """
        Obtiene un listado formateado de todos los productos.
        
        Returns:
            String con el listado de productos
        """
        if not self._productos:
            return "No hay productos registrados."
        
        resultado = "=" * 50 + "\n"
        resultado += "LISTA DE PRODUCTOS\n"
        resultado += "=" * 50 + "\n"
        
        for i, producto in enumerate(self._productos, 1):
            resultado += f"{i}. {producto}\n"
        
        resultado += "=" * 50 + f"\nTotal: {len(self._productos)} productos"
        return resultado