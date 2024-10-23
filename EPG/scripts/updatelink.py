# Função para extrair links do arquivo .m3u
def extract_links_from_m3u(input_file, output_file):
    # Abre o arquivo de entrada e o arquivo de saída
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        lines = infile.readlines()  # Lê todas as linhas do arquivo de entrada
        for i, line in enumerate(lines):
            if line.startswith('#EXTINF:-1'):  # Verifica se a linha começa com "#EXTINF:-1"
                # Verifica se a próxima linha é um link (começa com http ou https)
                if i + 1 < len(lines) and (lines[i + 1].startswith('http://') or lines[i + 1].startswith('https://')):
                    link = lines[i + 1].strip()  # Remove espaços em branco no início e no fim da linha
                    outfile.write(link + '\n')  # Escreve o link no arquivo de saída

# Especifica os arquivos de entrada e saída
input_file = 'pt.m3u'  # Altere para o nome do seu arquivo .m3u
output_file = 'channels-link.txt'

# Chama a função para extrair e salvar os links
extract_links_from_m3u(input_file, output_file)

print(f"Links extraídos e salvos em {output_file}")
