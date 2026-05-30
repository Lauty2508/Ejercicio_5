"""
Grupo: Fernández, Mobiglia, Rodríguez Potel

PROGRAMA PRINCIPAL — INTEGRACIÓN FINAL
Este script actúa estrictamente como el orquestador del sistema, articulando
los 4 módulos a través de flujos de control claros, respetando la encapsulación
y minimizando las llamadas al sistema (E/S).
"""
# PROLOGO
import os
import time

from modulo_1 import crear_archivo_pacientes
from modulo_2 import construir_indices, buscar_por_dni
from e5_modulo_3 import listar_pacientes_ordenados  
from e5_modulo_4 import asignar_agenda          

RUTA_PACIENTES = "pacientes.bin"

# RESOLUCION 
def leer_pacientes(ruta):
    """
    Lee TODOS los pacientes de un archivo binario.

    Precondición: El archivo debe existir y tener el formato correcto. \n
    Postcondición: Devuelve una lista de tuplas con los datos de los pacientes.
    """
    # PROLOGO
    from modulo_1 import leer_paciente
    pacientes = []
    k = 0

    # RESOLUCIÓN
    with open(ruta, "rb") as archivo:
        while paciente is not None: # EOF o fuera de rango
            paciente = leer_paciente(archivo, k)
            pacientes.append(paciente)
            k += 1

    # EPÍLOGO
    return pacientes

def _crear_datos_iniciales():
    """Genera la base de datos inicial con los casos de prueba estándar."""
    
    #RESOLUCIÓN
    pacientes_iniciales = [
        (23456789, "Fernandez", "Joaquin", "2345-6789", 1),
        (12345678, "Mobiglia", "Santiago", "1234-5678", 2),
        (34567890, "Rodriguez", "Lautaro", "0000-0001", 1),
        (45678901, "Paz", "Ana", "1111-2222", 3),
    ]

    #EPÍLOGO
    crear_archivo_pacientes(RUTA_PACIENTES, pacientes_iniciales)

def _mostrar_lista_pacientes(pacientes):
    """Muestra la lista de pacientes si hay pacientes que mostrar.

    Precondición: pacientes es una lista de tuplas con la forma (dni, apellido, nombre, telefono, prioridad).
    """
    if not pacientes:
        print("No hay pacientes para mostrar.")
        return
    for p in pacientes:
        print(f"DNI: {p[0]} | {p[1]}, {p[2]} | Tel: {p[3]} | Prioridad: {p[4]}")

def _resolver_agenda():
    """Coordina la resolución de la agenda diaria delegando al Módulo 4.
    Precondición: El archivo de pacientes debe existir y tener datos. \n
    Postcondición: Imprime la asignación de turnos o un mensaje si no se pudo resolver."""

    # PROLOGO
    pacientes_del_dia = leer_pacientes(RUTA_PACIENTES)
    
    franjas = ["10:00", "10:30", "11:00", "11:30"]
    disponibilidad = {
        23456789: ["11:00", "11:30"],
        12345678: ["10:00"],
        34567890: ["10:30", "11:30"],
        45678901: ["10:30"],
    }

    # RESOLUCIÓN
    asignacion = asignar_agenda(pacientes_del_dia, franjas, disponibilidad)

    # EPÍLOGO
    if asignacion is None:
        print("\n[Aviso] No se pudo encontrar una asignación válida para la agenda.")
        return

    print("\n=== AGENDA DEL DÍA RESUELTA (BACKTRACKING) ===")
    for franja in sorted(asignacion):
        p = asignacion[franja]
        print(f"Horario {franja} -> {p[1]}, {p[2]} (DNI: {p[0]})")

def main():
    # PROLOGO
    opcion = ""
    if not os.path.exists(RUTA_PACIENTES):
        _crear_datos_iniciales()

    indice_por_dni, _ = construir_indices(RUTA_PACIENTES)
    print(f"Sistema inicializado. Se indexaron {len(indice_por_dni)} registros en memoria RAM.")

    # RESOLUCION
    # se abre el archivo una sola vez antes del loop
    with open(RUTA_PACIENTES, "rb") as archivo_binario:
        while opcion != "5":
            time.sleep(1) # delay para poder leer la respuesta antes de mostrar el menu

            print("\n" + "="*40)
            print("         MENÚ DE CONSULTAS")
            print("="*40)
            print("1. Buscar por DNI")
            print("2. Listar ordenado por Apellido")
            print("3. Listar ordenado por Prioridad")
            print("4. Resolver agenda del día")
            print("5. Salir")
            print("="*40)

            opcion = input("Seleccione una opción (1-5): ").strip()

            if opcion == "1":
                try:
                    dni = int(input("Ingrese DNI a buscar: ").strip())
                except ValueError:
                    print("[Error] El DNI debe ser un número entero.")
                    continue

                paciente = buscar_por_dni(archivo_binario, indice_por_dni, dni)
                if paciente:
                    print(f"\n[Encontrado] DNI: {paciente[0]} | {paciente[1]}, {paciente[2]} | Prioridad: {paciente[4]}")
                else:
                    print("\n[Aviso] El DNI no existe en el sistema.")

            elif opcion == "2":
                print("\nOrdenando por Apellido (Merge Sort estable)...")

                pacientes_ordenados = listar_pacientes_ordenados(RUTA_PACIENTES, "apellido")
                _mostrar_lista_pacientes(pacientes_ordenados)

            elif opcion == "3":
                print("\nOrdenando por Prioridad (Merge Sort estable)...")
            
                pacientes_ordenados = listar_pacientes_ordenados(RUTA_PACIENTES, "prioridad")
                _mostrar_lista_pacientes(pacientes_ordenados)

            elif opcion == "4":
                _resolver_agenda()

            elif opcion == "5":
                print("\nTerminando programa...")
            else:
                print("[Error] Opción inválida.")

#EPÍlOGO
if __name__ == "__main__":
    main()