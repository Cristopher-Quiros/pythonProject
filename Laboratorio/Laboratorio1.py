import random
from colorama import Fore, Style
import os
import json
from datetime import datetime

# Variables globales
cancha = [['' for _ in range(10)] for _ in range(10)]
MAX_OCUPADOS = 15

# Precios de los asientos
PRECIOS = {
    'fila_1_4': 5000,
    'fila_5_7': 10000,
    'fila_8_10': 15000
}

# Generar los campos ocupados
def AsientosOcupados():
    asientos_ocupados = 0
    while asientos_ocupados < MAX_OCUPADOS:
        fila = random.randint(0, 9)
        columna = random.randint(0, 9)
        if not cancha[fila][columna].endswith(Style.RESET_ALL):
            cancha[fila][columna] = Fore.RED + 'X' + Style.RESET_ALL
            asientos_ocupados += 1

# Generar la matriz con los asientos
def CrearCancha():
    for i in range(10):
        for j in range(10):
            fila = i + 1
            asiento = f"{str(fila)}{chr(65 + j)}"  # chr convierte el código ASCII a letras
            cancha[i][j] = asiento
    AsientosOcupados()

# Imprimir matriz de asientos
def MostrarCancha():
    print("  " + " ".join([chr(65 + j) for j in range(10)]))
    for i in range(10):
        print(str(i + 1) + " " + " ".join(cancha[i]))

# Mostrar precios de los asientos
def MostrarPreciosAsientos():
    print("\nPrecios de los Asientos:")
    print("Asientos de líneas 1 - 4: 5000 colones")
    print("Asientos de líneas 5 - 7: 10000 colones")
    print("Asientos de líneas 8 - 10: 15000 colones")

# Registro de espectadores
def RegistroEspectador():
    print("\nRegistro de Espectador")
    while True:
        cedula = input("Ingrese su número de cédula (9 dígitos): ")
        if cedula.isdigit() and len(cedula) == 9:
            break
        else:
            print("La cédula debe contener exactamente 9 números.")

    # Verificar si el usuario ya está registrado
    for comprador in compradores:
        if comprador["cedula"] == cedula:
            print("El usuario ya está registrado.")
            return

    while True:
        nombre = input("Ingrese su nombre: ")
        if nombre.isalpha():
            break
        else:
            print("El nombre solo puede contener letras.")

    while True:
        genero = input("Ingrese su género (M/F): ").upper()
        if genero == 'M' or genero == 'F':
            break
        else:
            print("Género inválido. Ingrese 'M' para masculino o 'F' para femenino.")

    compradores.append({
        "cedula": cedula,
        "nombre": nombre,
        "genero": genero,
        "asientos_comprados": []
    })

    print("Registro exitoso.")

def cargar_compradores():
    try:
        with open("reporte_ventas.json", "r") as f:
            compradores = json.load(f)
    except FileNotFoundError:
        compradores = []
    return compradores

compradores = cargar_compradores()

# Guardar compra en JSON
def GuardarCompra(boletos_comprados, nombre_comprador):

    total_compra = 0  # Variable para almacenar el total de la compra
    for boleto in boletos_comprados:
        fila = int(boleto[0]) - 1
        columna = ord(boleto[1].upper()) - ord('A')

        for comprador in compradores:
            if comprador["nombre"] == nombre_comprador:
                # Calcular el precio del asiento
                if fila < 4:
                    precio_asiento = PRECIOS['fila_1_4']
                elif fila < 7:
                    precio_asiento = PRECIOS['fila_5_7']
                else:
                    precio_asiento = PRECIOS['fila_8_10']
                total_compra += precio_asiento  # Sumar al total de la compra

                comprador["asientos_comprados"].append({
                    "asiento": boleto,
                    "precio": precio_asiento,  # Registrar el precio del asiento
                    "fecha_compra": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

    # Guardar la información en un archivo JSON
    with open("reporte_ventas.json", "w") as f:
        json.dump(compradores, f, indent=4)

def CompraEntradas():
    print("\nCompra de Entradas")

    # Verificar si hay espectadores registrados
    if not compradores:
        print("No hay espectadores registrados. Por favor, regístrese primero.")
        input("Presione enter para continuar...")
        return

    # Solicitar número de cédula
    cedula = input("Ingrese su número de cédula (9 dígitos): ")

    # Verificar si el espectador ya está registrado
    nombre_comprador = ""
    for comprador in compradores:
        if comprador["cedula"] == cedula:
            nombre_comprador = comprador["nombre"]
            break

    if nombre_comprador == "":
        print("No se encontró un comprador registrado con esa cédula.")
        input("Presione enter para continuar...")
        return

    print(f"Bienvenido de nuevo, {nombre_comprador}.")

    # Solicitar cantidad de boletos a comprar
    cantidad_boletos = int(input("Ingrese la cantidad de boletos que desea comprar (1-3): "))
    if cantidad_boletos < 1 or cantidad_boletos > 3:
        print("Cantidad de boletos inválida.")
        input("Presione enter para continuar...")
        return

    # Lista para almacenar los boletos comprados
    boletos_comprados = []

    for i in range(cantidad_boletos):
        while True:
            fila = int(input(f"Ingrese la fila del boleto {i + 1} (1-10): "))
            columna = input(f"Ingrese la columna del boleto {i + 1} (A-J): ")

            # Validar fila y columna
            if fila < 1 or fila > 10 or columna.upper() < 'A' or columna.upper() > 'J':
                print("Asiento inválido.")
                continue

            # Verificar si el asiento está ocupado
            if not cancha[fila - 1][ord(columna.upper()) - ord('A')].endswith(Style.RESET_ALL):
                boletos_comprados.append((fila, columna))
                cancha[fila - 1][ord(columna.upper()) - ord('A')] = Fore.BLUE + 'X' + Style.RESET_ALL
                print("Asiento seleccionado con éxito.")
                break
            else:
                print("El asiento seleccionado está ocupado. Por favor, seleccione otro.")
                continue

    if len(boletos_comprados) == cantidad_boletos:
        total_compra = GuardarCompra(boletos_comprados, nombre_comprador)  # Registro de compra y obtención del total
        print(f"Compra realizada con éxito. Total de boletos: {cantidad_boletos}. Total de compra: {total_compra} colones.")
        input("Presione enter para continuar...")
    else:
        print("Se canceló la compra debido a asientos ocupados.")
        input("Presione enter para continuar...")

# Función para calcular el total de ingresos
def CalcularTotalIngresos():
    total_ingresos = sum([len(comprador['asientos_comprados']) for comprador in compradores])
    return total_ingresos

# Función para cargar el estado de los asientos desde el archivo JSON
def CargarEstadoAsientos():
    try:
        with open("reporte_ventas.json", "r") as f:
            try:
                compras = json.load(f)
                if compras:  # Verificar si hay datos en el archivo
                    for comprador in compras:
                        for asiento_comprado in comprador["asientos_comprados"]:
                            fila = int(asiento_comprado["asiento"][0]) - 1
                            columna = ord(asiento_comprado["asiento"][1].upper()) - ord('A')
                            cancha[fila][columna] = Fore.BLUE + 'X' + Style.RESET_ALL
                else:
                    print("El archivo reporte_ventas.json está vacío.")
            except json.decoder.JSONDecodeError:
                print("El archivo reporte_ventas.json está vacío o no contiene un formato JSON válido.")
    except FileNotFoundError:
        pass

def ImprimirReporteVentas():
    print("\nReporte de Ventas")

    # Contadores para el reporte
    boletos_hombres = sum(1 for comprador in compradores if comprador['genero'] == 'M')
    boletos_mujeres = sum(1 for comprador in compradores if comprador['genero'] == 'F')
    total_ingresos = sum(sum(asiento['precio'] for asiento in comprador['asientos_comprados']) for comprador in compradores)

    # Imprimir detalles de cada compra
    for comprador in compradores:
        print(f"Comprador: {comprador['nombre']} - Cédula: {comprador['cedula']} - Género: {comprador['genero']}")
        print("Detalles de compra:")
        for asiento in comprador["asientos_comprados"]:
            print(f"Asiento: {asiento['asiento'][0]}{asiento['asiento'][1]} - Precio: {asiento['precio']} colones")

    # Imprimir resumen
    print(f"Total de boletos vendidos: {sum(len(comprador['asientos_comprados']) for comprador in compradores)}")
    print(f"Total de boletos vendidos a hombres: {boletos_hombres}")
    print(f"Total de boletos vendidos a mujeres: {boletos_mujeres}")
    print(f"Total de ingresos: {total_ingresos} colones")

    # Guardar el reporte en un archivo JSON
    with open("reporte_ventas.json", "w") as f:
        json.dump(compradores, f, indent=4)


# Main app
CrearCancha()
CargarEstadoAsientos()

while True:
    os.system('cls')  # Limpiar la consola
    print("--------------------------------------------------")
    print("Bienvenido al Sistema".center(50))
    print("--------------------------------------------------")
    print("1. Visualizar estadio y precio de los asientos \n"
          + "2. Registro de espectadores \n"
          + "3. Compra de entradas \n"
          + "4. Reporte de Ventas \n"
          + "5. Salir")
    print("-------------------------------------------------")

    opc = input("Seleccione una opción: ")

    if opc == '1':
        os.system('cls')
        print("-----------------------------------------")
        print("Bienvenido al módulo de compras".center(40))
        print("-----------------------------------------")
        print("ASIENTOS DISPONIBLES".center(40))
        print("-----------------------------------------")
        MostrarCancha()
        MostrarPreciosAsientos()  # Mostrar precios de los asientos
        print("-----------------------------------------")
        input("Presione enter para continuar...")

    elif opc == '2':
        os.system('cls')
        RegistroEspectador()

    elif opc == '3':
        os.system('cls')
        CompraEntradas()

    elif opc == '4':
        os.system('cls')
        ImprimirReporteVentas()
        input("Presione enter para continuar...")

    elif opc == '5':
        os.system('cls')
        print("Sistema cerrado...")
        break

    else:
        os.system('cls')
        print("Opción Inválida")