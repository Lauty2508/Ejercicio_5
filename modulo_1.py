"""
MÓDULO 1: Persistencia Binaria de Pacientes

Plan de Casos de Prueba implementados y validados en este módulo:

* Caso de Prueba 1 - Datos Estándar: 
  Verifica que los datos válidos se empaqueten, guarden, lean y desempaqueten 
  manteniendo su integridad absoluta.
   
* Caso de Prueba 2 - Validación de Tamaño del Archivo: 
  Comprueba que el tamaño del archivo en disco (os.path.getsize) coincida 
  exactamente con el cálculo (cantidad_de_pacientes * TAM_REGISTRO), 
  garantizando la longitud fija requerida por la consigna.
   
* Caso de Prueba 3 - Truncado de Cadenas Excesivamente Largas: 
  Asegura que si se ingresan strings que superan los límites de bytes 
  (30 para apellido, 24 para nombre, 16 para teléfono), el sistema los 
  trunca correctamente sin romper el tamaño del registro binario.
   
* Caso de Prueba 4 - Protección contra errores UTF-8 rotos: 
  Verifica que el uso de errors='ignore' prevenga un UnicodeDecodeError 
  si un carácter de múltiples bytes (como una 'ñ' o vocal con tilde) queda 
  partido a la mitad por el truncado estricto.
   
* Caso de Prueba 5 - Índices Fuera de Rango: 
  Garantiza que la función leer_paciente maneje offsets inválidos de 
  manera segura, devolviendo None al no encontrar datos suficientes.
"""

import struct
import os


FORMATO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO)

# (a) empaquetado y desempaquetado de registros

def empaquetar_paciente(dni, apellido, nombre, telefono, prioridad):
    """
    Empaqueta los datos de un paciente en un registro de bytes de longitud fija.
    Trunca las cadenas largas para que no excedan el tamaño asignado y las codifica en UTF-8.
    
    Precondición: prioridad debe ser un entero entre 1 y 3.
    Postcondición: Devuelve un objeto bytes de tamaño TAM_REGISTRO.
    """
    # Codificamos a UTF-8 y luego truncamos los bytes al tamaño máximo permitido
    #RESOLUCIÓN
    apellido_b = apellido.encode('utf-8')[:30]
    nombre_b = nombre.encode('utf-8')[:24]
    telefono_b = telefono.encode('utf-8')[:16]
    
    #EPÍLOGO
    return struct.pack(FORMATO, dni, apellido_b, nombre_b, telefono_b, prioridad)

def desempaquetar_paciente(registro_bytes):
    """
    Desempaqueta un registro de bytes de longitud fija en sus componentes originales.
    Remueve el relleno de ceros de las cadenas y las decodifica desde UTF-8.
    
    Precondición: registro_bytes debe tener exactamente la longitud TAM_REGISTRO.
    Postcondición: Devuelve una tupla (dni, apellido, nombre, telefono, prioridad).
    """
    #PRÓLOGO
    dni, apellido_b, nombre_b, telefono_b, prioridad = struct.unpack(FORMATO, registro_bytes)
    
    # rstrip(b'\x00') elimina los bytes nulos de relleno agregados por struct.pack
    # errors='ignore' protege contra cortes de caracteres especiales que ocupan mas de un byte, puede pasar por el truncamiento, esto en vez de lanzar un error no nos escribe la ultima letra, ya que ocupa dos bytes pero fue truncada.

    #RESOLUCIÓN
    apellido = apellido_b.rstrip(b'\x00').decode('utf-8', errors='ignore')
    nombre = nombre_b.rstrip(b'\x00').decode('utf-8', errors='ignore')
    telefono = telefono_b.rstrip(b'\x00').decode('utf-8', errors='ignore')
    
    #EPÍLOGO
    return dni, apellido, nombre, telefono, prioridad

# (b) Operaciones de Archivo

def crear_archivo_pacientes(ruta, lista_pacientes):
    """
    Crea un archivo binario e inserta una lista de pacientes de forma secuencial.
    
    Precondición: lista_pacientes es una lista de tuplas con el formato 
                  (dni, apellido, nombre, telefono, prioridad).
    Postcondición: El archivo queda creado y guardado en disco.
    """
    with open(ruta, 'wb') as archivo:
        for paciente in lista_pacientes:
            registro_bytes = empaquetar_paciente(*paciente) #le pasamos ada uno de los elementos de la tupla paciente.
            archivo.write(registro_bytes)

def leer_paciente(archivo, k):
    """
    Lee un paciente específico del archivo binario usando acceso directo (O(1)).
    
    Precondición: El archivo debe estar abierto en modo lectura binaria ('rb').
                  k es la posición (índice 0-basado) del registro a leer.
    Postcondición: Devuelve la tupla con los datos del paciente, o None si k está fuera de rango.
    """
    #PRÓLOGO
    archivo.seek(k * TAM_REGISTRO)
    registro_bytes = archivo.read(TAM_REGISTRO)
    
    #RESOLUCIÓN
    # Verificamos si llegamos al final del archivo o leímos bytes incompletos
    if not registro_bytes or len(registro_bytes) < TAM_REGISTRO:
        return None
        
    #EPÍLOGO
    return desempaquetar_paciente(registro_bytes)



# EJECUCIÓN DE CASOS DE PRUEBA MODULO 1
if __name__ == '__main__':
    print("==================================================")
    RUTA_TEST = "pacientes_test.bin"
    
    # --- Caso de Prueba 1: Datos Estándar ---
    print("Ejecutando Caso de Prueba 1: Datos Estándar...")
    pacientes_validos = [
        (20123456, "Gomez", "Juan", "341-4555666", 1),
        (30987654, "Rodriguez", "Maria Ana", "11-23456789", 3),
        (40111222, "Paz", "Luis", "261-999888", 2)
    ] #lista de tuplas
    
    crear_archivo_pacientes(RUTA_TEST, pacientes_validos)
    with open(RUTA_TEST, 'rb') as f:
        for idx, original in enumerate(pacientes_validos): 
            assert leer_paciente(f, idx) == original, f"Error en el registro con índice {idx}" #nos fijamos que el idx sea el correcto para cada registro
    print("-> OK") #si ldx es correcto se imprime ok.si no se detiene el programa e imprime que hubo un error en el registro cccorrespondiente.

    # --- Caso de Prueba 2: Validación de Tamaño del Archivo ---
    print("Ejecutando Caso de Prueba 2: Verificación de Tamaño Fijo...")
    assert os.path.getsize(RUTA_TEST) == len(pacientes_validos) * TAM_REGISTRO, "Error en CP2: Tamaño incorrecto"
    print("-> OK")

    # --- Caso de Prueba 3: Truncado de Cadenas Excesivamente Largas ---
    print("Ejecutando Caso de Prueba 3: Truncado de Cadenas Largas...")
    paciente_extremo = [(99999999, "Anasagasti-Echeverria-De-La-Riestra", "Constantino-Alexandro-Francisco", "0054911223344556677", 2)]
    crear_archivo_pacientes(RUTA_TEST, paciente_extremo)
    with open(RUTA_TEST, 'rb') as f:
        recuperado = leer_paciente(f, 0)
        assert len(recuperado[1]) == 30 and len(recuperado[2]) == 24 and len(recuperado[3]) == 16, "Error en CP3: No se truncó correctamente"
    print("-> OK")

    # --- Caso de Prueba 4: Protección contra errores de bytes UTF-8 rotos ---
    print("Ejecutando Caso de Prueba 4: Caracteres UTF-8 Especiales en el Límite...")
    paciente_critico = [(77777777, "Test", "Alba-Munoz-Alba-Munoz-Albañ", "123", 1)]
    crear_archivo_pacientes(RUTA_TEST, paciente_critico)
    try:
        with open(RUTA_TEST, 'rb') as f:
            leer_paciente(f, 0)
        print("-> OK")
    except UnicodeDecodeError:
        assert False, "CRÍTICO: El programa falló al decodificar un byte truncado. Revisar errors='ignore'."

    # --- Caso de Prueba 5: Control de Índices Inexistentes (Fuera de Rango) ---
    print("Ejecutando Caso de Prueba 5: Índices Fuera de Rango...")
    with open(RUTA_TEST, 'rb') as f:
        assert leer_paciente(f, 5) is None, "Error en CP5: Debería devolver None"
    print("-> OK")

    print("==================================================")
    print(" ¡TODOS LOS CASOS DE PRUEBA DEL MÓDULO 1 PASARON CON ÉXITO! ")
    print("==================================================")
    
    # eliminamos el archivo de pruebas.
    if os.path.exists(RUTA_TEST):
        os.remove(RUTA_TEST)