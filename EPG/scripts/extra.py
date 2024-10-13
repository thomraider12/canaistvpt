import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

canais_extras = [
    {"id": "GoloFM.pt", "nome": "Golo FM - Desporto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/golofm.png", "desc": "A Primeira Rádio Desporto.\nA maior fábrica de notícias de Portugal que pode ouvir em FM e online."},
    {"id": "AviaçãoTV.pt", "nome": "AviaçãoTV - Direto (Lisboa)", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/aviaçãotv.png", "desc": "Assiste ao aeroporto de Lisboa em direto todos os dias."},
    {"id": "OnFM.pt", "nome": "OnFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/onfm.png", "desc": "Liga-te.\nA OnFM é a primeira visual rádio em Portugal."},
    {"id": "DJTomasA", "nome": "DJ Tomás Afonso", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tomasafonso.ico", "desc": "Ouve o DJ Tomás Afonso."},
    {"id": "RadioComercial.pt", "nome": "Rádio Comercial - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiocomercial.png", "desc": "A Melhor Música, sempre.\nEm casa, no carro em todo o lado."},
    {"id": "RFM.pt", "nome": "RFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/rfm.png", "desc": "Só grandes músicas."},
    {"id": "FamaRadio.pt", "nome": "Fama Rádio - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/famaradio.png", "desc": "A Melhor Seleção de Todas.\nUma estação de Rádio FM com um forte posicionamento nos clássicos; PopRock; anos 80 90 e 00, alternativo às atuais ofertas deste segmento."},
    {"id": "Observador.pt", "nome": "Observador - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/observador.png", "desc": "O Observador é um jornal diário online, independente e livre."},
    {"id": "TSF.pt", "nome": "TSF - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tsf.png", "desc": "Vamos ao fim da rua, Vamos ao fim do mundo.\nThe reference for radio news in Portugal."},
    {"id": "M80.pt", "nome": "M80 - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/m80.png", "desc": "Se a sua vida tem uma música, ela passa na M80."},
    {"id": "VozSantoTirso.pt", "nome": "Rádio Voz Santo Tirso - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiovozsantotirso.png", "desc": "Uma voz amiga\nA Rádio Voz de Santo Tirso é uma estação local, generalista com uma programação diversificada, cultural, entertenimento e musical de forma a integrar os valores artísticos locais, nacionais e estrangeiros."},
    {"id": "MegaHits.pt", "nome": "MegaHits - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/megahits.png", "desc": "Mais Música Nova\n45 minutos de música sem parar"},
    {"id": "NovaEra.pt", "nome": "Nova Era - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/novaera.png", "desc": "Música Sem Parar.\nAnimar, agitar e fazer vibrar os melhores ouvintes do Mundo."},
    {"id": "MEOSudoeste.pt", "nome": "MEO Sudoeste - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/meosudoeste.png", "desc": "Um Festival de Rádio\nDedicated to festival Meo Sudoeste, promoted by Altice group and originally named Festival Sudoeste in portuguese southwest in The 1990 decade. Actually is also on radio station with various frequences in Portugal."},
    {"id": "Orbital.pt", "nome": "Orbital - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/orbital.png", "desc": "A dar te música."},
    {"id": "Nove3Cinco.pt", "nome": "Nove3Cinco - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/nove3cinco.png", "desc": "Esta é a Rádio Deejay.\nRadio from Póvoa de Lanhoso"},
    {"id": "CidadeFM.pt", "nome": "Cidade FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadefm.png", "desc": "Só se quiseres\nA 1ª rádio dos exitos."},
    {"id": "CidadeHoje.pt", "nome": "Cidade Hoje - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadehoje.png", "desc": "Rádio e Jornal de Vila Nova de Famalicão\nCidade Hoje Rádio"},
    {"id": "TugaFM.pt", "nome": "Tuga FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tugafm.png", "desc": "Tuga FM."},
    {"id": "TruckersFM.uk", "nome": "TruckersFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/truckersfm.png", "desc": "Your Drive, Your Music. Radio made for driving. Your destination for great music.\nOn Air since 2015, Truckers.FM is an radio station that serves drivers, and the simulation gaming community.\nFocused primary on playing chart."}
]

# Criação do elemento raiz <tv>
root = ET.Element('tv')

# Obtém a hora atual e ajusta para a próxima hora cheia (minutos = 0)
current_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

# Define a programação de hora em hora para os próximos 7 dias
for canais_extra in canais_extras:
    # Adiciona o canal da rádio
    channel = ET.SubElement(root, 'channel', id=canais_extra["id"])
    display_name = ET.SubElement(channel, 'display-name')
    display_name.text = canais_extra["nome"]

    icon = ET.SubElement(channel, 'icon', src=canais_extra["logo"])

    for i in range(168):  # 168 horas em 7 dias
        start_time = current_time + timedelta(hours=i)
        end_time = start_time + timedelta(hours=1)

        # Formata as datas no formato XMLTV (YYYYMMDDHHMMSS + timezone)
        start_str = start_time.strftime('%Y%m%d%H%M%S +0000')
        end_str = end_time.strftime('%Y%m%d%H%M%S +0000')

        # Cria o elemento <programme>
        programme = ET.SubElement(root, 'programme', start=start_str, stop=end_str, channel=canais_extra["id"])

        # Adiciona o título do programa
        title = ET.SubElement(programme, 'title', lang="pt")
        title.text = canais_extra["nome"]

        # Adiciona a descrição do programa
        description = ET.SubElement(programme, 'desc', lang="pt")
        description.text = canais_extra["desc"]

        # Adiciona o ícone do programa
        icon = ET.SubElement(programme, 'icon', src=canais_extra["logo"])

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
