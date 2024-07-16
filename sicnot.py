import requests

def download_m3u8(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def save_m3u8(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

def replace_content(original_content, new_content):
    # Lógica para substituir o conteúdo do arquivo original pelo novo conteúdo
    return new_content  # Para simplificação, substituindo todo o conteúdo

def main():
    m3u8_url = "https://sicnot.live.impresa.pt/sicnot.m3u8"
    github_m3u8_url = "https://raw.githubusercontent.com/thomraider12/canaistvpt/main/sicnot.m3u8"
    
    # Baixar os conteúdos
    original_content = download_m3u8(m3u8_url)
    new_content = download_m3u8(github_m3u8_url)
    
    # Substituir o conteúdo
    updated_content = replace_content(original_content, new_content)
    
    # Salvar o novo arquivo
    save_m3u8(updated_content, "updated_sicnot.m3u8")

if __name__ == "__main__":
    main()
