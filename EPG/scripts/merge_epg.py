import os
import gzip
import xml.etree.ElementTree as ET

ignorar = ['epg-rtp-pt.xml.gz', 'epg-meo-pt.xml.gz']

def merge_epgs(epg_dir, output_file):
    # Criar elemento raiz para o XML combinado
    combined_root = None

    # Procurar todos os arquivos .xml.gz na pasta
    for file_name in os.listdir(epg_dir):
        # Ignorar o arquivo problemático
        if file_name in ignorar:
            print(f"Ignorando o arquivo problemático: {file_name}")
            continue
        
        if file_name.endswith('.xml.gz'):
            print(file_name)
            file_path = os.path.join(epg_dir, file_name)
            try:
                with gzip.open(file_path, 'rt', encoding='utf-8') as file:
                    # Ler o conteúdo XML do arquivo
                    tree = ET.parse(file)
                    root = tree.getroot()

                    # Se ainda não inicializou o root do combinado, faz isso agora
                    if combined_root is None:
                        combined_root = root
                    else:
                        # Adicionar cada elemento do arquivo atual ao XML combinado
                        for element in root:
                            combined_root.append(element)
            except ET.ParseError as e:
                print(f"Erro ao processar {file_name}: {e}")
                continue

    # Verificar se a raiz combinada foi criada
    if combined_root is None:
        print("Nenhum arquivo XML válido foi encontrado.")
        return

    # Escrever o XML combinado em um arquivo .xml.gz
    with gzip.open(output_file, 'wt', encoding='utf-8') as output:
        # Criar a árvore XML combinada e salvar
        combined_tree = ET.ElementTree(combined_root)
        combined_tree.write(output, encoding='unicode')
    
    print(f"Merge completo. Arquivo salvo como {output_file}")

# Usar o script
epg_dir = 'EPG'  # Diretório onde estão os arquivos
output_file = 'EPG/all.xml.gz'  # Nome do arquivo final combinado
merge_epgs(epg_dir, output_file)
