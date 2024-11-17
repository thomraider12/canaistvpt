import re

def extract_tvg_ids(m3u_path):
    """
    Extrai todos os `tvg-id` de um arquivo .m3u.
    """
    with open(m3u_path, 'r', encoding='utf-8') as m3u_file:
        m3u_content = m3u_file.read()
    # Usando regex para capturar os tvg-id no formato tvg-id="..."
    tvg_ids = re.findall(r'tvg-id="([^"]+)"', m3u_content)
    return set(tvg_ids)

def read_xmltv_ids(xmltv_ids_path):
    """
    Lê os IDs existentes em xmltv-ids.txt, ignorando a primeira linha.
    """
    with open(xmltv_ids_path, 'r', encoding='utf-8') as file:
        xmltv_ids = file.read().splitlines()[2:]  # Ignora a primeira linha
    return set(xmltv_ids)

def write_validation_result(xmltv_ids_path, all_ids_present, missing_ids, extra_ids):
    """
    Escreve o novo resultado de validação no final do arquivo xmltv-ids.txt.
    """
    with open(xmltv_ids_path, 'a', encoding='utf-8') as file:
        file.write("\n\n")  # Adiciona uma linha em branco para separar a validação
        if all_ids_present:
            file.write("Todos os id's estão presentes na lista pt.m3u.\n")
            if extra_ids:
                file.write(f"Mas alguns ids extras foram encontrados no xmltv-ids.txt: {', '.join(extra_ids)}")
        else:
            file.write("Nem todos os id's estão presentes na lista pt.m3u.\n")
            if missing_ids:
                file.write(f"Faltam os seguintes ids no xmltv-ids.txt: {', '.join(missing_ids)}")

def main():
    m3u_path = 'pt.m3u'  # Caminho para o arquivo m3u na pasta principal
    xmltv_ids_path = 'EPG/xmltv-ids.txt'  # Caminho para o arquivo xmltv-ids.txt

    # Extrair IDs do m3u
    m3u_ids = extract_tvg_ids(m3u_path)
    print(f"Encontrados {len(m3u_ids)} IDs na lista m3u.")

    # Ler IDs do xmltv-ids.txt
    xmltv_ids = read_xmltv_ids(xmltv_ids_path)
    print(f"Encontrados {len(xmltv_ids)} IDs no arquivo xmltv-ids.txt.")

    # Verificar se todos os IDs do m3u estão no xmltv-ids.txt
    missing_ids = m3u_ids - xmltv_ids  # IDs que estão no m3u, mas não no xmltv-ids.txt
    extra_ids = xmltv_ids - m3u_ids    # IDs que estão no xmltv-ids.txt, mas não no m3u

    all_ids_present = not missing_ids

    # Escrever o resultado no xmltv-ids.txt
    write_validation_result(xmltv_ids_path, all_ids_present, missing_ids, extra_ids)
    print("Validação concluída. Resultado escrito no arquivo xmltv-ids.txt.")

if __name__ == "__main__":
    main()
