import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

canais_extras = [
    {"id": "AviaçãoTV.pt", "nome": "AviaçãoTV - Direto (Lisboa)", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/aviaçãotv.png"},
    {"id": "OnFM.pt", "nome": "OnFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/onfm.png"},
    {"id": "DJTomasA", "nome": "DJ Tomás Afonso", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tomasafonso.ico"},
    {"id": "RadioComercial.pt", "nome": "Rádio Comercial - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiocomercial.png"},
    {"id": "RFM.pt", "nome": "RFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/rfm.png"},
    {"id": "FamaRadio.pt", "nome": "Fama Rádio - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/famaradio.png"},
    {"id": "Observador.pt", "nome": "Observador - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/observador.png"},
    {"id": "TSF.pt", "nome": "TSF - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tsf.png"},
    {"id": "M80.pt", "nome": "M80 - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/m80.png"},
    {"id": "VozSantoTirso.pt", "nome": "Rádio Voz Santo Tirso - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiovozsantotirso.png"},
    {"id": "MegaHits.pt", "nome": "MegaHits - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/megahits.png"},
    {"id": "NovaEra.pt", "nome": "Nova Era - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/novaera.png"},
    {"id": "MEOSudoeste.pt", "nome": "MEO Sudoeste - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/meosudoeste.png"},
    {"id": "Orbital.pt", "nome": "Orbital - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/orbital.png"},
    {"id": "Nove3Cinco.pt", "nome": "Nove3Cinco - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/nove3cinco.png"},
    {"id": "CidadeFM.pt", "nome": "Cidade FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadefm.png"},
    {"id": "CidadeHoje.pt", "nome": "Cidade Hoje - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadehoje.png"},
    {"id": "TugaFM.pt", "nome": "Tuga FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tugafm.png"},
    {"id": "TruckersFM.uk", "nome": "TruckersFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/truckersfm.png"}
]

# Criação do elemento raiz <tv>
root = ET.Element('tv')

# Obtém a hora atual e ajusta para a próxima hora cheia (minutos = 0)
current_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

# Define a programação de hora em hora para os próximos 7 dias
for canais_extra in canais_extras:
    # Adiciona o canal da rádio
    channel = ET.SubElement(root, 'channel', id=canal_extra["id"])
    display_name = ET.SubElement(channel, 'display-name')
    display_name.text = canais_extra["nome"]

    icon = ET.SubElement(channel, 'icon', src=canal_extra["logo"])

    for i in range(168):  # 168 horas em 7 dias
        start_time = current_time + timedelta(hours=i)
        end_time = start_time + timedelta(hours=1)

        # Formata as datas no formato XMLTV (YYYYMMDDHHMMSS + timezone)
        start_str = start_time.strftime('%Y%m%d%H%M%S +0000')
        end_str = end_time.strftime('%Y%m%d%H%M%S +0000')

        # Cria o elemento <programme>
        programme = ET.SubElement(root, 'programme', start=start_str, stop=end_str, channel=canal_extra["id"])

        # Adiciona o título do programa
        title = ET.SubElement(programme, 'title', lang="pt")
        title.text = canal_extra["nome"]

        # Adiciona a descrição do programa
        description = ET.SubElement(programme, 'desc', lang="pt")
        description.text = f"Programação contínua de {canal_extra['nome']}."

        # Adiciona o ícone do programa
        icon = ET.SubElement(programme, 'icon', src=canal_extra["logo"])

# Salva o arquivo XML no diretório raiz do projeto
try:
    tree = ET.ElementTree(root)
    tree.write('../epg-extra-pt.xml', encoding='utf-8', xml_declaration=True)
    sucesso = True
except Exception as e:
    print("Erro: " + e)
if sucesso:
    print("Ficheiro escrito com sucesso!")
else:
    print("Erro desconhecido.")
