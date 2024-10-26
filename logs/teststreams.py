import os
import subprocess
import requests

# Caminho do arquivo de links
file_path = 'channels-link.txt'
# Caminho do arquivo de resultados
result_file = 'stream-test-results.txt'

# Limpar arquivo de resultados
open(result_file, 'w').close()

# Função para testar um stream
def test_stream(stream):
    # Verifica se o link começa com 'http' ou 'https'
    if not stream.startswith(('http://', 'https://')):
        return f"Stream {stream} não está acessível"

    # Verifica a acessibilidade do link com o timeout de 10 segundos
    try:
        response = requests.get(stream, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return f"Stream {stream} não está acessível"

    # Comando VLC para testar o stream
    command = [
        "cvlc", stream, "--intf", "dummy", "--play-and-exit", "--run-time", "5"
    ]

    try:
        # Suprimindo saídas detalhadas do VLC
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Stream {stream} correu bem"
    except subprocess.CalledProcessError:
        return f"Stream {stream} falhou"

# Leitura e teste dos streams
with open(file_path, 'r') as file, open(result_file, 'a') as result:
    for line in file:
        stream = line.strip()
        if stream:  # Verifica se a linha não está vazia
            print(f"Testing stream: {stream}")
            result_message = test_stream(stream)
            print(result_message)
            result.write(result_message + "\n")

print("Testes finalizados. Resultados disponíveis em stream-test-results.txt")
