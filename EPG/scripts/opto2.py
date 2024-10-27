import xml.etree.ElementTree as ET
import json
import gzip
import os
from datetime import datetime

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
        
        # Adicionar classificação
        rating = ET.SubElement(programme, 'rating')
        value = ET.SubElement(rating, 'value')
        value.text = str(entry['classification'])

    # Gerar o XML como string
    xml_data = ET.tostring(tv, encoding='utf-8', method='xml').decode('utf-8')
    return xml_data

def save_xml_as_gzip(xml_data, output_filename):
    # Salvar o XML comprimido no formato .xml.gz
    with gzip.open(output_filename, 'wt', encoding='utf-8') as f:
        f.write(xml_data)

# Exemplo de uso
def main():
    # Caminho do JSON de entrada e XML de saída
    input_json_file = os.path.join(os.path.dirname(__file__), "..", "epg-sic-pt.json")
    output_xml_file = os.path.join(os.path.dirname(__file__), "..", "epg-sic-pt.xml.gz")  # Alterado para .xml.gz

    # Carregar o JSON de um ficheiro
    with open(input_json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Converter o JSON para XMLTV
    xml_output = json_to_xmltv(json_data)
    
    # Salvar o XML comprimido no formato .xml.gz
    save_xml_as_gzip(xml_output, output_xml_file)
    print(f"Arquivo XMLTV salvo como {output_xml_file}")

if __name__ == "__main__":
    main()
