import requests
import json
import os
import time

# Definir 90 minutos (1 hora e meia) em segundos
ninety_minutes_in_seconds = 90 * 60

# Obter a data atual e subtrair 1 hora e meia
start_date = int(time.time()) - ninety_minutes_in_seconds
end_date = start_date + 7 * 24 * 60 * 60  # 2 dias em segundos

# URL da EPG com as datas dinâmicas
url = f"https://opto.sic.pt/api/v1/content/epg?startDate={start_date}&endDate={end_date}"

# Realiza a requisição GET
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Obtém o conteúdo em JSON
    epg_data = response.json()

    # Caminho do arquivo JSON (salvando diretamente na pasta EPG)
    json_file_path = os.path.join(os.path.dirname(__file__), "..", "epg-sic-pt.json")
    
    # Salva o JSON em um arquivo
    with open(json_file_path, 'w') as json_file:
        json.dump(epg_data, json_file, indent=4)
    
    print(f"EPG salva em: {json_file_path}")
else:
    print(f"Erro ao obter EPG: {response.status_code} - {response.text}")
