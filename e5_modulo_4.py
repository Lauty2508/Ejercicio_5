"""

Grupo: Fernández, Mobiglia, Rodríguez Potel

"""

#   Módulo 4:

"""
    CASOS DE PRUEBA MÓDULO 4:

    Sean:
    pacientes_del_dia: [(11111111, 'Perez', 'Ana', '1111', 1), (22222222, 'Gomez', 'Blas', '2222', 2), (33333333, 'Lopez', 'Cloe', '3333', 3)]
    
    franjas: ['10:00', '10:30', '11:00']

    Casos:

    Normal (Con resolución de conflicto): Devuelve asignación.
    disponibilidad: {11111111: ['10:00', '10:30'], 22222222: ['10:00'], 33333333: ['10:30', '11:00']}
    asignación: {
                '10:30': (11111111, 'Perez', 'Ana', '1111', 1),
                '10:00': (22222222, 'Gomez', 'Blas', '2222', 2),
                '11:00': (33333333, 'Lopez', 'Cloe', '3333', 3)
                }

    Extremo (Sobre-restringido): Pacientes con la disponibilidad exactamente igual entre sí. Devuelve None porque todos deben ser capaces de tomar un turno y hay un embotellamiento imposible.
    disponibilidad: {11111111: ['10:00'], 22222222: ['10:00'], 33333333: ['10:00']}
    asignación: None
    """



# =====================================================
#                     FUNCIONES
#======================================================



def asignar_agenda(pacientes_del_dia, franjas, disponibilidad):
    """Asigna a cada paciente un turno en cada franja horaria mediante backtracking. Cada franja recibe como máximo a un paciente y cada paciente queda en una franja compatible con su disponibilidad.

    Precondición: pacientes_del_dia es una lista de tuplas con la forma (dni, apellido, nombre, telefono, prioridad), franjas es una lista que contiene los horarios y disponibilidad es un diccionario (clave: dni, valor: lista de franjas disponibles).
    Postcondición: devuelve una asignación válida si la hay, sino devuelve None."""

    #PRÓLOGO: estructuras iniciales para el backtracking
    asignacion = {}

    #RESOLUCIÓN: delega la asignación al algoritmo recursivo
    existe = _verificar_asignacion(pacientes_del_dia, franjas, disponibilidad, asignacion)

    #EPÍLOGO: devuelve una asignación válida o None
    return asignacion if existe else None

def _verificar_asignacion(pacientes, franjas, disponibilidad, asignacion, indice = 0):
    """Verifica de manera recursiva que haya una asignación válida.
    
    Precondición: pacientes, franjas y disponibilidad son los del problema. Asignación es un diccionario vacío.
    Postcondición: devuelve True si existe una asignación válida o False si no."""

    # PRÓLOGO - caso base
    if indice == len(pacientes):
        return True
    
    #RESOLUCIÓN - caso recursivo
    paciente = pacientes[indice]
    dni = paciente[0]

    #Extrae las franjas horarias del diccionario disponibilidad. 
    # Si la clave no está devuelve una lista vacía
    franjas_compatibles = disponibilidad.get(dni, [])

    for franja in franjas:
        
        # Poda:
        # La franja debe concordar con la disponibilidad del paciente.
        # La franja no puede estar ocupada por otro paciente.
        if (franja in franjas_compatibles) and (franja not in asignacion):
            asignacion[franja] = paciente

            if _verificar_asignacion(pacientes, franjas, disponibilidad, asignacion, indice + 1):
                return True 
        
            # Back-track
            del asignacion[franja]

    return False

# =====================================================
# EJECUCIÓN DE CASOS DE PRUEBA (PUNTO H)
# =====================================================
if __name__ == '__main__':
    print("==================================================")
    print("      PUNTO H: PRUEBAS DE BACKTRACKING")
    print("==================================================")
    
    # Datos base para las pruebas
    pacientes_prueba = [
        (11111111, 'Perez', 'Ana', '1111', 1),
        (22222222, 'Gomez', 'Blas', '2222', 2),
        (33333333, 'Lopez', 'Cloe', '3333', 3)
    ]
    franjas_prueba = ['10:00', '10:30', '11:00']

    # -----------------------------------------------------------------
    # 1. Probando caso CON solución
    # -----------------------------------------------------------------
    print("\n1. Probando caso CON solución...")
    disp_con_solucion = {
        11111111: ['10:00', '10:30'],
        22222222: ['10:00'],           # Blas solo puede a las 10:00
        33333333: ['10:30', '11:00']
    }
    
    resultado_sol = asignar_agenda(pacientes_prueba, franjas_prueba, disp_con_solucion)
    print(f"Asignación obtenida:")
    for f, p in resultado_sol.items():
        print(f"  {f} -> {p[1]}, {p[2]} (DNI: {p[0]})")
    
    # Verificación estricta de restricciones exigida por la consigna
    assert resultado_sol is not None, "Error: Debería haber encontrado una solución." #si no encuentra solucion imprime este mensaje y para todas las pruebas, si no continua.
    
    franjas_usadas = set()
    for franja, paciente in resultado_sol.items():
        dni_paciente = paciente[0]
        
        # Restricción 1: Cada franja recibe a lo sumo un paciente.
        # (Al usar un diccionario, la unicidad de las claves y el set lo garantizan)
        assert franja not in franjas_usadas, f"Error: La franja {franja} está duplicada." #recorre las franjas de la solucion, y las va ahregando a franjas usadas, si alguna esta repetida para todo e imprime ese mensaje mostrando que franja se uso dos veces, lo cual es imposible ya que en la solucion debe haber una franja distinta por paciente.
        franjas_usadas.add(franja)
        
        # Restricción 2: Cada paciente queda en una franja compatible.
        assert franja in disp_con_solucion[dni_paciente], f"Error: {franja} no es compatible para el DNI {dni_paciente}." #se fija que la franja que se le asigno al paciente este dentro de sus franjas disponibles.
    
    print("-> OK: La asignación respeta todas las restricciones (1 paciente por franja y horarios compatibles).")


    # -----------------------------------------------------------------
    # 2. Probando caso SOBRE-RESTRINGIDO (sin solución)
    # -----------------------------------------------------------------
    print("\n2. Probando caso SOBRE-RESTRINGIDO (sin solución)...")
    # Los 3 pacientes solo pueden a las 10:00, creando un embotellamiento imposible
    disp_sin_solucion = {
        11111111: ['10:00'],
        22222222: ['10:00'],
        33333333: ['10:00']
    }
    
    resultado_sin_sol = asignar_agenda(pacientes_prueba, franjas_prueba, disp_sin_solucion)
    print(f"Asignación obtenida: {resultado_sin_sol}")
    
    assert resultado_sin_sol is None, "Error: Debería devolver None porque no hay solución posible."
    print("-> OK: El algoritmo detectó correctamente que no existe solución válida.")


    # -----------------------------------------------------------------
    # 3. Discusión Teórica (Impresa por consola para el informe)
    # -----------------------------------------------------------------
    print("\n==================================================")
    print("                DISCUSIÓN TEÓRICA")
    print("==================================================")
    discusion = """
Análisis de la Fuerza Bruta:
Un enfoque de fuerza bruta pura consiste en generar combinaciones a ciegas. 
Si tenemos M franjas horarias y N pacientes, el algoritmo construiría todas 
las agendas posibles asignando cualquier franja a cualquier paciente de forma 
exhaustiva, lo que genera un árbol de combinaciones de tamaño M^N. La fuerza 
bruta requiere construir estos árboles completos (agendas enteras) y recién 
al final de la ejecución analizar si cada configuración es válida (es decir, 
si no hay franjas repetidas y si respeta la disponibilidad). Esto implica 
un costo computacional masivo e ineficiente.

Análisis del Backtracking con Poda:
A diferencia de la fuerza bruta, el algoritmo implementado utiliza 
backtracking con poda para construir la agenda de forma incremental. En lugar 
de crear secuencias completas y validarlas al final, el programa evalúa las 
restricciones (que el horario esté libre y sea compatible con el paciente) 
en cada paso intermedio.

Si al intentar asignar un turno a un paciente se detecta un choque de horarios 
o una incompatibilidad, el algoritmo reconoce el error prematuramente y descarta 
esa rama completa (poda). Al hacer esto, evita generar y evaluar todos los 
múltiples sub-árboles (combinaciones futuras) que derivarían de esa mala decisión 
inicial. Si el camino no tiene salida, el algoritmo retrocede (backtrack), 
limpia el estado actual y prueba una nueva alternativa. Como resultado, el 
único camino que el algoritmo completa desde la raíz hasta la última hoja es 
una asignación 100% válida, reduciendo drásticamente el tiempo de procesamiento.
"""
    print(discusion)