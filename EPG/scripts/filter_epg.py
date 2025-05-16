import gzip
import xml.etree.ElementTree as ET
import os

def extract_epg(input_file, output_file, channels_to_keep):
    # Abre o arquivo EPG compactado e lê o XML
    with gzip.open(input_file, 'rt', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()

        # Encontra todos os canais e programas associados
        channels = root.findall('channel')
        programmes = root.findall('programme')

        # Filtra os canais que não estão na lista
        filtered_channels = [ch for ch in channels if ch.get('id') in channels_to_keep]
        filtered_programmes = [pr for pr in programmes if pr.get('channel') in channels_to_keep]

        # Cria uma nova árvore XML para o EPG filtrado
        new_root = ET.Element('tv')
        for ch in filtered_channels:
            new_root.append(ch)
        for pr in filtered_programmes:
            new_root.append(pr)

        # Salva o XML filtrado temporariamente como um arquivo de texto
        temp_output_file = 'filtered_epg.xml'
        tree = ET.ElementTree(new_root)
        tree.write(temp_output_file, encoding='utf-8', xml_declaration=True)

        # Compacta o arquivo temporário com gzip
        with open(temp_output_file, 'rb') as f_in, gzip.open(output_file, 'wb') as f_out:
            f_out.writelines(f_in)

        # Remove o arquivo temporário
        os.remove(temp_output_file)

# Lista de IDs de canais que você quer manter (modifique conforme necessário)
pluto_channels_to_keep = ['65c69ee3d77d450008c80438', '636adc255bcf470007d6e0e2', '608181d420fc8500075f612a', '5f1213ba0ecebc00070e170f', '5f1ef1a8cec6be00072a7ac9', '5ca671f215a62078d2ec0abf', '66c45afaa72e7b0008a2b153', '55b285cd2665de274553d66f']
samsung_channels_to_keep = ['USBC3900018K6', 'CABB260002016', 'GBBA33000557H', 'CABC52000180Z', 'USAK3508705A', 'INBA4900004W9']
rtp_channels_to_keep = ['rtp-1', 'rtp-2', 'rtp-3', 'rtp-memoria', 'rtp-internacional', 'rtp-madeira', 'rtp-acores', 'rtp-africa']
rakuten_channels_to_keep = ['travelxp-pt', 'bloomberg-tv-new', 'fifa-plus-pt-new', 'red-bull-tv-en', 'jukin-fail-army-new', 'family-rakuten-tv', 'documentaries-rakuten-tv', 'top-movies-rakuten-tv']

extract_epg('epg-pluto-tv.xml.gz', 'filtered-epg-pluto-tv.xml.gz', pluto_channels_to_keep)

extract_epg('epg-samsung-tvplus.xml.gz', 'filtered-epg-samsung-tvplus.xml.gz', samsung_channels_to_keep)

extract_epg('epg-rtp-pt.xml.gz', 'filtered-epg-rtp-pt.xml.gz', rtp_channels_to_keep)

extract_epg('epg-rakuten-tv.xml.gz', 'filtered-epg-rakuten-tv.xml.gz', rakuten_channels_to_keep)

print("Filtragem concluída!")
