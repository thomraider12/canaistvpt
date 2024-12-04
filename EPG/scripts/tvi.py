import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import gzip
from xml.dom import minidom

# Lista de canais e seus dados
canais = [
    {
        'id': 'tvi',
        'nome': 'TVI',
        'icon': 'https://cdn.iol.pt/img/logostvi/branco/tvi.png',
        'url_base': 'https://tvi.iol.pt/emissao/dia/tvi?data='
    },
    {
        'id': 'cnnpt',
        'nome': 'CNN Portugal',
        'icon': 'https://cdn.iol.pt/img/logostvi/branco/cnn.png',
        'url_base': 'https://tvi.iol.pt/emissao/dia/cnn?data='
    },
    {
        'id': 'vmaistvi',
        'nome': 'V+TVI',
        'icon': 'https://cdn.iol.pt/img/logostvi/branco/vmaistvi.png',
        'url_base': 'https://tvi.iol.pt/emissao/dia/vmais?data='
    },
    {
        'id': 'tvireality',
        'nome': 'TVI Reality',
        'icon': 'https://cdn.iol.pt/img/logostvi/branco/tvireality.png',
        'url_base': 'https://tvi.iol.pt/emissao/dia/tvireality?data='
    },
    {
        'id': 'tviinternacional',
        'nome': 'TVI Internacional',
        'icon': 'https://cdn.iol.pt/img/logostvi/branco/tviinternacional.png',
        'url_base': 'https://tvi.iol.pt/emissao/dia/tviinternacional?data='
    },
    {
        'id': 'tviafrica',
        'nome': 'TVI África',
        'icon': 'https://cdn.iol.pt/img/logostvi/branco/tviafrica.png',
        'url_base': 'https://tvi.iol.pt/emissao/dia/tviafrica?data='
    }
]

# Quantos dias futuros processar
dias_a_extrair = 11

# Criar a estrutura XMLTV
raiz = ET.Element('tv')

# Adicionar canais à estrutura XML
for canal in canais:
    canal_elemento = ET.SubElement(raiz, 'channel', {'id': canal['id']})
    ET.SubElement(canal_elemento, 'display-name').text = canal['nome']
    ET.SubElement(canal_elemento, 'icon', {'src': canal['icon']})

# Função para processar a programação de um canal para um dia específico
def processar_programacao(canal, data):
    url = f"{canal['url_base']}{data.strftime('%Y-%m-%d')}"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a programação de {canal['nome']} para {data}: {e}")
        return
    
    # Processar o HTML
    sopa = BeautifulSoup(resposta.text, 'html.parser')
    programas = sopa.find_all('div', class_='guiatv-linha')
    
    # Guardar dados para calcular "stop"
    lista_programas = []
    for programa in programas:
        # Extrair dados do programa
        hora = programa.find('div', class_='hora').text.strip() if programa.find('div', class_='hora') else '00:00'
        hora_formatada = hora.replace(':', '') + '00'  # HHMMSS
        start = f"{data.strftime('%Y%m%d')}{hora_formatada}"
        
        titulo = programa.find('h2').text.strip() if programa.find('h2') else 'Sem título'
        descricao = programa.find('div', class_='texto texto2').text.strip() if programa.find('div', class_='texto texto2') else 'Sem descrição'
        div_capa = programa.find('div', class_='capaPrograma').find('div', class_='picture16x9') if programa.find('div', class_='capaPrograma') else None
        
        # Adicionar à lista temporária
        lista_programas.append({
            'start': start,
            'title': titulo,
            'desc': descricao,
            'div_capa': div_capa
        })
    
    # Adicionar programas ao XML com "stop" e imagem
    for i, programa in enumerate(lista_programas):
        start = programa['start']
        stop = lista_programas[i + 1]['start'] if i + 1 < len(lista_programas) else f"{data.strftime('%Y%m%d')}235959"

        # Extrair URL da imagem (se existir)
        div_capa = programa.get('div_capa')
        url_imagem = ""
        if div_capa:
            estilo = div_capa.get('style', '')
            if 'background-image:url(' in estilo:
                url_imagem = estilo.split('background-image:url(')[1].split(')')[0].strip()
        
        # Adicionar programa ao XML
        elemento_programa = ET.SubElement(raiz, 'programme', {
            'start': start,
            'stop': stop,
            'channel': canal['id']
        })
        ET.SubElement(elemento_programa, 'title').text = programa['title']
        ET.SubElement(elemento_programa, 'desc').text = programa['desc']
        if url_imagem:
            ET.SubElement(elemento_programa, 'icon', {'src': url_imagem})

# Processar a programação para todos os canais e dias
for dia_offset in range(dias_a_extrair):
    data = datetime.now() + timedelta(days=dia_offset)
    for canal in canais:
        print(f"Processando canal {canal['nome']} para o dia {data.strftime('%Y-%m-%d')}...")
        processar_programacao(canal, data)

# Gerar o XML final
xml_str = minidom.parseString(ET.tostring(raiz, encoding='utf-8')).toprettyxml(indent="  ")
with gzip.open('epg-tvi-pt.xml.gz', 'wb') as f:
    f.write(xml_str.encode('utf-8'))

print("Arquivo XMLTV gerado com sucesso: epg-tvi-pt.xml.gz")