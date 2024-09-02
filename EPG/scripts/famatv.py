import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Criação do elemento raiz <tv>
root = ET.Element('tv')

# Adiciona o canal FamaTV
channel = ET.SubElement(root, 'channel', id="FamaTV.pt")
display_name = ET.SubElement(channel, 'display-name')
display_name.text = "FamaTV"

# Obtém a hora atual e ajusta para a próxima hora cheia (minutos = 0)
current_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

# Define a programação de hora em hora para os próximos 7 dias
for i in range(168):
    start_time = current_time + timedelta(hours=i)
    end_time = start_time + timedelta(hours=1)

    # Formata as datas no formato XMLTV (YYYYMMDDHHMMSS + timezone)
    start_str = start_time.strftime('%Y%m%d%H%M%S +0000')
    end_str = end_time.strftime('%Y%m%d%H%M%S +0000')

    # Cria o elemento <programme>
    programme = ET.SubElement(root, 'programme', start=start_str, stop=end_str, channel="FamaTV.pt")
    
    # Adiciona o título do programa
    title = ET.SubElement(programme, 'title', lang="pt")
    title.text = "FamaTV - Direto"

    # Adiciona a descrição do programa
    description = ET.SubElement(programme, 'desc', lang="pt")
    description.text = "As notícias mais recentes de Famalicão e de Portugal no canal Fama TV."

    # Adiciona o ícone do programa
    icon = ET.SubElement(programme, 'icon', src="https://ae-minho.pt/assets/img/noticias/115.jpg")

# Salva o arquivo XML no diretório raiz do projeto
try:
    tree = ET.ElementTree(root)
    tree.write('epg-fama-pt.xml', encoding='utf-8', xml_declaration=True)
    sucesso = True
except Exception as e:
    print(f"Erro ao escrever o ficheiro: {e}")
    sucesso = False
if sucesso:
    print("Ficheiro escrito com sucesso.")
else:
 print("Erro desconhecido!?")
