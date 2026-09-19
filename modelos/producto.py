"""Módulo que contiene la clase Producto."""

from typing import Dict, Any


class Producto:
    """Clase que representa un producto del restaurante."""
    
    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int = 0
    ) -> None:
        """Inicializa un nuevo producto."""
        self.codigo = self._validar_codigo(codigo)
        self.nombre = self._validar_nombre(nombre)
        self.categoria = self._validar_categoria(categoria)
        self.precio = self._validar_precio(precio)
        self.stock = self._validar_stock(stock)
    
    def _validar_codigo(self, codigo: str) -> str:
        if not codigo or not codigo.strip():
            raise ValueError("El código del producto no puede estar vacío")
        return codigo.strip().upper()
    
    def _validar_nombre(self, nombre: str) -> str:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        return nombre.strip()
    
    def _validar_categoria(self, categoria: str) -> str:
        if not categoria or not categoria.strip():
            raise ValueError("La categoría no puede estar vacía")
        return categoria.strip().lower()
    
    def _validar_precio(self, precio: float) -> float:
        try:
            precio = float(precio)
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un número válido")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return precio
    
    def _validar_stock(self, stock: int) -> int:
        try:
            stock = int(stock)
        except (ValueError, TypeError):
            raise ValueError("El stock debe ser un número entero")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        return stock
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el producto a diccionario."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Producto":
        """Crea un producto desde un diccionario."""
        return cls(
            codigo=data.get("codigo", ""),
            nombre=data.get("nombre", ""),
            categoria=data.get("categoria", ""),
            precio=data.get("precio", 0.0),
            stock=data.get("stock", 0)
        )
    
    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} ({self.categoria}) - ${self.precio:.2f} - Stock: {self.stock}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Producto):
            return False
        return self.codigo == other.codigo
    
    def __hash__(self) -> int:
        return hash(self.codigo)