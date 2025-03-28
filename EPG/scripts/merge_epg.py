import os
import gzip
import xml.etree.ElementTree as ET

ignorar = ['epg-meo-pt.xml.gz', 'epg-test-pt.xml.gz']

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
            file_path = os.path.join(epg_dir, file_name)
            try:
                with gzip.open(file_path, 'rt', encoding='utf-8') as file:
                    # Ler o conteúdo XML do arquivo
                    tree = ET.parse(file)
                    root = tree.getroot()

                    # Exibir mensagem de processamento do arquivo
                    print(f'Processando "{file_name}":')

                    # Inicializar o root do combinado, se necessário
                    if combined_root is None:
                        combined_root = root
                    else:
                        # Adicionar cada elemento ao combinado e mostrar a mensagem
                        for element in root:
                            combined_root.append(element)

                            # Identificar o tipo de elemento e mostrar a mensagem
                            if element.tag == 'channel':
                                canal_id = element.get('id')
                                print(f"Juntando a tudo, o canal {canal_id}")
                            elif element.tag == 'programme':
                                canal_ref = element.get('channel')
                                print(f"Juntando a tudo, a programação do canal {canal_ref}")
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