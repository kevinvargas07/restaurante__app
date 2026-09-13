from typing import List, Optional
from modelos import Producto, Usuario
from .archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self):
        self.productos: List[Producto] = []
        self.usuarios: List[Usuario] = []
        self._cargar_datos()

    def _cargar_datos(self) -> None:
        """Carga productos y usuarios desde los archivos JSON"""
        self.productos = ArchivoServicio.cargar_productos()
        self.usuarios = ArchivoServicio.cargar_usuarios()

    def validar_acceso(self, identificacion: str, contrasena: str) -> Optional[Usuario]:
        """Valida las credenciales del usuario. Retorna el Usuario si es correcto."""
        for usuario in self.usuarios:
            if usuario.identificacion == identificacion and usuario.contrasena == contrasena:
                return usuario
        return None

    def listar_usuarios(self) -> List[Usuario]:
        return self.usuarios

    def listar_productos(self) -> List[Producto]:
        return self.productos

    def cantidad_usuarios(self) -> int:
        return len(self.usuarios)

    def cantidad_productos(self) -> int:
        return len(self.productos)