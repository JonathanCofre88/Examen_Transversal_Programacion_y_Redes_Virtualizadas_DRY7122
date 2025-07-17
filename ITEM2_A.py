import requests
import urllib.parse
import os

# URLs base y clave API de GraphHopper
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "30b1f46e-398b-4e4c-8230-8ff161152dc3"  # Reemplaza con tu clave válida

# Geocodificación de la ciudad
def geocoding(location, key):
    while location.strip() == "":
        location = input("Por favor, ingresa la ubicación nuevamente: ")

    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    response = requests.get(url)
    json_status = response.status_code
    json_data = response.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit["name"]
        value = hit.get("osm_value", "")
        country = hit.get("country", "")
        state = hit.get("state", "")

        # Traducción del tipo de lugar al español
        tipos_lugar = {
            "city": "ciudad",
            "town": "pueblo",
            "village": "villa",
            "neighbourhood": "barrio",
            "locality": "localidad",
            "island": "isla",
            "industrial": "zona industrial",
            "residential": "zona residencial",
            "quarter": "sector"
        }
        tipo_traducido = tipos_lugar.get(value, "zona desconocida")

        # Construcción de nombre completo
        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name

        print(f"Ubicación encontrada: {new_loc} (Tipo: {tipo_traducido})")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        print("❌ No se encontró la ubicación.")

    return json_status, lat, lng, new_loc

# Elegir medio de transporte
def elegir_medio_transporte():
    print("\nElige el medio de transporte:")
    print("1 - Vehiculo")
    print("2 - Bicicleta")
    print("3 - A pie")

    while True:
        opcion = input("Ingresa 1, 2 o 3 (o 's' para salir): ").lower()
        if opcion == "s":
            return None
        elif opcion == "1":
            return "car"
        elif opcion == "2":
            return "bike"
        elif opcion == "3":
            return "foot"
        else:
            print("Opción no válida, intenta de nuevo.")

# Mostrar narrativas del viaje
def mostrar_narrativas(data, nombre_origen, nombre_destino, medio_transporte):
    distancia_metros = data["paths"][0]["distance"]
    tiempo_ms = data["paths"][0]["time"]

    # Conversión
    km = distancia_metros / 1000
    millas = km / 1.60934
    total_seg = int(tiempo_ms / 1000)
    horas = total_seg // 3600
    minutos = (total_seg % 3600) // 60
    segundos = total_seg % 60

    # Narrativa resumida
    print("\nNarrativa del viaje:")
    print(f"Ciudad de origen: {nombre_origen}")
    print(f"Ciudad de destino: {nombre_destino}")
    print(f"Medio de transporte: {medio_transporte}")
    print(f"Distancia: {km:.2f} km")
    print(f"Duración estimada: {horas}h {minutos}min")

    # Narrativa detallada
    print("\n===========================================")
    print(f"Distancia total: {millas:.2f} millas / {km:.2f} kilómetros")
    print(f"Duración estimada del viaje: {horas:02d}:{minutos:02d}:{segundos:02d} (HH:MM:SS)")
    print("===========================================")

# Programa principal
def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # Limpia pantalla
        print("=== Calculadora de distancia entre ciudades ===")
        print("Escribe 's' para salir en cualquier momento.\n")

        # Ciudad de origen
        loc1 = input("Ciudad de Origen (Chile): ").strip()
        if loc1.lower() == "s":
            print("Saliendo...")
            break
        orig = geocoding(loc1, key)
        if orig[0] != 200:
            input("Presiona Enter para intentar de nuevo...")
            continue

        # Ciudad de destino
        loc2 = input("Ciudad de Destino (Argentina): ").strip()
        if loc2.lower() == "s":
            print("Saliendo...")
            break
        dest = geocoding(loc2, key)
        if dest[0] != 200:
            input("Presiona Enter para intentar de nuevo...")
            continue

        # Medio de transporte
        medio = elegir_medio_transporte()
        if medio is None:
            print("Saliendo...")
            break

        # Llamada a la API de rutas
        op = f"&point={orig[1]},{orig[2]}"
        dp = f"&point={dest[1]},{dest[2]}"
        params = {
            "key": key,
            "vehicle": medio,
            "locale": "es",
            "points_encoded": "false",
            "instructions": "false"
        }
        url_ruta = route_url + urllib.parse.urlencode(params) + op + dp

        response = requests.get(url_ruta)
        if response.status_code == 200:
            data = response.json()
            mostrar_narrativas(data, orig[3], dest[3], medio)
        else:
            print(f"❌ Error en la API de rutas: {response.status_code}")

        input("\nPresiona Enter para continuar...")

# Ejecutar
if __name__ == "__main__":
    main()
