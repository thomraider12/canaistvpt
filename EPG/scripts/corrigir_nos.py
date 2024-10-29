import gzip
from lxml import etree

def corrigir_xml(input_file, output_file):
    try:
        # Descomprimir o arquivo .xml.gz e ler como bytes
        with gzip.open(input_file, 'rb') as f:
            xml_content = f.read().decode('utf-8', errors='ignore')  # Ignorar caracteres inválidos durante a decodificação

        # Corrigir tags abertas/fechadas incorretamente
        parser = etree.XMLParser(recover=True)  # Configurado para corrigir pequenos erros automaticamente
        root = etree.fromstring(xml_content.encode('utf-8'), parser=parser)  # Reconvertido para bytes

        # Salvar o XML corrigido temporariamente
        temp_file = "temp.xml"
        with open(temp_file, "wb") as f:
            f.write(etree.tostring(root, pretty_print=True, encoding="UTF-8", xml_declaration=True))

        # Comprimir novamente para .xml.gz
        with open(temp_file, 'rb') as f_in, gzip.open(output_file, 'wb') as f_out:
            f_out.writelines(f_in)

        print(f"Correção concluída. Arquivo corrigido salvo como {output_file}")

    except Exception as e:
        print(f"Erro ao corrigir o XML: {e}")

# Usar o script
input_file = 'EPG/epg-nos-pt.xml.gz'  # Caminho para o arquivo problemático
output_file = 'EPG/epg-nos-pt-corrigido.xml.gz'  # Caminho para o arquivo corrigido
corrigir_xml(input_file, output_file)
