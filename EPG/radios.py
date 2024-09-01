import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Lista de rádios
radios = [
    {"id": "DJTomasA", "nome": "DJ Tomás Afonso", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tomasafonso.ico"},
    {"id": "RadioComercial.pt", "nome": "Rádio Comercial", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiocomercial.png"},
    {"id": "RFM.pt", "nome": "RFM", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/rfm.png"},
    {"id": "FamaRadio.pt", "nome": "Fama Rádio", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/famaradio.png"},
    {"id": "Observador.pt", "nome": "Observador", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/observador.png"},
    {"id": "TSF.pt", "nome": "TSF", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tsf.png"},
    {"id": "M80.pt", "nome": "M80", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/m80.png"},
    {"id": "VozSantoTirso.pt", "nome": "Rádio Voz Santo Tirso", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiovozsantotirso.png"},
    {"id": "MegaHits.pt", "nome": "MegaHits", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/megahits.png"},
    {"id": "NovaEra.pt", "nome": "Nova Era", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/novaera.png"},
    {"id": "MEOSudoeste.pt", "nome": "MEO Sudoeste", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/meosudoeste.png"},
    {"id": "Orbital.pt", "nome": "Orbital", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/orbital.png"},
    {"id": "Nove3Cinco.pt", "nome": "Nove3Cinco", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/nove3cinco.png"},
    {"id": "CidadeFM.pt", "nome": "Cidade FM", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadefm.png"},
    {"id": "CidadeHoje.pt", "nome": "Cidade Hoje", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadehoje.png"},
    {"id": "TugaFM.pt", "nome": "Tuga FM", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tugafm.png"}
]

# Criação do elemento raiz <tv>
root = ET.Element('tv')

# Obtém a hora atual e ajusta para a próxima hora cheia (minutos = 0)
current_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

# Define a programação de hora em hora para os próximos 7 dias
for radio in radios:
    # Adiciona o canal da rádio
    channel = ET.SubElement(root, 'channel', id=radio["id"])
    display_name = ET.SubElement(channel, 'display-name')
    display_name.text = radio["nome"]
    
    icon = ET.SubElement(channel, 'icon', src=radio["logo"])

    for i in range(168):  # 168 horas em 7 dias
        start_time = current_time + timedelta(hours=i)
        end_time = start_time + timedelta(hours=1)

        # Formata as datas no formato XMLTV (YYYYMMDDHHMMSS + timezone)
        start_str = start_time.strftime('%Y%m%d%H%M%S +0000')
        end_str = end_time.strftime('%Y%m%d%H%M%S +0000')

        # Cria o elemento <programme>
        programme = ET.SubElement(root, 'programme', start=start_str, stop=end_str, channel=radio["id"])
        
        # Adiciona o título do programa
        title = ET.SubElement(programme, 'title', lang="pt")
        title.text = radio["nome"]

        # Adiciona a descrição do programa
        description = ET.SubElement(programme, 'desc', lang="pt")
        description.text = f"Programação contínua da rádio {radio['nome']}."

        # Adiciona o ícone do programa
        icon = ET.SubElement(programme, 'icon', src=radio["logo"])

# Salva o arquivo XML no diretório raiz do projeto
tree = ET.ElementTree(root)
tree.write('epg-radios-pt.xml', encoding='utf-8', xml_declaration=True)
