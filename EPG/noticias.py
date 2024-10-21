import gzip
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import os

# Função para converter o formato de tempo do XML para datetime
def parse_xml_time(xml_time):
    return datetime.strptime(xml_time, "%Y%m%d%H%M%S %z")

# Função para verificar se um programa está no ar
def is_currently_airing(start_time, end_time, current_time):
    return start_time <= current_time < end_time

# Atualize o caminho para o arquivo EPG
epg_path = 'epg-pt.xml.gz'
html_path = '../noticias.html'


# Descompactar e analisar o arquivo EPG usando gzip
with gzip.open(epg_path, 'rt', encoding='utf-8') as file:
    epg_tree = ET.parse(file)

epg_root = epg_tree.getroot()

# Obter o horário atual
current_time = datetime.now(pytz.timezone('Europe/Lisbon'))

# Extrair informações dos canais e programas atuais
channels = {}
for channel in epg_root.findall('channel'):
    channel_id = channel.get('id')
    display_name = channel.find('display-name').text
    channels[channel_id] = display_name

programs = {}
for programme in epg_root.findall('programme'):
    channel_id = programme.get('channel')
    title = programme.find('title').text
    start = parse_xml_time(programme.get('start'))
    end = parse_xml_time(programme.get('stop'))
    if is_currently_airing(start, end, current_time):
        programs[channel_id] = {
            'title': title,
            'start': start,
            'end': end
        }

# Combinar informações dos canais e programas
current_programs = {channels[key]: programs[key]['title'] for key in programs if key in channels}

# Carregar e modificar o HTML
with open(html_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Mapear classes dos canais para IDs do EPG
channel_classes_to_ids = {
    'rtp1': 'RTP 1',
    'rtp2': 'RTP 2',
    'sic': 'SIC',
    'tvi': 'TVI',
    'sicnot': 'SIC Noticias',
    'rtp3': 'RTP 3',
    'cnnportugal': 'CNN Portugal',
    'vmaistvi': 'V+ TVI',
    'portocanal': 'Porto Canal',
    'euronewspt': 'Euronews Portuguese',
    # Adicione mapeamentos adicionais conforme necessário
}

# Inserir nomes dos programas no HTML sem escapar tags
for class_name, channel_name in channel_classes_to_ids.items():
    if channel_name in current_programs:
        program_tag = soup.find('a', class_=class_name)
        if program_tag:
            # Preserva o conteúdo HTML sem escapar tags
            new_content = f"{channel_name}<sup>HD</sup> - {current_programs[channel_name]}"
            program_tag.string = ""
            program_tag.append(BeautifulSoup(new_content, 'html.parser'))

# Salvar o HTML modificado
with open(html_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("HTML modificado com sucesso e salvo como 'noticias.html'")
