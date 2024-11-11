import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

canais_extras = [
    {"id": "FamaTV.pt", "nome": "FamaTV - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/famatv.png", "desc": "A FamaTV é uma televisão/publicação local generalista, com raízes em Vila Nova de Famalicão, mas atenta aos acontecimentos e valores dos municípios limítrofes.\nA FamaTV esforça-se por apresentar uma programação interessante e atual promovendo as características da cultura local e regional."},
    {"id": "GoloFM.pt", "nome": "Golo FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/golofm.png", "desc": "A Primeira Rádio Desporto.\nA maior fábrica de notícias de Portugal que pode ouvir em FM e online."},
    {"id": "AviaçãoTV.pt", "nome": "AviaçãoTV - Direto (Lisboa)", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/aviaçãotv.png", "desc": "Assiste ao aeroporto de Lisboa em direto todos os dias."},
    {"id": "OnFM.pt", "nome": "OnFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/onfm.png", "desc": "Liga-te.\nA OnFM é a primeira visual rádio em Portugal."},
    {"id": "RadioComercial.pt", "nome": "Rádio Comercial - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiocomercial.png", "desc": "A Melhor Música, sempre.\nEm casa, no carro em todo o lado."},
    {"id": "RFM.pt", "nome": "RFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/rfm.png", "desc": "Só grandes músicas."},
    {"id": "RadioRenascença.pt", "nome": "Rádio Renascença - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/renascença.png", "desc": "A par com o mundo."},
    {"id": "CMRadio.pt", "nome": "CM Rádio - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cmradio.png", "desc": "CM Rádio.\nA vida ao vivo."},
    {"id": "Observador.pt", "nome": "Observador - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/observador.png", "desc": "O Observador é um jornal diário online, independente e livre."},
    {"id": "FamaRadio.pt", "nome": "Fama Rádio - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/famaradio.png", "desc": "A Melhor Seleção de Todas.\nUma estação de Rádio FM com um forte posicionamento nos clássicos; PopRock; anos 80 90 e 00, alternativo às atuais ofertas deste segmento."},
    {"id": "TSF.pt", "nome": "TSF - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tsf.png", "desc": "Vamos ao fim da rua, Vamos ao fim do mundo.\nThe reference for radio news in Portugal."},
    {"id": "M80.pt", "nome": "M80 - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/m80.png", "desc": "Se a sua vida tem uma música, ela passa na M80."},
    {"id": "VozSantoTirso.pt", "nome": "Rádio Voz Santo Tirso - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiovozsantotirso.png", "desc": "Uma voz amiga A Rádio Voz de Santo Tirso é uma estação local, generalista com uma programação diversificada, cultural, entertenimento e musical de forma a integrar os valores artísticos locais, nacionais e estrangeiros."},
    {"id": "MegaHits.pt", "nome": "MegaHits - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/megahits.png", "desc": "Mais Música Nova\n45 minutos de música sem parar."},
    {"id": "NovaEra.pt", "nome": "Nova Era - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/novaera.png", "desc": "Música Sem Parar.\nAnimar, agitar e fazer vibrar os melhores ouvintes do Mundo."},
    {"id": "MEOSudoeste.pt", "nome": "MEO Sudoeste - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/meosudoeste.png", "desc": "Um Festival de Rádio dedicated to festival MEO Sudoeste, promoted by Altice group and originally named Festival Sudoeste in portuguese southwest in the 1990 decade.\nActually is also on radio station with various frequences in Portugal."},
    {"id": "Orbital.pt", "nome": "Orbital - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/orbital.png", "desc": "A dar te música."},
    {"id": "Nove3Cinco.pt", "nome": "Nove3Cinco - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/nove3cinco.png", "desc": "Esta é a Rádio Deejay.\nRadio from Póvoa de Lanhoso"},
    {"id": "CidadeFM.pt", "nome": "Cidade FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadefm.png", "desc": "Só se quiseres\nA 1ª rádio dos exitos."},
    {"id": "CidadeHoje.pt", "nome": "Cidade Hoje - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadehoje.png", "desc": "Rádio e Jornal de Vila Nova de Famalicão\nCidade Hoje Rádio"},
    {"id": "TugaFM.pt", "nome": "Tuga FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tugafm.png", "desc": "Rádio à tua medida.\nFoi fundada em 2019 com intuito de marcar a sua diferença com outro genero de musicas."},
    {"id": "TruckersFM.uk", "nome": "TruckersFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/truckersfm.png", "desc": "Your Drive, Your Music.\nRadio made for driving.\nYour destination for great music.\nOn Air since 2015, Truckers.FM is an radio station that serves drivers, and the simulation gaming community.\nFocused primary on playing chart."},
    {"id": "HiperFM.pt", "nome": "HiperFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/hiperfm.png", "desc": "A Hiper FM, localizada no distrito de Santarém e a emitir em 104.6 FM, é uma rádio dinâmica e jovem,\nque aposta em música Rock, Pop e Dance e conta com a colaboração de vários DJs de renome."},
    {"id": "RadioOxigenio.pt", "nome": "Oxigénio - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/oxigenio.png", "desc": "Localizada em Lisboa, a Rádio Oxigénio foi fundada em 1999 com o objetivo de trazer uma lufada de ar fresco aos ouvintes conhecedores de música.\nA sua programação musical inclui uma grande variedade de géneros."},
    {"id": "RadioRadar.pt", "nome": "Radar - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radar.png", "desc": "A Rádio Radar é uma rádio local, localizada na área da Grande Lisboa, e focada num estilo musical alternativo.\nPela Radar passou o famoso radialista António Sérgio com o programa Viriato 25."},
    {"id": "RadioSmoothFM.pt", "nome": "Smooth FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/smoothfm.png", "desc": "Parte do grupo Media Capital, a Smooth FM está no ar desde o ano de 2011 e transmite para as cidades de Lisboa e Porto e zona centro. A sua programação musical centra-se em jazz, blues e soul."},
    {"id": "RadioSuperFM.pt", "nome": "SuperFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/superfm.png", "desc": "A Super FM é uma rádio diferente, inovadora e com espírito, que passa os grandes êxitos do Rock e da Pop. Alguns dos seus locutores mais conhecidos são Diogo Batáguas, Ana Lucas e Mónica Amaral."},
    {"id": "batidafm.pt", "nome": "batida.fm - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/batidafm.png", "desc": "A  Batida FM é direcionada aos ouvintes jovens adultos.\nCriada em 2011, numa parceria entre a Vodafone e a Media Capital Rádios, emite essencialmente música indie e rock alternativo nas cidades de Lisboa, Porto e Coimbra."},
    {"id": "CidadeHipHop.pt", "nome": "Cidade HipHop - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadefm.png", "desc": "Só se quiseres\nA 1ª rádio dos exitos."}
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
    tree.write('../epg-extra.xml', encoding='utf-8', xml_declaration=True)
    sucesso = True
except Exception as e:
    print("Erro: " + e)
if sucesso:
    print("Ficheiro escrito com sucesso!")
else:
    print("Erro desconhecido.")
