import gzip
from lxml import etree
import os

def corrigir_xml(file_path):
    try:
        # Descomprimir o arquivo .xml.gz e ler como bytes
        with gzip.open(file_path, 'rb') as f:
            xml_content = f.read().decode('utf-8', errors='ignore')  # Ignorar caracteres inválidos durante a decodificação

        # Corrigir tags abertas/fechadas incorretamente
        parser = etree.XMLParser(recover=True)  # Configurado para corrigir pequenos erros automaticamente
        root = etree.fromstring(xml_content.encode('utf-8'), parser=parser)  # Reconvertido para bytes

        # Salvar o XML corrigido temporariamente
        temp_file = "temp.xml"
        with open(temp_file, "wb") as f:
            f.write(etree.tostring(root, pretty_print=True, encoding="UTF-8", xml_declaration=True))

        # Comprimir novamente e substituir o arquivo original
        with open(temp_file, 'rb') as f_in, gzip.open(file_path, 'wb') as f_out:
            f_out.writelines(f_in)

        # Remover o arquivo temporário
        os.remove(temp_file)
        print(f"Correção concluída e substituída para o arquivo: {file_path}")

    except Exception as e:
        print(f"Erro ao corrigir o XML para o arquivo {file_path}: {e}")

# Lista de arquivos EPG para corrigir
epg_files = [
    'EPG/epg-pt.xml.gz'
]

# Corrigir e substituir todos os arquivos da lista
for file_path in epg_files:
    corrigir_xml(file_path)
