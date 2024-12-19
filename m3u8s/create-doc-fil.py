# Script para criar entradas de canais em formato .txt

def criar_entrada_txt():
    # Nome do ficheiro para salvar as entradas
    nome_ficheiro = "m3u8s/fildoc.txt"

    while True:
        print("\nInsira os dados para criar uma nova entrada:")
        nome = input("Nome do canal: ")
        descricao = input("Descrição do canal: ")
        stream = input("URL do stream: ")
        tvg_logo = input("URL do logotipo (tvg-logo): ")

        # Formatar a entrada no padrão solicitado
        entrada = (
            f"#EXTINF:-1 media=\"true\" tvg-logo=\"{tvg_logo}\", {nome}\n"
            f"#EXTDESC: {descricao}\n"
            f"{stream}\n\n"
        )

        # Escrever a entrada no ficheiro
        with open(nome_ficheiro, "a", encoding="utf-8") as ficheiro:
            ficheiro.write(entrada)

        print(f"Entrada adicionada ao ficheiro '{nome_ficheiro}':\n{entrada}")

        # Perguntar se deseja adicionar outra entrada
        continuar = input("Deseja adicionar outra entrada? (s/n): ").strip().lower()
        if continuar != 's':
            print("\nFinalizando o script. Todas as entradas foram salvas.")
            break

if __name__ == "__main__":
    criar_entrada_txt()
