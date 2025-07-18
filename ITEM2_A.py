import requests
import urllib.parse
import os

# URLs base y clave API
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "30b1f46e-398b-4e4c-8230-8ff161152dc3"

# Geocodificación
def geocoding(location, key):
    while location.strip() == "":
        location = input("Por favor, ingresa la ubicación nuevamente: ")

    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    response = requests.get(url)
    json_data = response.json()

    if response.status_code == 200 and json_data["hits"]:
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit["name"]
        country = hit.get("country", "")
        state = hit.get("state", "")
        full_name = f"{name}, {state}, {country}".strip(", ")
        return 200, lat, lng, full_name
    else:
        print("No se pudo encontrar la ubicación.")
        return response.status_code, None, None, location

# Elegir medio de transporte
def elegir_medio_transporte():
    print("\nElige el medio de transporte:")
    print("1 - Vehículo")
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

# Mostrar resumen del viaje
def mostrar_resumen(path, origen, destino):
    km = path["distance"] / 1000
    millas = km / 1.60934
    tiempo_seg = int(path["time"] / 1000)
    horas = tiempo_seg // 3600
    minutos = (tiempo_seg % 3600) // 60
    segundos = tiempo_seg % 60

    print("\n==============================================")
    print(f"Ruta desde {origen} hasta {destino}")
    print("==============================================")
    print(f"Distancia: {km:.2f} km / {millas:.2f} millas")
    print(f"Duración estimada: {horas}h {minutos}m {segundos}s")

# Mostrar narrativa paso a paso
def mostrar_narrativa(instrucciones):
    print("\nNarrativa del viaje paso a paso:")
    print("==============================================")
    for idx, paso in enumerate(instrucciones):
        texto = paso["text"]
        metros = int(paso["distance"])
        print(f"{idx+1}. {texto} ({metros} m)")

# Programa principal
def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Calculadora de rutas entre ciudades ===")
        print("Escribe 's' para salir en cualquier momento.\n")

        # Ciudad de origen
        origen_input = input("Ciudad de Origen (Chile): ").strip()
        if origen_input.lower() == "s":
            break
        orig = geocoding(origen_input, key)
        if orig[0] != 200:
            input("Presiona Enter para intentar de nuevo...")
            continue
        origen_final = orig[3]

        # Ciudad de destino
        destino_input = input("Ciudad de Destino (Argentina): ").strip()
        if destino_input.lower() == "s":
            break
        dest = geocoding(destino_input, key)
        if dest[0] != 200:
            input("Presiona Enter para intentar de nuevo...")
            continue
        destino_final = dest[3]

        # Medio de transporte
        medio = elegir_medio_transporte()
        if medio is None:
            break

        # Llamada a la API de rutas
        params = {
            "key": key,
            "point": [f"{orig[1]},{orig[2]}", f"{dest[1]},{dest[2]}"],
            "vehicle": medio,
            "locale": "es",
            "instructions": "true"
        }

        url = route_url + urllib.parse.urlencode(params, doseq=True)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            path = data["paths"][0]
            instrucciones = path["instructions"]

            mostrar_resumen(path, origen_final, destino_final)
            input("\nPresiona Enter para ver la narrativa paso a paso...")
            mostrar_narrativa(instrucciones)
        else:
            print("No se pudo obtener la ruta. Intenta nuevamente.")

        input("\nPresiona Enter para calcular otra ruta...")

# Ejecutar
if __name__ == "__main__":
    main()