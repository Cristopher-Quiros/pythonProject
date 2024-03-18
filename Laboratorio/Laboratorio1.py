

class S:
    def __init__(self):
        self.estadio = "Estadio Ejemplo"
        self.precios_asientos = {
            "VIP": 100,
            "Platea": 80,
            "General": 50
        }
        self.espectadores = {}
        self.ventas = {}

    def mostrar_menu(self):
        while True:
            print("Bienvenido al Sistema de Venta de Entradas")
            print("1. Registrar espectador")
            print("2. Comprar entrada")
            print("3. Reporte de ventas")
            print("4. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.registrar_espectador()
            elif opcion == "2":
                self.comprar_entrada()
            elif opcion == "3":
                self.reporte_ventas()
            elif opcion == "4":
                print("Gracias por usar el sistema de venta de entradas")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

        def registrar_espectador(self):
            nombre_espectador = input("Ingrese el nombre del espectador: ")
            edad_espectador = input("Ingrese la edad del espectador: ")
            self.espectadores[nombre_espectador] = edad_espectador
            print(f"Espectador {nombre_espectador} registrado correctamente.")

        def comprar_entrada(self):
            nombre_espectador = input("Ingrese el nombre del espectador que desea comprar una entrada: ")
            if nombre_espectador in self.espectadores:
                print("Opciones de asientos disponibles:")
                for asiento, precio in self.precios_asientos.items():
                    print(f"{asiento}: ${precio}")
                    asiento_elegido = input("Seleccione el tipo de asiento que desea comprar: ")
                    if asiento_elegido in self.precios_asientos:
                        monto = self.precios_asientos[asiento_elegido]
                        self.ventas[nombre_espectador] = monto
                        print(f"Entrada comprada correctamente para {nombre_espectador}. Monto: ${monto}")
                    else:
                        print("Tipo de asiento inválido. Intente nuevamente.")
                else:
                    print("Espectador no registrado. Registre al espectador antes de comprar una entrada.")

                def reporte_ventas(self):
                    total_ventas = sum(self.ventas.values())
                    print("Reporte de Ventas:")
                    for espectador, monto in self.ventas.items():
                        print(f"{espectador}: ${monto}")
                    print(f"Total de ventas: ${total_ventas}")
# Uso del SistemaVentaEntradas
sistema = SistemaVentaEntradas()
sistema.mostrar_menu()
11616516

