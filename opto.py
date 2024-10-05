import requests
import json
import os
import time
import lzma  # Importando a biblioteca para compressão

# Obter a data atual e a data de 2 dias depois em formato Unix
start_date = int(time.time())
end_date = start_date + 2 * 24 * 60 * 60  # 2 dias em segundos

# URL da EPG com as datas dinâmicas
url = f"https://opto.sic.pt/api/v1/content/epg?startDate={start_date}&endDate={end_date}&channels=549519c3-31fa-42de-a621-15e981082fd9,d47400e0-19d9-4f71-94f4-2b4cfdc1a2ca"

# Realiza a requisição GET
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Obtém o conteúdo em JSON
    epg_data = response.json()
    
    # Caminho do arquivo JSON
    json_file_path = os.path.join("EPG", "epg-sic-pt.json")
    
    # Salva o JSON em um arquivo
    with open(json_file_path, 'w') as json_file:
        json.dump(epg_data, json_file, indent=4)
    
    print(f"EPG salva em: {json_file_path}")

    # Caminho do arquivo .xz
    xz_file_path = os.path.join("EPG", "epg-sic-pt.json.xz")

    # Compacta o arquivo JSON em .xz
    with open(json_file_path, 'rb') as json_file:
        with lzma.open(xz_file_path, 'wb') as xz_file:
            xz_file.write(json_file.read())

    print(f"EPG comprimida em: {xz_file_path}")
else:
    print(f"Erro ao obter EPG: {response.status_code} - {response.text}")
