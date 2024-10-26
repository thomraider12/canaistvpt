import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timedelta
import gzip

def convert_jsontv_to_xmltv(json_path, xml_output_path):
    # Carregar JSONTV e verificar a estrutura
    with open(json_path, "r", encoding="utf-8") as file:
        jsontv_data = json.load(file)
    
    # Elemento raiz do XMLTV
    tv_element = ET.Element("tv")

    # Iterar pelos canais no JSONTV
    for channel_key, channel_info in jsontv_data.items():
        # Criar o elemento <channel> e adicionar detalhes
        channel_element = ET.SubElement(tv_element, "channel", id=channel_key)
        display_name = ET.SubElement(channel_element, "display-name")
        display_name.text = channel_info.get("_info", {}).get("name", channel_key)
        
        icon_url = channel_info.get("_info", {}).get("logoUrl", "")
        if icon_url:
            ET.SubElement(channel_element, "icon", src=icon_url)

        # Seções de programação
        sections = ["primetime", "morning", "afternoon", "evening"]

        # Iterar sobre cada seção para adicionar programas
        for section in sections:
            programmes = channel_info.get(section, [])
            for i, programme in enumerate(programmes):
                start_time = datetime.strptime(programme["date"], "%Y-%m-%d %H:%M:%S")
                start_formatted = start_time.strftime("%Y%m%d%H%M%S")

                # Calcular o horário de fim (se possível) ou definir uma duração padrão
                if i + 1 < len(programmes):
                    end_time = datetime.strptime(programmes[i + 1]["date"], "%Y-%m-%d %H:%M:%S")
                    stop_time = end_time  # Usa o início do próximo programa como horário de término
                else:
                    stop_time = start_time + timedelta(minutes=30)  # Duração padrão de 30 minutos

                # Garantir que o stop não seja no dia seguinte, a menos que seja intencional
                # Se o stop_time é antes do start_time ou é muito longe, corrigir
                if stop_time <= start_time or stop_time - start_time > timedelta(hours=24):
                    stop_time = start_time + timedelta(minutes=30)  # Recalcular se o stop é anterior ao start

                stop_formatted = stop_time.strftime("%Y%m%d%H%M%S")

                # Criar o elemento <programme>
                programme_element = ET.SubElement(tv_element, "programme", 
                                                  start=start_formatted,
                                                  stop=stop_formatted,
                                                  channel=channel_key)

                # Adicionar título e descrição
                title = ET.SubElement(programme_element, "title")
                title.text = programme["name"]

                desc = ET.SubElement(programme_element, "desc")
                desc.text = programme["description"]

                # Adicionar URL e imagens, se disponíveis
                url = ET.SubElement(programme_element, "url")
                url.text = programme.get("url", "")

                if "image" in programme:
                    for img in programme["image"]:
                        ET.SubElement(programme_element, "icon", src=img["src"])

    # Salvar o XMLTV em arquivo
    xml_content = ET.tostring(tv_element, encoding='utf-8', xml_declaration=True).decode('utf-8')

    # Melhorar a formatação para visualização (indentação e novas linhas)
    pretty_xml = minidom.parseString(xml_content).toprettyxml(indent="  ")

    # Salvar o arquivo comprimido em GZIP
    with gzip.open(xml_output_path, 'wt', encoding='utf-8') as gz_file:
        gz_file.write(pretty_xml)

# Exemplo de uso
try:
    convert_jsontv_to_xmltv("epg-rtp-pt.json", "epg-rtp-pt.xml.gz")  # Altere o nome do arquivo para .gz
    print("Conversão concluída com sucesso.")
except KeyError as e:
    print(f"Erro: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
