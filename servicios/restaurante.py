from typing import List, Optional, Set
from modelos import Producto, Usuario

class Restaurante:
    def __init__(self):
        self.productos: List[Producto] = []
        self.usuarios: List[Usuario] = []

    # --- PRODUCTOS ---
    def registrar_producto(self, codigo: str, nombre: str, categoria: str, precio: float) -> bool:
        if any(p.codigo == codigo for p in self.productos):
            return False
        self.productos.append(Producto(codigo, nombre, categoria, precio))
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        for p in self.productos:
            if p.codigo == codigo:
                return p
        return None

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self.productos.remove(producto)
        return True

    def listar_productos(self) -> List[Producto]:
        return self.productos

    def obtener_categorias_unicas(self) -> Set[str]:
        return {p.categoria for p in self.productos}

    # --- USUARIOS ---
    def registrar_usuario(self, identificacion: str, nombre: str, correo: str) -> bool:
        if any(u.identificacion == identificacion for u in self.usuarios):
            return False
        self.usuarios.append(Usuario(identificacion, nombre, correo))
        return True

    def listar_usuarios(self) -> List[Usuario]:
        return self.usuarios