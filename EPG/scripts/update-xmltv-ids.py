import gzip
import xml.etree.ElementTree as ET

# Função para extrair os IDs dos canais do arquivo XML
def extrair_ids_canais(xml_gz_file):
    canais = []
    
    with gzip.open(xml_gz_file, 'rt', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        
        # Procura por todos os elementos com id (ajuste conforme a estrutura real do XML)
        for elem in root.findall(".//channel"):
            id_canal = elem.get("id")
            if id_canal:
                canais.append(id_canal)
    
    return canais

# Função para gravar os canais em um arquivo de texto
def gravar_em_arquivo(canais, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Canais em XMLTV disponíveis no all.xml.gz:" + "\n\n")
        for canal in canais:
            # Formata o nome do canal no formato desejado
            canal_formatado = f"{canal}"
            f.write(canal_formatado + "\n")

# Caminho do arquivo XML comprimido
xml_gz_file = 'all.xml.gz'

# Caminho do arquivo de saída
output_file = 'xmltv-ids.txt'

# Extrair os IDs dos canais
canais = extrair_ids_canais(xml_gz_file)

# Gravar os canais no arquivo de texto
gravar_em_arquivo(canais, output_file)

print(f"Os canais foram gravados em {output_file}")