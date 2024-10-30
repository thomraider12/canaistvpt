import requests
import xml.etree.ElementTree as ET
import gzip
import json
import time
from xml.dom import minidom

# Função para converter JSON para XMLTV e contar programas adicionados
def json_to_xmltv(json_data, root):
    program_count = 0
    for event in json_data.get("objects", []):
        # Obtém o nome do programa para exibição
        program_name = event.get("name", "Sem título")
        print(f"Processando programa: \"{program_name}\"")  # Mensagem de processamento

        # Criando o elemento programa com os novos nomes de campo
        programme = ET.SubElement(root, "programme", {
            "start": event["segment_start_time"],
            "stop": event["segment_end_time"],
            "channel": "ubisoft_br_tv"
        })

        # Adiciona título
        title = ET.SubElement(programme, "title", {"lang": "pt"})
        title.text = program_name

        # Adiciona descrição
        desc = ET.SubElement(programme, "desc", {"lang": "pt"})
        desc.text = event.get("long_description", event.get("short_description", "Sem descrição"))
        
        program_count += 1  # Incrementa a contagem de programas adicionados

    print(f"{program_count} programas adicionados.")
    return root

# Função para obter dados de API
def fetch_data_for_timestamp(timestamp):
    url = f"https://api-ott.ubisoftbrasil.tv/getvideosegments?&banners=0&connection=wifi&device_type=desktop&for_user=0&image_format=widescreen&image_width=366&language=pt&linear_channel_id=114&parent_id=114&parent_type=linear_channel&partner=internal&platform=web&timestamp={timestamp}&timezone=-0000&use_device_width_widescreen=1&version=14.0"
    print(url)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Função para adicionar o canal ao XMLTV
def add_channel(root, channel_id, display_name, icon_url):
    # Verifica se o canal já existe
    existing_channels = root.findall("channel")
    for channel in existing_channels:
        if channel.get("id") == channel_id:
            return  # Canal já existe, não adiciona novamente

    # Adiciona o canal se não existir
    channel = ET.SubElement(root, "channel", {"id": channel_id})
    display_name_element = ET.SubElement(channel, "display-name", {"lang": "pt"})
    display_name_element.text = display_name
    icon_element = ET.SubElement(channel, "icon", {"src": icon_url})

# Função principal para processar múltiplos dias
def process_multiple_days(start_timestamp, days):
    # Lê o arquivo XML existente e obtém o elemento raiz
    with gzip.open("epg-extra.xml.gz", "rb") as f:
        tree = ET.parse(f)
        root = tree.getroot()

    # Adiciona o canal ao root se não estiver presente
    add_channel(root, "ubisoft_br_tv", "Ubisoft Brasil TV", "https://images.pluto.tv/channels/64c815e8a1c6130008fef928/colorLogoPNG.png")

    # Para cada dia, faça a extração dos dados JSON e converta para XML
    timestamp = start_timestamp
    for day in range(1, days + 1):
        print(f"Processando dia {day}...")

        # Obter dados da API para o timestamp atual
        json_data = fetch_data_for_timestamp(timestamp)
        
        # Convertendo os dados JSON para XMLTV e adicionando ao root existente
        root = json_to_xmltv(json_data, root)
        
        # Incrementa o timestamp em 24 horas para o próximo dia
        timestamp += 86400  # Segundos em um dia

    # Transforma o XML em uma string formatada
    xml_content = ET.tostring(root, encoding="unicode")
    pretty_xml = minidom.parseString(xml_content).toprettyxml(indent="  ")

    # Escreve o conteúdo formatado de volta ao arquivo .gz
    with gzip.open("epg-extra.xml.gz", "wb") as f:
        f.write(pretty_xml.encode("utf-8"))

    print("\nProcessamento concluído e arquivo atualizado com sucesso.")

# Executar a função principal para processar múltiplos dias
start_timestamp = int(time.time()) - 5400  # Define como 1h30min atrás
days = 7  # Quantidade de dias que você quer extrair
process_multiple_days(start_timestamp, days)