from .producto import Producto

class Bebida(Producto):
    def __init__(self, nombre, precio, tamaño, graduacion=0.0):
        super().__init__(nombre, precio, categoria="bebida")
        self.tamaño = tamaño
        self.graduacion = graduacion

    def __str__(self):
        return f"{self.nombre} ({self.tamaño}, {self.graduacion}% alc.) - ${self.precio:.2f}"