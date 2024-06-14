import requests
import os

# Funções ========================================================================================

def load_env_file(file_path):
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            key, value = line.split('=', 1)

            os.environ[key] = value
            
            
def get_dist_dur(api_key, start, end):

    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {

        "origins": start,

        "destinations": end,

        "key": api_key

    }

    response = requests.get(base_url, params=params)

    
    if response.status_code == 200:

        data = response.json()

        if data["status"] == "OK":

            distance = data["rows"][0]["elements"][0]["distance"]["text"]

            duration = data["rows"][0]["elements"][0]["duration"]["text"]

            return distance, duration

        else:

            print("Request failed.")

            return None, None

    else:

        print("Failed to make the request.")

        return None, None
    
    

def get_lati_longi(api_key, address):

    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = {

        "address": address,

        "key": api_key

    }

    response = requests.get(url, params=params)


    if response.status_code == 200:

        data = response.json()

        if data["status"] == "OK":

            location = data["results"][0]["geometry"]["location"]

            lat = location["lat"]

            lng = location["lng"]

            return lat, lng

        else:

            print(f"Error: {data['error_message']}")

            return 0, 0

    else:

        print("Failed to make the request.")

        return 0, 0

def set_array(adress, key):
    n = len(adress)
    array_distance = [[0]*n for _ in range(n)]
    array_duration = [[0]*n for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            distance, duration = get_dist_dur(key, adress[i], adress[j])
            if distance is not None and duration is not None:
                array_distance[i][j] = array_distance[j][i] = distance
                array_duration[i][j] = array_duration[j][i] = duration

    return array_distance, array_duration

# Pegando a chave da API na env ============================================================================

load_env_file('.env')

api_key = os.getenv('API_KEY')

# Testes ===================================================================================================

# Teste 1 ----
address = 'Rua Benjamin Constant, 184, Rio Grande'

lati, longi = get_lati_longi(api_key, address)

print(f"Latitude: {lati}")

print(f"Longitude: {longi}")


# Teste 2 ----

start = "Palace Lucerna, Nové Město"

end = "Project FOX, Praha 3-Žižkov"

distance, duration = get_dist_dur(api_key, start, end)

if distance and duration:

    print(f"Distância: {distance}")

    print(f"Duração: {duration}")
    

# Teste 3 ----
    
enderecos = [
    "1600 Amphitheatre Parkway, Mountain View, CA",
    "1 Infinite Loop, Cupertino, CA",
    "350 5th Ave, New York, NY"
]

print('\n\n-----------------\n\n')

matriz_distancias, matriz_tempos = set_array(enderecos, api_key)
print("Matriz de Distâncias:")
for linha in matriz_distancias:
    print(linha)

print("\nMatriz de Tempos:")
for linha in matriz_tempos:
    print(linha)
    
print('\n\n-----------------\n\n')
