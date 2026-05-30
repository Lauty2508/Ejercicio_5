"""
Grupo: Fernández, Mobiglia, Rodríguez Potel

CASOS DE PRUEBA MÓDULO 3:

Sea la lista de tuplas pacientes con la forma (dni, apellido, nombre, teléfono, prioridad):
[(12345678, 'Mobiglia', 'Santiago', '1234-5678', 2), (23456789, 'Fernández', 'Joaquín', '2345-6789', 1), (34567890, 'Rodríguez', 'Lautaro', '0000-0001', 1)]

Normal: (con criterio apellido, desempata por prioridad)
[(23456789, 'Fernández', 'Joaquín', '2345-6789', 1), (12345678, 'Mobiglia', 'Santiago', '1234-5678', 2), (34567890, 'Rodríguez', 'Lautaro', '0000-0001', 1)]

Normal: (con criterio prioridad, desempata por apellido)
[(23456789, 'Fernández', 'Joaquín', '2345-6789', 1), (34567890, 'Rodríguez', 'Lautaro', '0000-0001', 1), (12345678, 'Mobiglia', 'Santiago', '1234-5678', 2)]

Límite: (Para ambos tipos de criterio) - Sin registros en el archivo, devuelven listas vacías.
[]

Extremo: Si no se ingresa el criterio correctamente (por ejemplo: criterio = 'nombre') o si no se ingresa valor, no devuelve nada la función.

"""

import struct
from modulo_1 import TAM_REGISTRO, desempaquetar_paciente

#   MÓDULO 3:

def listar_pacientes_ordenados(ruta, criterio):
    """Ordena a los pacientes de la forma que se imponga con el criterio dado por parámetro (por apellido o por prioridad).
    Precondición: ruta es un archivo binario con registros. Criterio es la forma por la que se ordenará:
    por apellido y desempata por prioridad o por prioridad y desempata por apellido.
    Postcondición: devuelve una lista con los pacientes de forma ordenada."""

    #PRÓLOGO
    k = 0 
    pacientes = []

    #RESOLUCIÓN
    with open(ruta, 'rb') as archivo:
        datos = archivo.read(TAM_REGISTRO)

        while len(datos) == TAM_REGISTRO:
            paciente = desempaquetar_paciente(datos)
            pacientes.append(paciente)

            k += 1
            archivo.seek(k * TAM_REGISTRO)
            datos = archivo.read(TAM_REGISTRO)

    #EPÍLOGO
    if criterio == "apellido":
        pacientes_ordenados_apellido = ordenar_pacientes_apellido(pacientes)
        return pacientes_ordenados_apellido
    
    elif criterio == "prioridad":
        pacientes_ordenados_prioridad = ordenar_pacientes_prioridad(pacientes)
        return pacientes_ordenados_prioridad




#ORDENAMIENTO POR APELLIDO, DESEMPATE POR PRIORIDAD

def ordenar_pacientes_apellido(pacientes):
    """Ordena listas de tuplas con la forma (dni, apellido, nombre, telefono, prioridad) usando merge sort por apellido.
    Precondición: pacientes es una lista de tuplas.
    Postcondición: devuelve una nueva lista con los pacientes ordenados por apellido y desempatados por prioridad."""
    
    #PRÓLOGO - caso base
    if len(pacientes) <= 1:
        return list(pacientes)
    
    #RESOLUCIÓN - caso recursivo
    medio = len(pacientes) >> 1
    mitad_izq = ordenar_pacientes_apellido(pacientes[:medio])
    mitad_der = ordenar_pacientes_apellido(pacientes[medio:])
    pacientes_ordenados = _fusionar_apellido(mitad_izq, mitad_der)
    
    #EPÍLOGO
    return pacientes_ordenados

def _fusionar_apellido(izq, der):
    """Fusiona dos listas ordenadas por apellido en una sola lista ordenada.
    Precondición: izq y der están ordenadas en forma no decreciente.
    Postcondición: devuelve una nueva lista con todos los elementos
    de izq y der, en orden no decreciente y estable."""
    
    #PRÓLOGO
    resultado = []
    i = 0
    j = 0
    n_izq = len(izq)
    n_der = len(der)

    #RESOLUCIÓN
    while i < n_izq and j < n_der:

        #Ordena por apellido.
        if izq[i][1] < der[j][1]:
            resultado.append(izq[i])
            i += 1
        elif izq[i][1] > der[j][1]:
            resultado.append(der[j])
            j += 1

        #Desempata por prioridad.
        elif izq[i][4] <= der[j][4]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1

    resultado.extend(izq[i:])
    resultado.extend(der[j:])

    #EPÍLOGO
    return resultado




#ORDENAMIENTO POR PRIORIDAD, DESEMPATE POR APELLIDO

def ordenar_pacientes_prioridad(pacientes):
    """Ordena listas de tuplas con la forma (dni, apellido, nombre, telefono, prioridad) usando merge sort por prioridad. Desempata con el apellido.
    Precondición: pacientes es una lista de tuplas.
    Postcondición: devuelve una nueva lista con los pacientes ordenados por prioridad y desempatados por apellido."""
    
    #PRÓLOGO - caso base
    if len(pacientes) <= 1:
        return list(pacientes)
    
    #RESOLUCIÓN - caso recursivo
    medio = len(pacientes) >> 1
    mitad_izq = ordenar_pacientes_prioridad(pacientes[:medio])
    mitad_der = ordenar_pacientes_prioridad(pacientes[medio:])
    pacientes_ordenados = _fusionar_prioridad(mitad_izq, mitad_der)
    
    #EPÍLOGO
    return pacientes_ordenados

def _fusionar_prioridad(izq, der):
    """Fusiona dos listas ordenadas por prioridad en una sola lista ordenada.
    Precondición: izq y der están ordenadas en forma no decreciente.
    Postcondición: devuelve una nueva lista con todos los elementos
    de izq y der, en orden no decreciente y estable."""

    #PRÓLOGO
    resultado = []
    i = 0
    j = 0
    n_izq = len(izq)
    n_der = len(der)

    #RESOLUCIÓN
    while i < n_izq and j < n_der:

        #Ordena por prioridad.
        if izq[i][4] < der[j][4]:
            resultado.append(izq[i])
            i += 1
        elif izq[i][4] > der[j][4]:
            resultado.append(der[j])
            j += 1
        
        #Desempata por apellido.
        elif izq[i][1] <= der[j][1]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1

    resultado.extend(izq[i:])
    resultado.extend(der[j:])

    #EPÍLOGO
    return resultado



"""
RESPUESTA EJERCICIO F:

La estabilidad del algoritmo de ordenamiento es relevante para el criterio 'prioridad' porque, si no fuese
estable, se ordenaría únicamente por prioridad, haciendo que el orden impuesto por el otro criterio se pierda.

Por ejemplo: 
Pacientes (lista de tuplas con la forma (apellido, prioridad)): 
[(Mobiglia, 2), (Rodríguez, 1), (Fernández, 1)]

Primera pasada (ordenado por apellido):
[(Fernández, 1), (Mobiglia, 2), (Rodríguez, 1)]

Posible segunda pasada (ordenado por prioridad) de forma no estable:
[(Rodríguez, 1), (Fernández, 1), (Mobiglia, 2)]
Esto haría que aquellos que estén empatados por prioridad, pierdan su orden por apellido.

Segunda pasada (ordenado por prioridad) de forma estable:
[(Fernández, 1), (Rodríguez, 1), (Mobiglia, 2)]
Mantiene el orden por apellido entre pacientes con la misma prioridad.

"""
