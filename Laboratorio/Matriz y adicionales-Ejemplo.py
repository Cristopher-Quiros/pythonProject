# Definir la matriz para representar los asientos del estadio
filas = 15
columnas = 15
estadio = [['O' for _ in range(columnas)] for _ in range(filas)]  # 'O' representa un asiento disponible

# Definir los precios de los asientos
precios = {
'O': 15000, 10000: 5000, 'X':0}

# 'O' representa asientos disponibles y 'X' representa asientos ocupados



# Variables para el registro de ventas
ventas_totales = 0
espectadores_registrados = []

# Función para mostrar el estado actual del estadio con precios
def mostrar_estadio():
    print("Estado actual del estadio:")
    for i, fila in enumerate(estadio):
        for j, asiento in enumerate(fila):
            precio = precios[asiento]
            print(f'{i+1}-{j+1} (${precio})', end='  ')
        print()

# Función para verificar si un asiento está reservado
def asiento_reservado(fila, columna):
    return estadio[fila][columna] == 'X'

# Función para vender boletos y asignar asientos
def vender_boletos():
    global ventas_totales
    fila = int(input("Ingrese el número de fila: ")) - 1
    columna = int(input("Ingrese el número de columna: ")) - 1

    if asiento_reservado(fila, columna):
        print("Lo siento, este asiento ya está ocupado.")
    else:
        estadio[fila][columna] = 'X'
        print("¡Boleto vendido con éxito!")
        ventas_totales += precios['X']
        espectadores_registrados.append((fila, columna))

# Función para generar el reporte de ventas
def reporte_ventas():
    print("Reporte de ventas:")
    print("Total de ingresos:", ventas_totales)
    print("Lista de asientos vendidos:")
    for fila, columna in espectadores_registrados:
        print("Fila:", fila+1, "- Columna:", columna+1)

# Menú principal
def menu():
    while True:
        print("\nBienvenido al sistema de gestión de asientos del estadio:")
        print("1. Mostrar estado del estadio")
        print("2. Vender boletos")
        print("3. Generar reporte de ventas")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            mostrar_estadio()
        elif opcion == '2':
            vender_boletos()
        elif opcion == '3':
            reporte_ventas()
        elif opcion == '4':
            print("¡Gracias por utilizar nuestro sistema!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

# Ejecutar el programa
menu()
