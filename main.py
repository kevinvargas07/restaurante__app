from servicios import Restaurante

def mostrar_menu():
    print("\n--- RESTAURANTE APP ---")
    print("1. Agregar producto")
    print("2. Agregar bebida")
    print("3. Agregar cliente")
    print("4. Listar productos")
    print("5. Listar bebidas")
    print("6. Listar clientes")
    print("7. Salir")
    return input("Seleccione una opción: ")

def main():
    restaurante = Restaurante()

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio: "))
            categoria = input("Categoría (opcional, presione Enter para 'comida'): ") or "comida"
            restaurante.agregar_producto(nombre, precio, categoria)
            print("Producto agregado.")

        elif opcion == "2":
            nombre = input("Nombre de la bebida: ")
            precio = float(input("Precio: "))
            tamaño = input("Tamaño (ej. 500ml): ")
            graduacion = float(input("Graduación alcohólica (0 si no aplica): ") or 0)
            restaurante.agregar_bebida(nombre, precio, tamaño, graduacion)
            print("Bebida agregada.")

        elif opcion == "3":
            nombre = input("Nombre del cliente: ")
            telefono = input("Teléfono: ")
            direccion = input("Dirección (opcional): ")
            restaurante.agregar_cliente(nombre, telefono, direccion)
            print("Cliente agregado.")

        elif opcion == "4":
            print("\n--- LISTA DE PRODUCTOS ---")
            for p in restaurante.listar_productos():
                print(p)

        elif opcion == "5":
            print("\n--- LISTA DE BEBIDAS ---")
            for b in restaurante.listar_bebidas():
                print(b)

        elif opcion == "6":
            print("\n--- LISTA DE CLIENTES ---")
            for c in restaurante.listar_clientes():
                print(c)

        elif opcion == "7":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()