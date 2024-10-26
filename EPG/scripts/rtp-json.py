import requests
import json
import os
from datetime import datetime, timedelta

# Função para obter a data em formato "dia-mes-ano"
def obter_data_formatada(dia_offset):
    data = datetime.now() + timedelta(days=dia_offset)
    return data.strftime("%d-%m-%Y")

# URL base do endpoint da RTP
url_base = "https://www.rtp.pt/EPG/json/rtp-home-page-tv-radio/list-all-grids/tv"

# Variável para armazenar todos os programas combinados
epg_completa = {}

# Loop para pegar dados dos próximos 7 dias
for i in range(7):
    # Data formatada para o dia atual + offset
    data_formatada = obter_data_formatada(i)
    url = f"{url_base}/{data_formatada}"
    
    # Realiza a requisição GET
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Dados JSON do dia atual
        dados_dia = response.json().get("result", {})
        
        # Combina os dados do dia atual no JSON principal
        for canal, programas in dados_dia.items():
            if canal not in epg_completa:
                epg_completa[canal] = {}
                
            # Ignora '_info' e combina apenas os períodos de programas
            for periodo, lista_programas in programas.items():
                if periodo != '_info':  # Ignora o campo '_info'
                    if periodo in epg_completa[canal]:
                        # Assegurar que epg_completa[canal][periodo] seja uma lista
                        if isinstance(epg_completa[canal][periodo], list):
                            epg_completa[canal][periodo].extend(lista_programas)
                        else:
                            print(f"Aviso: '{periodo}' não é uma lista para o canal '{canal}'. Tipo encontrado: {type(epg_completa[canal][periodo])}.")
                    else:
                        epg_completa[canal][periodo] = lista_programas
    else:
        print(f"Erro ao obter EPG para {data_formatada}: {response.status_code}")

# Caminho para salvar o arquivo JSON combinado
json_file_path = os.path.join(os.path.dirname(__file__), "..", "epg-rtp-pt.json")

# Salva o JSON em um arquivo
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(epg_completa, json_file, indent=4, ensure_ascii=False)

print(f"EPG combinada salva em: {json_file_path}")