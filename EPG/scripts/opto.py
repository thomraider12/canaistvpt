import requests
import json
import os
import time
import lzma
import xmltodict

# Obter a data atual e a data de 2 dias depois em formato Unix
start_date = int(time.time())
end_date = start_date + 2 * 24 * 60 * 60  # 2 dias em segundos

# URL da EPG com as datas dinâmicas
url = f"https://opto.sic.pt/api/v1/content/epg?startDate={start_date}&endDate={end_date}&channels=549519c3-31fa-42de-a621-15e981082fd9"

# Realiza a requisição GET
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Obtém o conteúdo em JSON
    epg_data = response.json()
    
    # Caminho absoluto para a pasta EPG
    epg_directory = os.path.join(os.path.dirname(__file__), '..', 'EPG')

    # Cria a pasta EPG caso não exista
    os.makedirs(epg_directory, exist_ok=True)
    
    # Caminho do arquivo XML
    xml_file_path = os.path.join(epg_directory, "epg-sic-pt.xml")
    
    # Converte o JSON para XML
    xml_data = xmltodict.unparse({"epg": epg_data}, pretty=True)  # Converte para XML
    
    # Salva o XML em um arquivo
    with open(xml_file_path, 'w') as xml_file:
        xml_file.write(xml_data)

    print(f"EPG salva em: {xml_file_path}")

    # Caminho do arquivo .xz
    xz_file_path = os.path.join(epg_directory, "epg-sic-pt.xml.xz")

    # Compacta o arquivo XML em .xz
    with open(xml_file_path, 'rb') as xml_file:
        with lzma.open(xz_file_path, 'wb') as xz_file:
            xz_file.write(xml_file.read())

    print(f"EPG comprimida em: {xz_file_path}")

else:
    print(f"Erro ao obter EPG: {response.status_code} - {response.text}")
