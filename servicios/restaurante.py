from modelos import Producto, Bebida, Cliente

class Restaurante:
    def __init__(self):
        self.productos = []
        self.bebidas = []
        self.clientes = []

    # --- Productos ---
    def agregar_producto(self, nombre, precio, categoria="comida"):
        producto = Producto(nombre, precio, categoria)
        self.productos.append(producto)
        return producto

    def listar_productos(self):
        return self.productos

    # --- Bebidas ---
    def agregar_bebida(self, nombre, precio, tamaño, graduacion=0.0):
        bebida = Bebida(nombre, precio, tamaño, graduacion)
        self.bebidas.append(bebida)
        return bebida

    def listar_bebidas(self):
        return self.bebidas

    # --- Clientes ---
    def agregar_cliente(self, nombre, telefono, direccion=""):
        cliente = Cliente(nombre, telefono, direccion)
        self.clientes.append(cliente)
        return cliente

    def listar_clientes(self):
        return self.clientes