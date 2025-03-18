import customtkinter as ctk
import vlc
import tkinter as tk
import requests
import re
from io import StringIO
from PIL import Image
from urllib.request import urlopen

M3U_URL = "https://raw.githubusercontent.com/thomraider12/canaistvpt/refs/heads/main/pt.m3u"

class TVPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Player TV")
        self.geometry("800x600")
        
        # Criar um contenedor principal
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)
        
        # Criar um frame para o player
        self.video_frame = ctk.CTkFrame(self.main_container, width=800, height=400)
        self.video_frame.pack(pady=10, fill="both", expand=True)
        
        # Criar uma instância do VLC
        try:
            print("A inicializar VLC...")
            self.instance = vlc.Instance()
            self.player = self.instance.media_player_new()
            print("VLC inicializado com sucesso.")
        except Exception as e:
            print(f"Erro ao inicializar o VLC: {e}")
        
        # Criar um contenedor para os canais
        self.channels_container = ctk.CTkFrame(self.main_container)
        self.channels_container.pack(fill="both", expand=True)
        
        # Criar um canvas e uma barra de rolagem para os canais
        self.canvas = tk.Canvas(self.channels_container)
        self.scrollbar = tk.Scrollbar(self.channels_container, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(fill="both", expand=True)
        
        # Carregar canais
        print("A carregar canais...")
        self.channels = self.load_channels()
        if self.channels:
            print(f"{len(self.channels)} canais carregados.")
        else:
            print("Nenhum canal encontrado.")
        
        self.create_channel_buttons()
        
        # Contenedor para botões de controle
        self.controls_container = ctk.CTkFrame(self.main_container)
        self.controls_container.pack(pady=10, fill="x")
        
        # Adicionar botão de full screen
        self.fullscreen_button = ctk.CTkButton(self.controls_container, text="Full Screen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(pady=10)
        
        # Criar um frame para o botão de exit fullscreen (inicialmente oculto)
        self.fullscreen_exit_container = ctk.CTkFrame(self)
        self.exit_fullscreen_button = ctk.CTkButton(self.fullscreen_exit_container, text="Exit Full Screen", command=self.toggle_fullscreen)
        self.exit_fullscreen_button.pack(side="bottom", pady=10)
        
        self.is_fullscreen = False
        
        # Associar a tecla Escape para sair do modo fullscreen
        self.bind("<Escape>", lambda e: self.toggle_fullscreen() if self.is_fullscreen else None)
    
    def load_channels(self):
        try:
            print(f"A fazer a requisição para {M3U_URL}...")
            response = requests.get(M3U_URL)
            if response.status_code != 200:
                print(f"Erro ao carregar a lista de canais: Código de status {response.status_code}.")
                return []
            
            channels = []
            data = response.text
            
            # Alteração da expressão regular
            print("A processar os dados M3U...")
            entries = re.findall(r'#EXTINF:-1.*?tvg-logo="(.*?)".*?,(.*?)\n(.*?)\n', data)
            
            # Exibir canais e URLs para depuração
            for logo, name, url in entries:
                print(f"Canal: {name}, URL: {url}")  # Depuração: Exibe nome e URL do canal
                
                # Limpar qualquer espaço extra ou caracteres indesejados no URL
                url = url.strip()  # Remover espaços à frente e atrás
                channels.append({"name": name, "url": url, "logo": logo})
            
            return channels
        except Exception as e:
            print(f"Erro ao carregar ou processar os canais: {e}")
            return []
    
    def create_channel_buttons(self):
        print("A criar botões dos canais...")
        for channel in self.channels:
            try:
                print(f"A carregar logo para o canal {channel['name']}...")
                img = Image.open(urlopen(channel["logo"])).resize((50, 50))
                # Usar CTkImage em vez de PhotoImage
                img = ctk.CTkImage(light_image=img, dark_image=img)  # Para temas claros e escuros
                btn = ctk.CTkButton(self.scrollable_frame, image=img, text=channel["name"], command=lambda url=channel["url"]: self.play(url))
                btn.image = img  # Manter referência
                btn.pack(side="left", padx=5, pady=5)  # Organizar na horizontal
                print(f"Botão para o canal {channel['name']} criado com sucesso.")
            except Exception as e:
                print(f"Erro ao carregar o logo ou criar o botão para o canal {channel['name']}: {e}")
    
    def play(self, url):
        if url:
            try:
                print(f"A abrir a stream para a URL: {url}")
                media = self.instance.media_new(url)
                self.player.set_media(media)
                
                # Usa o ID do frame correto dependendo do modo
                if self.is_fullscreen:
                    self.player.set_hwnd(self.video_frame.winfo_id())
                else:
                    self.player.set_hwnd(self.video_frame.winfo_id())
                
                self.player.play()
                print("Stream aberta e reprodução iniciada.")
            except Exception as e:
                print(f"Erro ao tentar reproduzir o vídeo: {e}")
    
    def toggle_fullscreen(self):
        if self.is_fullscreen:
            # Voltar ao tamanho original
            self.attributes("-fullscreen", False)
            self.geometry("800x600")
            
            # Ocultar o contenedor de saída de fullscreen
            self.fullscreen_exit_container.pack_forget()
            
            # Mostrar o contenedor principal
            self.main_container.pack(fill="both", expand=True)
            
            self.is_fullscreen = False
        else:
            # Ajustar o player para ocupar toda a tela
            self.attributes("-fullscreen", True)
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
            
            # Ocultar o contenedor principal
            self.main_container.pack_forget()
            
            # Mostrar apenas o video_frame e o botão de sair
            self.video_frame.pack_forget()
            self.video_frame = ctk.CTkFrame(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
            self.video_frame.pack(fill="both", expand=True)
            
            # Mostrar o botão de sair do fullscreen
            self.fullscreen_exit_container.pack(side="bottom", fill="x")
            
            # Atualizar o VLC para o novo frame
            if self.player.get_media():
                self.player.set_hwnd(self.video_frame.winfo_id())
                
            self.is_fullscreen = True

if __name__ == "__main__":
    try:
        print("A iniciar a aplicação...")
        app = TVPlayer()
        app.mainloop()
        print("Aplicação iniciada com sucesso.")
    except Exception as e:
        print(f"Erro ao iniciar o programa: {e}")