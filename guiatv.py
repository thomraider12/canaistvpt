import customtkinter as ctk
from PIL import Image
import requests
from io import BytesIO
import re
import gzip
import xml.etree.ElementTree as ET
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Inicializar a aplicação
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CanaisTVPT - Guia de Programação")
app.geometry("800x600")

# Mostrar avisos ao abrir a aplicação
messagebox.showinfo("Atenção:", "Demora a abrir os canais, se acontecer, por favor aguarda.")
messagebox.showinfo("Atenção:", "Precisas sempre de ligação à internet para ver a programação.")

# Frames principais
frame_canais_container = ctk.CTkFrame(app, width=200, corner_radius=0)
frame_canais_container.pack(side="left", fill="y")

# Adicionar barra de rolagem ao frame_canais
canvas_canais = tk.Canvas(frame_canais_container, bg="#2B2B2B", highlightthickness=0)

# Estilizar a barra de rolagem
style = ttk.Style()
style.theme_use("default")
style.configure(
    "Vertical.TScrollbar",
    gripcount=0,
    background="#2B2B2B",  # Cor de fundo
    troughcolor="#2B2B2B",  # Fundo do canal de rolagem
    bordercolor="#2B2B2B",
    arrowcolor="white",  # Cor das setas
    sliderrelief="flat"
)
scrollbar_canais = ttk.Scrollbar(frame_canais_container, orient="vertical", command=canvas_canais.yview, style="Vertical.TScrollbar")
scrollbar_canais.pack(side="right", fill="y", padx=0, pady=0)

scrollable_frame_canais = ctk.CTkFrame(canvas_canais)

scrollable_frame_canais.bind(
    "<Configure>",
    lambda e: canvas_canais.configure(
        scrollregion=canvas_canais.bbox("all")
    )
)

canvas_canais.create_window((0, 0), window=scrollable_frame_canais, anchor="nw")
canvas_canais.configure(yscrollcommand=scrollbar_canais.set)

canvas_canais.pack(side="left", fill="both", expand=True)

# Atualizar frame_canais para usar scrollable_frame_canais
frame_canais = scrollable_frame_canais

frame_guia = ctk.CTkScrollableFrame(app, corner_radius=0)
frame_guia.pack(side="right", fill="both", expand=True)

# Função para carregar logos a partir de URLs
def carregar_logo(url, size=(100, 80)):  # Tamanho ajustado para imagens mais esticadas
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).resize(size, Image.Resampling.LANCZOS)
        return ctk.CTkImage(image, size=size)
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        return None

# Função para extrair dados do ficheiro m3u a partir de uma URL
def extrair_canais(url_m3u):
    canais = []
    try:
        response = requests.get(url_m3u)
        response.raise_for_status()
        linhas = response.text.splitlines()
        for linha in linhas:
            if linha.startswith("#EXTINF"):
                match_logo = re.search(r'tvg-logo="(.*?)"', linha)
                match_nome = re.search(r',(.+)$', linha)
                match_id = re.search(r'tvg-id="(.*?)"', linha)
                if match_logo and match_nome and match_id:
                    canais.append({
                        "nome": match_nome.group(1).strip(),
                        "logo": match_logo.group(1).strip(),
                        "tvg-id": match_id.group(1).strip()
                    })
    except Exception as e:
        print(f"Erro ao obter canais: {e}")
    return canais

# Função para obter a programação do EPG
def obter_programacao_epg(epg_url):
    try:
        response = requests.get(epg_url)
        response.raise_for_status()
        with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
            tree = ET.parse(gz)
            root = tree.getroot()
            return root
    except Exception as e:
        print(f"Erro ao obter EPG: {e}")
        return None

# Função para formatar a data/hora com tratamento de diferentes formatos
def formatar_horario_com_erro(horario):
    try:
        # Tenta o formato completo com fuso horário
        dt = datetime.strptime(horario, "%Y%m%d%H%M%S %z")
        return dt.strftime("%d-%m-%Y %H:%M")
    except Exception:
        try:
            # Tenta o formato sem fuso horário
            dt = datetime.strptime(horario, "%Y%m%d%H%M%S")
            return dt.strftime("%d-%m-%Y %H:%M")
        except Exception as e:
            print(f"Erro ao formatar horário: {e}")
            return "Horário desconhecido"

# Função para mostrar programação no frame_guia
def mostrar_programacao(tvg_id):
    for widget in frame_guia.winfo_children():
        widget.destroy()

    if epg_root is None:
        ctk.CTkLabel(frame_guia, text="Erro: EPG não carregada.").pack()
        return

    programas = epg_root.findall(f".//programme[@channel='{tvg_id}']")
    if not programas:
        ctk.CTkLabel(frame_guia, text=f"Sem programação para o canal: {tvg_id}").pack()
        return

    # Ordenar programas por data de início
    programas = sorted(programas, key=lambda p: p.get("start", "Desconhecido"))

    for programa in programas:
        titulo = programa.find("title").text if programa.find("title") is not None else "Sem título"
        descricao = programa.find("desc").text if programa.find("desc") is not None else "Sem descrição"
        imagem = programa.find("icon").get("src") if programa.find("icon") is not None else None
        inicio = formatar_horario_com_erro(programa.get("start", "Desconhecido"))
        fim = formatar_horario_com_erro(programa.get("stop", "Desconhecido"))

        # Frame do programa
        frame_programa = ctk.CTkFrame(frame_guia, corner_radius=10)
        frame_programa.pack(pady=5, padx=10, fill="x")

        # Imagem do programa
        if imagem:
            try:
                img_data = requests.get(imagem).content
                img = Image.open(BytesIO(img_data)).resize((120, 100), Image.Resampling.LANCZOS)  # Tamanho ajustado
                img_ctk = ctk.CTkImage(img, size=(120, 100))  # Tamanho ajustado
                img_label = ctk.CTkLabel(frame_programa, image=img_ctk, text="")
                img_label.pack(side="left", padx=10)
            except Exception as e:
                print(f"Erro ao carregar imagem do programa: {e}")

        # Informações do programa
        info_frame = ctk.CTkFrame(frame_programa, corner_radius=10)
        info_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(info_frame, text=titulo, font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        ctk.CTkLabel(info_frame, text=f"Início: {inicio} - Fim: {fim}", font=("Arial", 12)).pack(anchor="w", pady=5)
        ctk.CTkLabel(info_frame, text=descricao, font=("Arial", 12), wraplength=400).pack(anchor="w", pady=5)

# URL para o ficheiro m3u
m3u_url = "https://github.com/thomraider12/canaistvpt/raw/main/pt.m3u"
epg_url = "https://github.com/thomraider12/canaistvpt/raw/main/EPG/all.xml.gz"

# Obter lista de canais e EPG
canais = extrair_canais(m3u_url)
epg_root = obter_programacao_epg(epg_url)

for canal in canais:
    logo_image = carregar_logo(canal["logo"], size=(100, 80))  # Tamanho ajustado para os ícones
    if logo_image:
        canal_button = ctk.CTkButton(
            frame_canais,
            image=logo_image,
            text=canal["nome"],
            compound="left",
            command=lambda c=canal["tvg-id"]: mostrar_programacao(c)
        )
        canal_button.pack(pady=5, padx=10, fill="x")

# Executar a aplicação
app.mainloop()