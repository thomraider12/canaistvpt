import gzip
import xml.etree.ElementTree as ET
from datetime import datetime

def carregar_xmltv_gz(arquivo_gz):
    with gzip.open(arquivo_gz, 'rt', encoding='utf-8') as file:
        return ET.parse(file)

def converter_data(xmltv_data):
    try:
        data = datetime.strptime(xmltv_data[:14], "%Y%m%d%H%M%S")
        return data.strftime("%d-%m-%Y %H:%M")
    except ValueError:
        return "Data inválida"

def buscar_programas_por_canal(tree, canal_id):
    root = tree.getroot()
    programas = []

    for programa in root.findall('programme'):
        canal = programa.get('channel')
        if canal == canal_id:
            titulo = programa.find('title').text if programa.find('title') is not None else "Sem título"
            descricao = programa.find('desc').text if programa.find('desc') is not None else "Sem descrição"
            icon_elem = programa.find('icon')
            imagem = icon_elem.get('src') if icon_elem is not None else "Sem imagem"
            hora_inicio = converter_data(programa.get('start'))
            hora_fim = converter_data(programa.get('stop'))
            programas.append((titulo, descricao, imagem, hora_inicio, hora_fim))
    return programas


def main():
    arquivo_gz = input("Digite o caminho do arquivo XMLTV (ex: 'guia.xmltv.gz'): ")
    tree = carregar_xmltv_gz(arquivo_gz)

    canal_id = input("Digite o xmltv_id do canal que deseja procurar: ")
    programas = buscar_programas_por_canal(tree, canal_id)

    if programas:
        print(f"\nProgramas para o canal {canal_id}:\n")
        for titulo, descricao, imagem, hora_inicio, hora_fim in programas:
            print(f"Título: {titulo}")
            print(f"Descrição: {descricao}")
            print(f"Imagem: {imagem}")
            print(f"Início: {hora_inicio}")
            print(f"Término: {hora_fim}\n")
    else:
        print(f"Nenhum programa encontrado para o canal {canal_id}.")

if __name__ == "__main__":
    main()