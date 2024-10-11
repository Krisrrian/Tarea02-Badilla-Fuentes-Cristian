# Tarea 02 Redes de computacion ICI

#  ---Nombre participantes,Rut y Correo ---
#  Cristian Badilla Fuentes 21.507.403-k - cristian.badilla@alumnos.uv.cl
#  Amalia Toledo Astudillo  21.854.361-8 - amalia.toledo@alumnos.uv.cl
#  Benjamin Maldonado Nuñez 21.506.811-0 - benjamin.maldonadon@alumnos.uv.cl


import getopt
import sys
import requests
import os
import re

# Definir la URL de la API para hacer la consulta
URL_API = 'https://api.maclookup.app/v2/macs/'

# Función que realiza la consulta a la API
def consultar_mac(direccion_mac):
    try:
        # Hacer la solicitud a la API con la dirección MAC
        respuesta = requests.get(URL_API + direccion_mac)
        
        # Verificar si la solicitud fue exitosa
        if respuesta.status_code == 200:
            datos = respuesta.json()
            
            # Verificar si la respuesta contiene información del fabricante
            if datos and 'company' in datos and datos['company']:
                print(f"Dirección MAC: {direccion_mac}")
                print(f"Fabricante   : {datos['company']}")
            else:
                # Si no se encuentra fabricante
                print(f"Dirección MAC: {direccion_mac}")
                print("Fabricante   : No encontrado")
            
            # Imprimir el tiempo de respuesta
            print(f"Tiempo de respuesta: {respuesta.elapsed.total_seconds() * 1000:.2f}ms")
        
        else:
            # Imprimir el código de estado y el texto de respuesta para diagnósticos
            print(f"Error: La API devolvió un estado {respuesta.status_code}. Respuesta: {respuesta.text}")
    
    except Exception as e:
        print(f"Error al consultar la API: {e}")

# Función para obtener las direcciones MAC de la tabla ARP
def obtener_tabla_arp():
    try:
        # Ejecutar el comando "arp -a" y capturar la salida
        salida = os.popen('arp -a').read()
        
        # Expresión regular para extraer las direcciones MAC en el formato correcto
        direcciones_mac = re.findall(r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})', salida)
        
        # Unir los fragmentos de la dirección MAC y asegurarse de que el formato sea correcto
        return [':'.join(mac) for mac in direcciones_mac]
    
    except Exception as e:
        print(f"Error al obtener la tabla ARP: {e}")
        return []

# Función principal para manejar los argumentos y ejecutar la lógica
def main():
    try:
        opciones, argumentos = getopt.getopt(sys.argv[1:], "hm:a", ["help", "mac=", "arp"])
    except getopt.GetoptError as error:
        print(error)
        uso()
        sys.exit(2)

    direccion_mac = None
    arp = False

    for opcion, argumento in opciones:
        if opcion in ("-h", "--help"):
            uso()
            sys.exit()
        elif opcion in ("-m", "--mac"):
            direccion_mac = argumento
        elif opcion in ("-a", "--arp"):
            arp = True
        else:
            assert False, "Opción no válida"

    if direccion_mac:
        direccion_mac = direccion_mac.replace('-', ':').lower()  # Asegurarse del formato correcto
        print(f"Consultando fabricante para la MAC: {direccion_mac}")
        # Llamar a la función consultar_mac para consultar el fabricante
        consultar_mac(direccion_mac)
    elif arp:
        print("Obteniendo tabla ARP...")
        macs = obtener_tabla_arp()
        if macs:
            for mac in macs:
                mac_str = mac.lower()  # Convertir todas las direcciones a minúsculas
                print(f"Consultando fabricante para la MAC: {mac_str}")
                consultar_mac(mac_str)
        else:
            print("No se encontraron entradas en la tabla ARP.")
    else:
        uso()

def uso():
    print("Uso: OUILookup.py --mac <mac> | --arp | [--help]")
    print("--mac: MAC a consultar. Ej: aa:bb:cc:00:00:00.")
    print("--arp: Muestra los fabricantes de los hosts disponibles en la tabla ARP.")
    print("--help: Muestra este mensaje y termina.")

if __name__ == "__main__":
    main()
