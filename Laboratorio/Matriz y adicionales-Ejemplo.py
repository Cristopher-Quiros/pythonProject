# Representar la matriz para los asientos del estadio

filas = 15
columnas = 15
estadio = [['0' for _ in range(columnas)] for _ in range(filas)]


# Función para mostrar el estado actual del estadio
def mostrar_estadio():
    print("Estado actual del estadio:")
    for fila in estadio:
        print(' '.join(fila))


# Función para vender boletos y asignar asientos
def vender_boletos():
    fila = int(input("Ingrese el número de fila: "))
    columna = int(input("Ingrese el número de columna: "))

    if estadio[fila][columna] == 'X':
        print("Lo siento, este asiento ya está ocupado.")
    else:
        estadio[fila][columna] = 'X'
        print("¡Boleto vendido con éxito!")


# Menú principal
def menu():
    while True:
        print("\nBienvenido al sistema de gestión de asientos del estadio:")
        print("1. Mostrar estado del estadio")
        print("2. Vender boletos")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            mostrar_estadio()
        elif opcion == '2':
            vender_boletos()
        elif opcion == '3':
            print("¡Gracias por utilizar nuestro sistema!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")


# Ejecutar el programa
menu()
