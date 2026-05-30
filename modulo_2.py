"""
Grupo: Fernández, Mobiglia, Rodríguez Potel

CASOS DE PRUEBA MÓDULO 2:

Sea un archivo binario (ej: 'pacientes_test.bin') que contiene secuencialmente los siguientes registros empaquetados en las posiciones (k) indicadas:
k=0: (23456789, 'Fernández', 'Joaquín', '2345-6789', 1)
k=1: (12345678, 'Mobiglia', 'Santiago', '1234-5678', 2)
k=2: (34567890, 'Rodríguez', 'Lautaro', '0000-0001', 1)
k=3: (45678901, 'Fernández', 'Ana', '1111-2222', 3)  # Apellido repetido intencionalmente

Casos:

Normal: Construcción de índices a partir de un archivo válido. Devuelve los dos diccionarios con las posiciones k correctas.
indice_por_dni: {23456789: 0, 12345678: 1, 34567890: 2, 45678901: 3}
indice_por_apellido: {'Fernández': [0, 3], 'Mobiglia': [1], 'Rodríguez': [2]}

Normal: Búsqueda exitosa por DNI. Se pasa el archivo abierto, el índice y un DNI existente. Devuelve el registro correcto mediante acceso directo.
DNI buscado: 12345678
Retorna: (12345678, 'Mobiglia', 'Santiago', '1234-5678', 2)

Normal: Búsqueda de un paciente con un apellido que comparte con otros (para validar que el k en indice_por_dni apunta inequívocamente al paciente correcto).
DNI buscado: 45678901
Retorna: (45678901, 'Fernández', 'Ana', '1111-2222', 3)


Límite: Búsqueda por un DNI que no existe en el índice. Devuelve None, evitando el acceso innecesario a disco.
DNI buscado: 99999999
Retorna: None

Límite: Construcción de índices sobre un archivo binario existente pero vacío (0 bytes). Devuelve diccionarios vacíos.
Retorna: ({}, {})


Extremo: Intento de construir índices pasando una ruta de archivo que no existe. La función captura el caso y devuelve diccionarios vacíos (o lanza FileNotFoundError, según la implementación final).
Retorna: ({}, {})

Extremo: Búsqueda pasando un diccionario de índice vacío o None. Devuelve None porque el DNI lógicamente no se encontrará.

Extremo: Búsqueda pasando un tipo de dato incorrecto para el DNI (ej: un string '12345678' en lugar del entero 12345678). Devuelve None ya que las claves del diccionario fueron guardadas como enteros al desempaquetar.
"""

import struct
import os

from modulo_1 import TAM_REGISTRO, FORMATO, leer_paciente

# ==========================================
# MÓDULO 2 — ÍNDICES EN MEMORIA
# ==========================================

def construir_indices(ruta):
    """
    Recorre una sola vez el archivo binario y construye dos índices en memoria.
    
    Precondición: El archivo en la ruta debe existir y tener el formato de pacientes.
    Postcondición: Devuelve dos diccionarios (indice_por_dni, indice_por_apellido).
    
    Argumentos:
        ruta (str): La ruta al archivo binario de pacientes.
        
    Retorna:
        tuple: (indice_por_dni, indice_por_apellido)
            - indice_por_dni: dict con clave DNI (int) y valor k (posición del registro).
            - indice_por_apellido: dict con clave apellido (str) y valor lista de k's.
    """
    indice_por_dni = {}
    indice_por_apellido = {}
    
    # Verificamos si el archivo existe para evitar errores
    if not os.path.exists(ruta):
        return indice_por_dni, indice_por_apellido
        
    with open(ruta, 'rb') as archivo:
        k = 0  # Índice de posición del registro (0, 1, 2...)
        while True:
            registro_bytes = archivo.read(TAM_REGISTRO)
            
            # Condición de corte: llegamos al final del archivo
            if not registro_bytes or len(registro_bytes) < TAM_REGISTRO:
                break
                
            # Solo necesitamos desempaquetar DNI (primer campo) y apellido (segundo campo)
            # para armar el índice, minimizando el procesamiento.
            tupla = struct.unpack(FORMATO, registro_bytes)
            dni = tupla[0]
            # Decodificamos y limpiamos el padding de ceros (\x00)
            apellido = tupla[1].decode('utf-8').rstrip('\x00')
            
            # 1. Índice por DNI (Asumimos DNI único, guarda un solo entero)
            indice_por_dni[dni] = k
            
            # 2. Índice por Apellido (Puede haber repetidos, guarda una lista)
            if apellido not in indice_por_apellido:
                indice_por_apellido[apellido] = []
            indice_por_apellido[apellido].append(k)
            
            k += 1
            
    return indice_por_dni, indice_por_apellido


def buscar_por_dni(archivo, indice_por_dni, dni):
    """
    Busca el registro de un paciente utilizando su DNI mediante el índice en memoria.
    
    Comparación conceptual (Índice vs Búsqueda Secuencial):
    -------------------------------------------------------
    Utilizar el diccionario `indice_por_dni` permite resolver la búsqueda en memoria en 
    tiempo O(1) promedio gracias a la tabla hash subyacente. Una vez obtenida la posición 'k', 
    se realiza un ÚNICO acceso a disco mediante `seek(k * TAM_REGISTRO)`.
    
    Si NO tuviéramos este índice, estaríamos forzados a realizar una búsqueda secuencial 
    O(n) leyendo directamente sobre el archivo. Esto implicaría acceder a disco 'n' veces en el 
    peor caso (leyendo y desempaquetando cada registro hasta encontrar el DNI), lo cual es 
    varios órdenes de magnitud más lento debido a la latencia de entrada/salida (E/S) del disco.
    
    Precondición: El archivo debe estar abierto en modo lectura binaria ('rb'). # asi se evita tener que abrir el archivo por cada busqueda que se quiera hacer
    Postcondición: Devuelve los datos del paciente o None si no existe.
    
    Argumentos:
        archivo (file object): El objeto archivo abierto (retornado por open()).
        indice_por_dni (dict): Diccionario índice (clave: DNI, valor: posición k).
        dni (int): El DNI del paciente a buscar.
        
    Retorna:
        El registro del paciente (dict o tupla, según devuelva leer_paciente), 
        o None si el DNI no está en el índice.
    """
    # busqueda en O(1)
    k = indice_por_dni.get(dni)
    
    if k is None:
        return None  # el paciente no existe 
        
    # acceso directo O(1) a la posición en el archivo
    return leer_paciente(archivo, k)