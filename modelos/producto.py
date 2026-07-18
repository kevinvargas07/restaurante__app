class Producto:
    def __init__(self, nombre, precio, categoria="comida"):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    def __str__(self):
        return f"{self.nombre} ({self.categoria}) - ${self.precio:.2f}"