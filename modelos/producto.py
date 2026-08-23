"""Módulo que contiene la clase Producto."""

from typing import Optional, Dict, Any


class Producto:
    """Clase que representa un producto del restaurante."""
    
    def __init__(
        self,
        nombre: str,
        precio: float,
        categoria: str,
        descripcion: Optional[str] = None
    ) -> None:
        """
        Inicializa un nuevo producto.
        
        Args:
            nombre: Nombre del producto
            precio: Precio del producto
            categoria: Categoría del producto
            descripcion: Descripción opcional del producto
            
        Raises:
            ValueError: Si los valores no son válidos
        """
        self.nombre = self._validar_nombre(nombre)
        self.precio = self._validar_precio(precio)
        self.categoria = self._validar_categoria(categoria)
        self.descripcion = descripcion
    
    def _validar_nombre(self, nombre: str) -> str:
        """Valida que el nombre no esté vacío."""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        return nombre.strip()
    
    def _validar_precio(self, precio: float) -> float:
        """Valida que el precio sea positivo."""
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return precio
    
    def _validar_categoria(self, categoria: str) -> str:
        """Valida que la categoría no esté vacía."""
        if not categoria or not categoria.strip():
            raise ValueError("La categoría del producto no puede estar vacía")
        return categoria.strip()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el producto a un diccionario para serialización JSON.
        
        Returns:
            Diccionario con los datos del producto
        """
        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "descripcion": self.descripcion
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Producto':
        """
        Crea un producto a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos del producto
            
        Returns:
            Instancia de Producto
            
        Raises:
            KeyError: Si faltan campos obligatorios
            ValueError: Si los datos no son válidos
        """
        nombre = data.get("nombre")
        precio = data.get("precio")
        categoria = data.get("categoria")
        descripcion = data.get("descripcion")
        
        if nombre is None:
            raise KeyError("Falta el campo 'nombre'")
        if precio is None:
            raise KeyError("Falta el campo 'precio'")
        if categoria is None:
            raise KeyError("Falta el campo 'categoria'")
        
        return cls(nombre, precio, categoria, descripcion)
    
    def __str__(self) -> str:
        """Representación en string del producto."""
        desc = f" - {self.descripcion}" if self.descripcion else ""
        return f"{self.nombre} (${self.precio:.2f}) - {self.categoria}{desc}"
    
    def __eq__(self, other: object) -> bool:
        """Compara dos productos por nombre."""
        if not isinstance(other, Producto):
            return False
        return self.nombre.lower() == other.nombre.lower()
    
    def __hash__(self) -> int:
        """Permite usar productos en conjuntos."""
        return hash(self.nombre.lower())