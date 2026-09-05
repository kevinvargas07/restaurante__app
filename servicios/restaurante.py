from typing import List, Optional, Set, Dict
from modelos import Producto, Usuario, Venta
from .archivo_servicio import ArchivoServicio

class Restaurante:
    def __init__(self):
        # Colecciones principales (listas)
        self.productos: List[Producto] = []
        self.usuarios: List[Usuario] = []
        self.ventas: List[Venta] = []
        
        # Índices auxiliares (diccionarios para búsquedas eficientes)
        self.indice_productos: Dict[str, Producto] = {}
        self.indice_usuarios: Dict[str, Usuario] = {}
        self.ventas_por_usuario: Dict[str, List[Venta]] = {}
        
        # Cargar datos desde JSON al iniciar
        self._cargar_datos()

    def _cargar_datos(self) -> None:
        """Carga datos desde JSON y reconstruye índices"""
        self.productos = ArchivoServicio.cargar_productos()
        self.usuarios = ArchivoServicio.cargar_usuarios()
        self.ventas = ArchivoServicio.cargar_ventas()
        
        # Reconstruir índices
        self._reconstruir_indices()

    def _reconstruir_indices(self) -> None:
        """Reconstruye todos los índices auxiliares"""
        # Índice de productos por código
        self.indice_productos = {p.codigo: p for p in self.productos}
        
        # Índice de usuarios por identificación
        self.indice_usuarios = {u.identificacion: u for u in self.usuarios}
        
        # Índice de ventas por usuario
        self.ventas_por_usuario = {}
        for venta in self.ventas:
            if venta.identificacion_usuario not in self.ventas_por_usuario:
                self.ventas_por_usuario[venta.identificacion_usuario] = []
            self.ventas_por_usuario[venta.identificacion_usuario].append(venta)

    def _guardar_datos(self) -> None:
        """Guarda todos los datos en archivos JSON"""
        ArchivoServicio.guardar_productos(self.productos)
        ArchivoServicio.guardar_usuarios(self.usuarios)
        ArchivoServicio.guardar_ventas(self.ventas)

    # --- PRODUCTOS ---
    def registrar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int = 0) -> bool:
        if codigo in self.indice_productos:
            return False
        producto = Producto(codigo, nombre, categoria, precio, stock)
        self.productos.append(producto)
        self.indice_productos[codigo] = producto
        self._guardar_datos()
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        # Búsqueda O(1) mediante índice
        return self.indice_productos.get(codigo)

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int = None) -> bool:
        producto = self.indice_productos.get(codigo)
        if producto is None:
            return False
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        if stock is not None:
            producto.stock = stock
        self._guardar_datos()
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.indice_productos.get(codigo)
        if producto is None:
            return False
        self.productos.remove(producto)
        del self.indice_productos[codigo]
        self._guardar_datos()
        return True

    def listar_productos(self) -> List[Producto]:
        return self.productos

    def obtener_categorias_unicas(self) -> Set[str]:
        # Uso de set para obtener categorías únicas
        return {p.categoria for p in self.productos}

    # --- USUARIOS ---
    def registrar_usuario(self, identificacion: str, nombre: str, correo: str) -> bool:
        if identificacion in self.indice_usuarios:
            return False
        usuario = Usuario(identificacion, nombre, correo)
        self.usuarios.append(usuario)
        self.indice_usuarios[identificacion] = usuario
        self._guardar_datos()
        return True

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        # Búsqueda O(1) mediante índice
        return self.indice_usuarios.get(identificacion)

    def listar_usuarios(self) -> List[Usuario]:
        return self.usuarios

    # --- VENTAS ---
    def registrar_venta(self, codigo_venta: str, identificacion_usuario: str, items: List[Dict]) -> bool:
        # Validar que el usuario existe
        if identificacion_usuario not in self.indice_usuarios:
            return False
        
        # Validar stock y calcular total
        total = 0.0
        for item in items:
            producto = self.indice_productos.get(item["codigo_producto"])
            if producto is None:
                return False
            if producto.stock < item["cantidad"]:
                return False
            total += producto.precio * item["cantidad"]
        
        # Actualizar stock
        for item in items:
            producto = self.indice_productos[item["codigo_producto"]]
            producto.stock -= item["cantidad"]
        
        # Crear y registrar venta
        venta = Venta(codigo_venta, identificacion_usuario, items, total)
        self.ventas.append(venta)
        
        # Actualizar índice de ventas por usuario
        if identificacion_usuario not in self.ventas_por_usuario:
            self.ventas_por_usuario[identificacion_usuario] = []
        self.ventas_por_usuario[identificacion_usuario].append(venta)
        
        self._guardar_datos()
        return True

    def consultar_ventas_por_usuario(self, identificacion_usuario: str) -> List[Venta]:
        # Consulta O(1) mediante índice de ventas por usuario
        return self.ventas_por_usuario.get(identificacion_usuario, [])

    def listar_ventas(self) -> List[Venta]:
        return self.ventas