# função de geolocalização para aplicação

import requests

def endereco_para_coodernadas(estado, cidade, numero, rua):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "street": f"{rua} {numero}",
        "city": f"{cidade}",
        "state": f"{estado}",
        "country": "BR",
        "format": "json",
        "limit": 1
    }
    response = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    
    if response.status_code == 200:
        data = response.json()
        if data:
            
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            print("Endereço não encontrado.")
            return None, None
    else:
        print("Erro na requisição:", response.status_code)
        return None, None

