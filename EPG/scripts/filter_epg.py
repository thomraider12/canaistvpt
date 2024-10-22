import gzip
import xml.etree.ElementTree as ET

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

        # Escreve o XML filtrado no arquivo de saída
        tree = ET.ElementTree(new_root)
        with gzip.open(output_file, 'wt', encoding='utf-8') as f_out:
            tree.write(f_out, encoding='utf-8', xml_declaration=True)

# Lista de IDs de canais que você quer manter (modifique conforme necessário)
pluto_channels_to_keep = ['formula-1-channel', 'top-gear-ptv1']
samsung_channels_to_keep = ['USBC3900018K6', 'GBBA3300024F7', 'CABC52000180Z', 'CABB260002016']

# Processa a EPG do PlutoTV
extract_epg('epg-pluto-tv.xml.gz', 'filtered-epg-pluto-tv.xml.gz', pluto_channels_to_keep)

# Processa a EPG da SamsungTVPlus
extract_epg('epg-samsung-tvplus.xml.gz', 'filtered-epg-samsung-tvplus.xml.gz', samsung_channels_to_keep)

print("Filtragem concluída!")
