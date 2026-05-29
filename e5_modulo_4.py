"""

Grupo: Fernández, Mobiglia, Rodríguez Potel

"""

#   Módulo 4:

"""
CASOS DE PRUEBA MÓDULO 4:

Sean:
pacientes_del_dia: [(23456789, 'Fernández', 'Joaquín', '2345-6789', 1), (12345678, 'Mobiglia', 'Santiago', '1234-5678', 2), (34567890, 'Rodríguez', 'Lautaro', '0000-0001', 1)]

franjas: ['10:00', '10:30', '11:00', '11:30', '12:00']

disponibilidad: {23456789: ['11:00', '12:30'], 12345678: ['9:30','10:00'], 34567890: ['11:30', '12:00']}


Casos:

Normal: Devuelve asignación.
asignación: {
            '11:00': (23456789, 'Fernández', 'Joaquín', '2345-6789', 1),
            '10:00': (12345678, 'Mobiglia', 'Santiago', '1234-5678', 2),
            '11:30': (34567890, 'Rodríguez', 'Lautaro', '0000-0001', 1)
            }

Normal: Todos los horarios estaban ocupados. Devuelve asignación.
Ejemplo:
pacientes_del_dia: [(23456789, 'Fernández', 'Joaquín', '2345-6789', 1), (12345678, 'Mobiglia', 'Santiago', '1234-5678', 2)]
franjas: ['10:00', '10:30']
disponibilidad: {23456789: ['10:00'], 12345678: ['10:30']}
asginación: {
            '10:00': (23456789, 'Fernández', 'Joaquín', '2345-6789', 1),
            '10:30':  (12345678, 'Mobiglia', 'Santiago', '1234-5678', 2)
}


Límite: Lista de pacientes vacía. Devuelve asignación porque cumple con el caso base de la recursión.
asignación: {}

Límite: Dos pacientes con horarios de su disponibilidad compartida. Devuelve asignación.
disponibilidad: {23456789: ['10:00','13:00','13:30'], 12345678: ['10:00', '11:00'], 34567890: ['11:30']}
asignación: {
            '10:00': (23456789, 'Fernández', 'Joaquín', '2345-6789', 1),
            '11:00': (12345678, 'Mobiglia', 'Santiago', '1234-5678', 2),
            '11:30': (34567890, 'Rodríguez', 'Lautaro', '0000-0001', 1)
            }

Límite: Un solo paciente y un único horario de franja. Devuelve asignación.
pacientes_del_dia: [(23456789, 'Fernández', 'Joaquín', '2345-6789', 1)]
franjas: ['10:00']
disponibilidad: {23456789: ['10:00']}
asignación: {
            '10:00': (23456789, 'Fernández', 'Joaquín', '2345-6789', 1)
            }

Límite: Lista franjas vacía. Devuelve None.

Límite: Diccionario disponibilidad vacío. Devuelve None.



Extremo: Pacientes con disponibilidad fuera de la franja. Devuelve None porque todos los horarios deben estar dentro.

Extremo: Lista vacía de franjas de disponibilidad. Devuelve None porque deben tener un horario especificado.

Extremo: Pacientes con la disponibilidad exactamente igual entre sí. Devuelve None porque todos deben ser capaces de tomar un turno.

Extremo: Más pacientes que la cantidad de horarios de las franjas. Devuelve None porque, al igual que el anterior, todos los pacientes deben tomar un turno.

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
