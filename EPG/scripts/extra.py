import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from xml.dom import minidom
import requests
import json
import gzip

# Função para obter dados das rádios da RTP
def obter_dados_radios_rtp():
    url_base = "https://www.rtp.pt/EPG/json/rtp-home-page-tv-radio/list-all-grids/radio"
    epg_radios = {}

    # Loop para pegar dados dos próximos 7 dias
    for i in range(7):
        data_formatada = (datetime.now() + timedelta(days=i)).strftime("%d-%m-%Y")
        url = f"{url_base}/{data_formatada}"
        
        response = requests.get(url)
        if response.status_code == 200:
            dados_dia = response.json().get("result", {})
            for canal, programas in dados_dia.items():
                print(f"Extraindo dados para {canal} no dia {data_formatada}")
                if canal not in epg_radios:
                    epg_radios[canal] = {}
                for periodo, lista_programas in programas.items():
                    if periodo != '_info':
                        if periodo in epg_radios[canal]:
                            epg_radios[canal][periodo].extend(lista_programas)
                        else:
                            epg_radios[canal][periodo] = lista_programas
        else:
            print(f"Erro ao obter EPG para {data_formatada}: {response.status_code}")

    return epg_radios

# Criação do elemento raiz <tv>
root = ET.Element('tv')

canais_extras = [
    {"id": "Fogos.pt", "nome": "ACOMPANHE A SITUAÇÃO DOS INCÊNDIOS EM PORTUGAL", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/fogos.png", "desc": "Atualizado de 15 em 15 minutos com informação geral, e de seguida info dos incêncios com >90 operacionais. É um canal temporário enquanto Portugal passa por esta crise."},
    {"id": "RTPDesporto1.pt", "nome": "RTP Desporto 1", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/rtpdesporto1.png", "desc": ""},
    {"id": "RTPDesporto2.pt", "nome": "RTP Desporto 2", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/rtpdesporto2.png", "desc": ""},
    {"id": "Linear.pt", "nome": "Linear - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/linear.png", "desc": "A rádio de Vila do Conde\n\nA Rádio Linear é a rádio de Vila do Conde, distrito do Porto.\nA sua programação é bastante variada, mas da mesma podem destacar-se Hora Desportiva,\nSucessos Linear e o Diário de Vila do Conde, entre outros programas."},
    {"id": "Radio5.pt", "nome": "Rádio 5 - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radio5.png", "desc": "Só música portuguesa.\n\nEm 89FM e 88.4FM para o Grande Porto, a\nRádio 5 dedica 24 horas por dia à música dos portugueses.\nCom emissão online."},
    {"id": "OndaViva.pt", "nome": "Onda Viva - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/ondaviva.png", "desc": "No ar desde o final dos anos 80,\na Rádio Onda Viva é uma das rádios mais ouvidos do Litoral Norte Português.\nA sua programação é variada e inclui desporto, música, entretenimento, passatempos e muito mais."},
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
    {"id": "VozSantoTirso.pt", "nome": "Rádio Voz Santo Tirso - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiovozsantotirso.png", "desc": "Uma voz amiga\n\nA Rádio Voz de Santo Tirso é uma estação local, generalista com uma programação diversificada,\ncultural, entertenimento e musical de forma a integrar os valores artísticos\nlocais, nacionais e estrangeiros."},
    {"id": "MegaHits.pt", "nome": "MegaHits - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/megahits.png", "desc": "Mais Música Nova\n45 minutos de música sem parar."},
    {"id": "NovaEra.pt", "nome": "Nova Era - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/novaera.png", "desc": "Música Sem Parar.\nAnimar, agitar e fazer vibrar os melhores ouvintes do Mundo."},
    {"id": "RadioSudoeste.pt", "nome": "Rádio Sudoeste - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiosudoeste.png", "desc": "Um Festival de Rádio dedicado ao festival MEO Sudoeste, promovido pelo grupo Altice e originalmente chamado Festival Sudoeste na década de 1990.\nAtualmente, também é uma estação de rádio com várias frequências em Portugal."},
    {"id": "Orbital.pt", "nome": "Orbital - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/orbital.png", "desc": "A dar-te música."},
    {"id": "Nove3Cinco.pt", "nome": "Nove3Cinco - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/nove3cinco.png", "desc": "Esta é a Rádio Deejay.\nRádio da Póvoa de Lanhoso"},
    {"id": "CidadeFM.pt", "nome": "Cidade FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadefm.png", "desc": "Só se quiseres\nA 1ª rádio dos éxitos."},
    {"id": "CidadeHoje.pt", "nome": "Cidade Hoje - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadehoje.png", "desc": "Rádio e Jornal de Vila Nova de Famalicão\nCidade Hoje Rádio"},
    {"id": "TugaFM.pt", "nome": "Tuga FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/tugafm.png", "desc": "Rádio à tua medida.\nFoi fundada em 2019 com o intuito de marcar a sua diferença com outro género de músicas."},
    {"id": "TruckersFM.uk", "nome": "TruckersFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/truckersfm.png", "desc": "Your Drive, Your Music.\nRádio feita para conduzir.\nO teu destino para uma ótima música.\nNo ar desde 2015, Truckers.FM é uma estação de rádio que serve motoristas e a comunidade de jogos de simulação.\nFocada principalmente em tocar músicas do chart."},
    {"id": "HiperFM.pt", "nome": "HiperFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/hiperfm.png", "desc": "A Hiper FM, localizada no distrito de Santarém e a emitir em 104.6 FM, é uma rádio dinâmica e jovem,\nque aposta em música Rock, Pop e Dance e conta com a colaboração de vários DJs de renome."},
    {"id": "RadioOxigenio.pt", "nome": "Oxigénio - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/oxigenio.png", "desc": "Localizada em Lisboa, a Rádio Oxigénio foi fundada em 1999 com o objetivo de trazer uma lufada de ar fresco aos ouvintes conhecedores de música.\nA sua programação musical inclui uma grande variedade de géneros."},
    {"id": "RadioRadar.pt", "nome": "Radar - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radar.png", "desc": "A Rádio Radar é uma rádio local, localizada na área da Grande Lisboa, e focada num estilo musical alternativo.\nPela Radar passou o famoso radialista António Sérgio com o programa Viriato 25."},
    {"id": "RadioSmoothFM.pt", "nome": "Smooth FM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/smoothfm.png", "desc": "Parte do grupo Media Capital, a Smooth FM está no ar desde 2011 e transmite para as cidades de Lisboa e Porto e zona centro. A sua programação musical centra-se em jazz, blues e soul."},
    {"id": "RadioSuperFM.pt", "nome": "SuperFM - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/superfm.png", "desc": "A Super FM é uma rádio diferente, inovadora e com espírito, que passa os grandes êxitos do Rock e da Pop. Alguns dos seus locutores mais conhecidos são Diogo Batáguas, Ana Lucas e Mónica Amaral."},
    {"id": "batidafm.pt", "nome": "batida.fm - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/batidafm.png", "desc": "A Batida FM é direcionada aos ouvintes jovens adultos.\nCriada em 2011, numa parceria entre a Vodafone e a Media Capital Rádios, emite essencialmente música indie e rock alternativo nas cidades de Lisboa, Porto e Coimbra."},
    {"id": "CidadeHipHop.pt", "nome": "Cidade HipHop - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/cidadefm.png", "desc": "Só se quiseres\nA 1ª rádio dos éxitos."},
    {"id": "RadioZigZag.pt", "nome": "ZigZag - Direto", "logo": "https://raw.githubusercontent.com/thomraider12/icones_tv/main/radiozigzag.png", "desc": ""}
]

# Obtém a hora atual e ajusta para a próxima hora cheia (minutos = 0)
current_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

# Adiciona canais extras
for canais_extra in canais_extras:
    # Adiciona o canal da rádio
    channel = ET.SubElement(root, 'channel', id=canais_extra["id"])
    display_name = ET.SubElement(channel, 'display-name')
    display_name.text = canais_extra["nome"]

    icon = ET.SubElement(channel, 'icon', src=canais_extra["logo"])

    for i in range(168):  # 168 horas em 7 dias
        start_time = current_time + timedelta(hours=i)
        end_time = start_time + timedelta(hours=1)

        start_str = start_time.strftime('%Y%m%d%H%M%S +0000')
        end_str = end_time.strftime('%Y%m%d%H%M%S +0000')

        programme = ET.SubElement(root, 'programme', start=start_str, stop=end_str, channel=canais_extra["id"])
        title = ET.SubElement(programme, 'title', lang="pt")
        title.text = canais_extra["nome"]
        description = ET.SubElement(programme, 'desc', lang="pt")
        description.text = canais_extra["desc"]
        icon = ET.SubElement(programme, 'icon', src=canais_extra["logo"])

# Obter dados das rádios da RTP
epg_radios = obter_dados_radios_rtp()

# Adicionar dados das rádios ao XML
for canal, programas in epg_radios.items():
    channel = ET.SubElement(root, 'channel', id=canal)
    display_name = ET.SubElement(channel, 'display-name')
    display_name.text = canal  # ou outro nome se disponível

    for periodo, lista_programas in programas.items():
        for programa in lista_programas:
            start_time = datetime.strptime(programa["date"], "%Y-%m-%d %H:%M:%S")
            start_str = start_time.strftime('%Y%m%d%H%M%S +0000')
            stop_time = start_time + timedelta(hours=1)  # Duração padrão de 1 hora
            end_str = stop_time.strftime('%Y%m%d%H%M%S +0000')

            programme = ET.SubElement(root, 'programme', start=start_str, stop=end_str, channel=canal)
            title = ET.SubElement(programme, 'title', lang="pt")
            title.text = programa["name"]
            description = ET.SubElement(programme, 'desc', lang="pt")
            description.text = programa["description"]

def formatar_xml(element):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Salva o arquivo XML comprimido no formato .gz
try:
    xml_pretty = formatar_xml(root)
    with gzip.open('../epg-extra.xml.gz', 'wt', encoding='utf-8') as f:
        f.write(xml_pretty)
    sucesso = True
except Exception as e:
    print("Erro: " + str(e))
    sucesso = False

if sucesso:
    print("Ficheiro comprimido escrito com sucesso!")
else:
    print("Erro desconhecido.")
