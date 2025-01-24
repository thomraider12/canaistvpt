import requests
import json
import os
import time
import xml.etree.ElementTree as ET
import gzip
from datetime import datetime
from xml.dom import minidom

# Definir 90 minutos (1 hora e meia) em segundos
ninety_minutes_in_seconds = 90 * 60

# Obter a data atual e subtrair 1 hora e meia
start_date = int(time.time()) - ninety_minutes_in_seconds
end_date = start_date + 7 * 24 * 60 * 60  # 7 dias em segundos

# URL da EPG com as datas dinâmicas
url = f"https://opto.sic.pt/api/v1/content/epg?startDate={start_date}&endDate={end_date}&channels=549519c3-31fa-42de-a621-15e981082fd9,d47400e0-19d9-4f71-94f4-2b4cfdc1a2ca"
print(url)

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

    # Função para converter JSON para XMLTV
    def json_to_xmltv(json_data):
        # Criação do elemento raiz <tv>
        tv = ET.Element('tv')

        # Mapeamento de canais
        channels = {}

        # Percorrer o JSON e criar os elementos XML
        for entry in json_data:
            channel_id = entry['channel']['id']

            # Se o canal ainda não foi adicionado, criamos a entrada para ele
            if channel_id not in channels:
                channel = ET.SubElement(tv, 'channel', id=channel_id)

                # Adicionar o nome do canal
                display_name = ET.SubElement(channel, 'display-name')
                display_name.text = entry['channel']['name']

                # Procurar e adicionar o ícone (logo) do canal, se disponível
                logo_url = next((img['url'] for img in entry['channel']['image'] if img['name'] == 'logo'), None)
                if logo_url:
                    icon = ET.SubElement(channel, 'icon', src=logo_url)

                channels[channel_id] = channel

            # Converter datas para o formato XMLTV (YYYYMMDDHHMMSS +0000)
            start = datetime.strptime(entry['start_date'], '%Y-%m-%dT%H:%M:%SZ')
            end = datetime.strptime(entry['end_date'], '%Y-%m-%dT%H:%M:%SZ')

            start_str = start.strftime('%Y%m%d%H%M%S') + ' +0000'
            end_str = end.strftime('%Y%m%d%H%M%S') + ' +0000'

            # Criar o elemento <programme>
            programme = ET.SubElement(tv, 'programme', start=start_str, stop=end_str, channel=channel_id)

            # Adicionar o título do programa
            title = ET.SubElement(programme, 'title', lang='pt')
            title.text = entry['title']

            # Adicionar descrição curta (se disponível)
            if 'short_description' in entry:
                desc = ET.SubElement(programme, 'desc', lang='pt')
                desc.text = entry['short_description']

            # Adicionar número de temporada e episódio, se disponíveis
            if 'season_number' in entry and 'episode_number' in entry:
                episode_num = ET.SubElement(programme, 'episode-num', system='onscreen')
                episode_num.text = f"S{entry['season_number']:02d}E{entry['episode_number']:02d}"

        # Gerar o XML como string
        xml_data = ET.tostring(tv, encoding='utf-8', method='xml').decode('utf-8')

        # Usar minidom para pretty print
        xml_pretty = minidom.parseString(xml_data).toprettyxml(indent="  ")

        return xml_pretty

    # Função para salvar XML em GZIP
    def save_xml_as_gzip(xml_data, output_filename):
        # Salvar o XML comprimido no formato .xml.gz
        with gzip.open(output_filename, 'wt', encoding='utf-8') as f:
            f.write(xml_data)

    # Converter o JSON para XMLTV
    xml_output = json_to_xmltv(epg_data)

    # Caminho do arquivo XML de saída
    output_xml_file = os.path.join(os.path.dirname(__file__), "..", "epg-sic-pt.xml.gz")

    # Salvar o XML comprimido no formato .xml.gz
    save_xml_as_gzip(xml_output, output_xml_file)
    print(f"Arquivo XMLTV salvo como {output_xml_file}")

    # Apagar o arquivo JSON após a conversão
    if os.path.exists(json_file_path):
        os.remove(json_file_path)
        print(f"Arquivo JSON {json_file_path} apagado com sucesso.")

else:
    print(f"Erro ao obter EPG: {response.status_code} - {response.text}")