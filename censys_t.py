import requests
from requests.auth import HTTPBasicAuth
import json

# Configuración de la API
API_ID = "your-api-id"
API_SECRET = "your-api-secret"
BASE_URL = "https://search.censys.io/api/v2"
VIEW_IP_URL = f"{BASE_URL}/hosts/"
NAMES_URL = f"{BASE_URL}/hosts/{{ip}}/names"  # Nuevo endpoint


def obtener_dominios(ip):
    """Obtiene información básica de un host"""
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth(API_ID, API_SECRET)

    try:
        response = requests.get(
            f"{VIEW_IP_URL}{ip}", auth=auth, headers=headers)
        response.raise_for_status()
        return response.json().get('result', {})
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar host: {str(e)}")
        return None


def obtener_nombres(ip, per_page=100, cursor=None):
    """Obtiene nombres asociados a una IP con paginación"""
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth(API_ID, API_SECRET)
    params = {"per_page": per_page}

    if cursor:
        params["cursor"] = cursor

    try:
        response = requests.get(
            NAMES_URL.format(ip=ip),
            auth=auth,
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener nombres: {str(e)}")
        return None


def guardar_resultados(ip, datos, tipo='info'):
    """Guarda resultados en archivo JSON"""
    nombre_archivo = f"{ip}_censys_{tipo}.json"
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        print(f"Resultados guardados en {nombre_archivo}")
    except IOError as e:
        print(f"Error al guardar: {str(e)}")


def consultar_todos_nombres(ip):
    """Consulta todos los nombres paginados"""
    todos_nombres = []
    cursor = None

    while True:
        resultado = obtener_nombres(ip, cursor=cursor)
        if not resultado:
            break

        todos_nombres.extend(resultado.get('data', []))
        cursor = resultado.get('links', {}).get('next')

        if not cursor:
            break

    return todos_nombres


if __name__ == "__main__":
    print("\n=== Consulta Censys API v2 ===")

    while True:
        ip = input(
            "\nIngrese la IP a consultar (o 'salir' para terminar): ").strip()

        if ip.lower() == 'salir':
            break

        if not ip.replace('.', '').isdigit() or len(ip.split('.')) != 4:
            print("Error: Ingrese una IPv4 válida")
            continue

        # Consulta información básica
        print("\n[1/2] Obteniendo información del host...")
        info_host = obtener_dominios(ip)
        if info_host:
            guardar_resultados(ip, info_host, 'info')
            print(
                f"ASN: {info_host.get('autonomous_system', {}).get('asn', 'N/A')}")
            print(
                f"Organización: {info_host.get('autonomous_system', {}).get('name', 'N/A')}")

        # Consulta nombres asociados
        print("[2/2] Buscando nombres asociados (puede tomar tiempo)...")
        nombres = consultar_todos_nombres(ip)
        if nombres:
            guardar_resultados(ip, nombres, 'nombres')
            print(f"Total nombres encontrados: {len(nombres)}")
            print("Ejemplos:", ", ".join(
                nombres[:3]) + ("..." if len(nombres) > 3 else ""))

    print("Saliendo del programa...")
