import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Criação do elemento raiz <tv>
root = ET.Element('tv')

# Adiciona o canal FamaTV
channel = ET.SubElement(root, 'channel', id="FamaTV.pt")
display_name = ET.SubElement(channel, 'display-name')
display_name.text = "FamaTV"

# Obtém a hora atual
current_time = datetime.utcnow()
# Define a programação de hora em hora para as próximas 24 horas
for i in range(24):
    start_time = current_time + timedelta(hours=i)
    end_time = start_time + timedelta(hours=1)

    # Formata as datas no formato XMLTV (YYYYMMDDHHMMSS + timezone)
    start_str = start_time.strftime('%Y%m%d%H%M%S +0000')
    end_str = end_time.strftime('%Y%m%d%H%M%S +0000')

    # Cria o elemento <programme>
    programme = ET.SubElement(root, 'programme', start=start_str, stop=end_str, channel="FamaTV.pt")
    
    # Adiciona o título do programa
    title = ET.SubElement(programme, 'title', lang="pt")
    title.text = "FamaTV"

# Cria a árvore XML e salva o arquivo
tree = ET.ElementTree(root)
tree.write('EPG/epg-fama-pt.xml', encoding='utf-8', xml_declaration=True)
