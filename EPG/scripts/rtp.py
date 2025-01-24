import requests
import json
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timedelta
import gzip

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

# Função para converter JSONTV para XMLTV
def convert_jsontv_to_xmltv(json_path, xml_output_path, duracao_maxima_horas=3):
    # Carregar JSONTV e verificar a estrutura
    with open(json_path, "r", encoding="utf-8") as file:
        jsontv_data = json.load(file)
    
    # Elemento raiz do XMLTV
    tv_element = ET.Element("tv")

    # Iterar pelos canais no JSONTV
    for channel_key, channel_info in jsontv_data.items():
        # Obter o nome do canal para exibir
        channel_name = channel_info.get("_info", {}).get("name", channel_key)
        print(f"Processando canal: {channel_name}")

        # Criar o elemento <channel> e adicionar detalhes
        channel_element = ET.SubElement(tv_element, "channel", id=channel_key)
        display_name = ET.SubElement(channel_element, "display-name")
        display_name.text = channel_name
        
        icon_url = channel_info.get("_info", {}).get("logoUrl", "")
        if icon_url:
            ET.SubElement(channel_element, "icon", src=icon_url)

        # Seções de programação
        sections = ["primetime", "morning", "afternoon", "evening"]

        # Iterar sobre cada seção para adicionar programas
        for section in sections:
            programmes = channel_info.get(section, [])
            for i, programme in enumerate(programmes):
                print(f"  Processando programa: {programme['name']}")

                start_time = datetime.strptime(programme["date"], "%Y-%m-%d %H:%M:%S")
                start_formatted = start_time.strftime("%Y%m%d%H%M%S")

                # Calcular o horário de fim
                if i + 1 < len(programmes):
                    # Usar início do próximo programa como base
                    next_start_time = datetime.strptime(programmes[i + 1]["date"], "%Y-%m-%d %H:%M:%S")
                    stop_time = min(start_time + timedelta(hours=duracao_maxima_horas), next_start_time)
                else:
                    # Último programa: limitar a duração máxima
                    stop_time = start_time + timedelta(hours=duracao_maxima_horas)

                stop_formatted = stop_time.strftime("%Y%m%d%H%M%S")

                # Criar o elemento <programme>
                programme_element = ET.SubElement(tv_element, "programme", 
                                                  start=start_formatted,
                                                  stop=stop_formatted,
                                                  channel=channel_key)

                # Adicionar título e descrição
                title = ET.SubElement(programme_element, "title")
                title.text = programme["name"]

                desc = ET.SubElement(programme_element, "desc")
                desc.text = programme["description"]

                # Adicionar URL e imagens, se disponíveis
                url = ET.SubElement(programme_element, "url")
                url.text = programme.get("url", "")

                if "image" in programme:
                    for img in programme["image"]:
                        ET.SubElement(programme_element, "icon", src=img["src"])

    # Salvar o XMLTV em arquivo
    xml_content = ET.tostring(tv_element, encoding='utf-8', xml_declaration=True).decode('utf-8')

    # Melhorar a formatação para visualização (indentação e novas linhas)
    pretty_xml = minidom.parseString(xml_content).toprettyxml(indent="  ")

    # Salvar o arquivo comprimido em GZIP
    with gzip.open(xml_output_path, 'wt', encoding='utf-8') as gz_file:
        gz_file.write(pretty_xml)

    if os.path.exists(json_path):
        os.remove(json_path)
        print(f"Ficheiro JSON {json_path} apagado com sucesso.")
    else:
        print(f"O ficheiro JSON {json_path} não foi encontrado para ser apagado.")

# Exemplo de uso
try:
    convert_jsontv_to_xmltv(json_file_path, "epg-rtp-pt.xml.gz")  # Altere o nome do arquivo para .gz
    print("Conversão concluída com sucesso.")
except KeyError as e:
    print(f"Erro: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
