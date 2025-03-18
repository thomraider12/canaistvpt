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
        'id': 'tvificcao',
        'nome': 'TVI Ficção',
        'icon': 'https://cdn.iol.pt/img/logostvi/branco/tvificcao.png',
        'url_base': 'https://tviplayer.iol.pt/ajax/guiatv/grelha/TVI_FICCAO/'
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

# ...existing code...

# Função para processar os canais "normais"
def processar_programacao(canal, data):
    url = f"{canal['url_base']}{data.strftime('%Y-%m-%d')}"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        print(f"Processado o canal {canal['nome']} para o dia {data.strftime('%Y-%m-%d')}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a programação de {canal['nome']} para {data}: {e}")
        return
    
    sopa = BeautifulSoup(resposta.text, 'html.parser')
    programas = sopa.find_all('div', class_='guiatv-linha')
    
    lista_programas = []
    for programa in programas:
        hora = programa.find('div', class_='hora').text.strip() if programa.find('div', class_='hora') else '00:00'
        hora_formatada = hora.replace(':', '') + '00'
        start = f"{data.strftime('%Y%m%d')}{hora_formatada}"
        
        titulo = programa.find('h2').text.strip() if programa.find('h2') else 'Sem título'
        descricao = programa.find('div', class_='texto texto2').text.strip() if programa.find('div', class_='texto texto2') else 'Sem descrição'
        # Encontrar a div da imagem do programa (se existir)
        div_capa = programa.find('div', class_='capaPrograma').find('div', class_='picture16x9') if programa.find('div', class_='capaPrograma') else None

        
        lista_programas.append({
            'start': start,
            'title': titulo,
            'desc': descricao,
            'div_capa': div_capa
        })
    
    for i, programa in enumerate(lista_programas):
        start = programa['start']
        stop = lista_programas[i + 1]['start'] if i + 1 < len(lista_programas) else f"{data.strftime('%Y%m%d')}235959"
        
        elemento_programa = ET.SubElement(raiz, 'programme', {
            'start': start,
            'stop': stop,
            'channel': canal['id']
        })
        ET.SubElement(elemento_programa, 'title').text = programa['title']
        ET.SubElement(elemento_programa, 'desc').text = programa['desc']
        # Extrair URL da imagem (se existir)
        div_capa = programa.get('div_capa')
        url_imagem = ""
        if div_capa:
            estilo = div_capa.get('style', '')
            if 'background-image:url(' in estilo:
                url_imagem = estilo.split('background-image:url(')[1].split(')')[0].strip()
        if url_imagem:
             ET.SubElement(elemento_programa, 'icon', {'src': url_imagem})
        
    print(f"Programas adicionados para o canal {canal['nome']}: {lista_programas}")

# Função para processar a programação do TVI Ficção
def processar_programacao_tvificcao(canal, data):
    data_inicio = data.strftime('%Y-%m-%d')
    data_fim = (data + timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"{canal['url_base']}{data_inicio},{data_fim}"
    
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        print(f"Processado o canal {canal['nome']} para o dia {data.strftime('%Y-%m-%d')}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a programação de {canal['nome']} para {data}: {e}")
        return
    
    sopa = BeautifulSoup(resposta.text, 'html.parser')
    grelha = sopa.find_all('tr')
    
    lista_programas = []
    for linha in grelha:
        hora = linha.find('span', class_='hora')
        titulo = linha.find('a', class_='programa')
        if hora and titulo:
            hora_formatada = hora.text.strip().replace(':', '') + '00'
            start = f"{data.strftime('%Y%m%d')}{hora_formatada}"
            titulo_texto = titulo.text.strip()

            lista_programas.append({'start': start, 'title': titulo_texto, 'desc': ''})
    
    for i, programa in enumerate(lista_programas):
        start = programa['start']
        stop = lista_programas[i + 1]['start'] if i + 1 < len(lista_programas) else f"{data.strftime('%Y%m%d')}235959"
        
        elemento_programa = ET.SubElement(raiz, 'programme', {
            'start': start,
            'stop': stop,
            'channel': canal['id']
        })
        ET.SubElement(elemento_programa, 'title').text = programa['title']
        ET.SubElement(elemento_programa, 'desc').text = programa['desc']

    print(f"Programas adicionados para o canal {canal['nome']}: {lista_programas}")

# Processar a programação para todos os canais e dias
for dia_offset in range(dias_a_extrair):
    data = datetime.now() + timedelta(days=dia_offset)
    for canal in canais:
        if canal['id'] == 'tvificcao':
            processar_programacao_tvificcao(canal, data)
        else:
            processar_programacao(canal, data)

# Gerar o XML final
xml_str = minidom.parseString(ET.tostring(raiz, encoding='utf-8')).toprettyxml(indent="  ")
with gzip.open('epg-tvi-pt.xml.gz', 'wb') as f:
    f.write(xml_str.encode('utf-8'))

print("Arquivo XMLTV gerado com sucesso: epg-tvi-pt.xml.gz")