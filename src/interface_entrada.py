import os
import platform
import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk, ImageDraw
import subprocess
import sys
import time

try:
    import pygame
except ImportError:
    print("⚠️ Biblioteca Pygame não encontrada. Instale com 'pip install pygame'")
    sys.exit(1)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
FONTE_PERSONALIZADA = os.path.join(ASSETS_DIR, "LondrinaSolid-Regular.ttf")
IMAGEM_FUNDO = os.path.join(ASSETS_DIR, "images", "img_projeto.png")

MUSICA_TEMA = os.path.join(ASSETS_DIR, "01. Stardew Valley Overture (mp3cut.net).mp3")
SOM_HOVER = os.path.join(ASSETS_DIR, "Voicy_List selection.mp3")

APP_TITLE = "Farm Planning Assistant"
COR_TRANSPARENTE = "#abcdef"
BOTAO_TAMANHO = (130, 42)
CORES_BOTAO = {
    "normal": ("#f3b874", "#be8053"),
    "hover": ("#daa363", "#a66f49"),
    "click": ("#b8864f", "#8a5737")
}

EFEITO_HOVER = None


def _hex_to_rgb(hex_color):
    """Converte #RRGGBB para (R, G, B)"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def _rgb_to_hex(rgb_tuple):
    """Converte (R, G, B) para #RRGGBB"""
    return f'#{int(rgb_tuple[0]):02x}{int(rgb_tuple[1]):02x}{int(rgb_tuple[2]):02x}'

def _interpolate_color(start_color, end_color, fraction):
    """Calcula uma cor intermediária entre duas cores hex."""
    start_rgb = _hex_to_rgb(start_color)
    end_rgb = _hex_to_rgb(end_color)

    new_rgb = []
    for i in range(3):
        diff = end_rgb[i] - start_rgb[i]
        new_val = int(start_rgb[i] + (diff * fraction))
        new_rgb.append(new_val)

    return _rgb_to_hex(tuple(new_rgb))

def animate_hover_color(widget, start_color, end_color, duration_ms=150):
    """Anima a cor 'fg' de um widget."""
    if hasattr(widget, "_animation_id"):
        try:
            widget.after_cancel(widget._animation_id)
        except tk.TclError:
            pass

    start_time = time.time()

    def animation_step():
        elapsed_time = (time.time() - start_time) * 1000
        fraction = elapsed_time / duration_ms

        if fraction >= 1.0:
            if widget.winfo_exists():
                widget.config(fg=end_color)
            if hasattr(widget, "_animation_id"):
                delattr(widget, "_animation_id")
            return

        current_color = _interpolate_color(start_color, end_color, fraction)

        try:
            if widget.winfo_exists():
                widget.config(fg=current_color)
                widget._animation_id = widget.after(16, animation_step)
            else:
                if hasattr(widget, "_animation_id"):
                    delattr(widget, "_animation_id")
        except tk.TclError:
            if hasattr(widget, "_animation_id"):
                delattr(widget, "_animation_id")

    animation_step()



def inicializar_audio():
    """Inicializa o mixer do pygame."""
    try:
        pygame.mixer.init()
        print("✅ Pygame Mixer inicializado.")
        return True
    except pygame.error as e:
        print(f"❌ Erro ao inicializar o Pygame Mixer: {e}")
        return False

def carregar_efeito_hover():
    """Carrega o efeito sonoro e armazena na variável global."""
    global EFEITO_HOVER
    if not pygame.mixer.get_init():
        if not inicializar_audio():
            return

    if not os.path.exists(SOM_HOVER):
        print(f"⚠️ Arquivo de efeito sonoro não encontrado: {SOM_HOVER}")
        return

    try:
        EFEITO_HOVER = pygame.mixer.Sound(SOM_HOVER)
        print("✅ Efeito sonoro de hover carregado.")
    except pygame.error as e:
        print(f"❌ Erro ao carregar o efeito sonoro: {e}")
        EFEITO_HOVER = None

def tocar_efeito_hover(volume=0.6):
    """Toca o efeito sonoro se estiver carregado."""
    if EFEITO_HOVER:
        try:
            EFEITO_HOVER.set_volume(volume)
            EFEITO_HOVER.play()
        except pygame.error as e:
            print(f"❌ Erro ao tocar o efeito sonoro: {e}")
            pass

def tocar_musica_loop():
    """Carrega e toca a música em loop."""
    if not os.path.exists(MUSICA_TEMA):
        print(f"⚠️ Arquivo de música não encontrado: {MUSICA_TEMA}")
        return

    if not pygame.mixer.get_init():
        if not inicializar_audio():
            return

    try:
        pygame.mixer.music.load(MUSICA_TEMA)
        pygame.mixer.music.play(-1)
        print(f"🎵 Tocando música: {MUSICA_TEMA}")
    except pygame.error as e:
        print(f"❌ Erro ao carregar ou tocar a música: {e}")

def parar_musica():
    """Para a música e desinicializa o mixer."""
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print("🛑 Música parada.")
    pygame.mixer.quit()


def carregar_fonte(caminho):
    if not os.path.exists(caminho):
        print(f"⚠️ Fonte não encontrada: {caminho}")
        return False

    try:
        if platform.system() == "Windows":
            import ctypes
            if ctypes.windll.gdi32.AddFontResourceW(caminho) > 0:
                print(f"Fonte carregada (Windows): {caminho}")
                return True
        else:
            print("🔹 Carregamento de fonte customizada para sistemas não-Windows implementado no PIL.")
            return True
    except Exception as e:
        print(f"Erro ao carregar fonte: {e}")
    return False


def arredondar_cantos(imagem, raio):
    mascara = Image.new('L', imagem.size, 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0) + imagem.size, raio, fill=255)
    imagem.putalpha(mascara)
    return imagem


def criar_gradiente(w, h, cor1, cor2):
    start = tuple(int(cor1[i:i+2], 16) for i in (1, 3, 5))
    end = tuple(int(cor2[i:i+2], 16) for i in (1, 3, 5))
    img = Image.new("RGB", (w, h))
    for y in range(h):
        cor = tuple(int(start[i] + (end[i] - start[i]) * (y / h)) for i in range(3))
        for x in range(w):
            img.putpixel((x, y), cor)
    return img

def criar_imagem_botao():
    """Cria a imagem de gradiente estática para os botões."""
    w, h = BOTAO_TAMANHO
    img_grad = criar_gradiente(w, h, CORES_BOTAO["normal"][0], CORES_BOTAO["normal"][1])
    return ImageTk.PhotoImage(img_grad)

def iniciar_jogo():
    parar_musica()
    print("✅ Iniciando o aplicativo principal...")
    janela.destroy()
    caminho_script = os.path.join(os.path.dirname(__file__), "interface_sistema.py")
    subprocess.Popen([sys.executable, caminho_script])

def sair_jogo():
    parar_musica()
    print("👋 Saindo do aplicativo...")
    janela.destroy()

def configurar_janela(root, imagem):
    w, h = imagem.width(), imagem.height()
    tela_w, tela_h = root.winfo_screenwidth(), root.winfo_screenheight()
    pos_x, pos_y = (tela_w - w) // 2, (tela_h - h) // 2

    root.title(APP_TITLE)
    root.geometry(f"{w}x{h}+{pos_x}+{pos_y}")
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", COR_TRANSPARENTE)
    root.config(bg=COR_TRANSPARENTE)
    root.resizable(False, False)

def permitir_mover_janela(widget, root):
    def iniciar_mov(e): root._x, root._y = e.x, e.y
    def mover(e): root.geometry(f"+{root.winfo_pointerx() - root._x}+{root.winfo_pointery() - root._y}")
    widget.bind("<Button-1>", iniciar_mov)
    widget.bind("<B1-Motion>", mover)

def criar_botao(root, texto, comando, imagem_tk, pos):
    """Cria um botão baseado em tk.Label, similar ao interface_sistema.py"""

    botao = tk.Label(
        root, text=texto, font=("Londrina Solid", 14),
        image=imagem_tk, compound="center", fg="black",
        bg=COR_TRANSPARENTE,
        borderwidth=0, cursor="hand2"
    )
    botao.image = imagem_tk

    def on_press(event):
        """Esta função agora não precisa mudar a cor."""
        pass

    def on_release(event):
        """Executa o comando ao soltar o clique."""

        x, y = event.x_root, event.y_root
        widget_atual = event.widget.winfo_containing(x, y)
        if widget_atual == botao:
            comando()

    botao.bind("<Enter>", lambda e: (animate_hover_color(e.widget, "#000000", "#FFFFFF", 150),
                                     tocar_efeito_hover(volume=0.6)))
    botao.bind("<Leave>", lambda e: animate_hover_color(e.widget, "#FFFFFF", "#000000", 150))


    botao.bind("<ButtonPress-1>", on_press)
    botao.bind("<ButtonRelease-1>", on_release)

    botao.place(x=pos[0], y=pos[1], width=BOTAO_TAMANHO[0], height=BOTAO_TAMANHO[1])
    return botao


def rodar_interface_entrada():
    global janela

    carregar_fonte(FONTE_PERSONALIZADA)

    janela = tk.Tk()
    janela.start_app = False

    fonte_padrao = tkFont.nametofont("TkDefaultFont")
    fonte_padrao.configure(family="Londrina Solid", size=12)
    janela.option_add("*Font", fonte_padrao)

    try:
        imagem_pil = arredondar_cantos(Image.open(IMAGEM_FUNDO).convert("RGBA"), 24)
        imagem_tk = ImageTk.PhotoImage(imagem_pil)
    except FileNotFoundError:
        print(f"❌ Imagem não encontrada: {IMAGEM_FUNDO}")
        return False

    configurar_janela(janela, imagem_tk)

    bg = tk.Label(janela, image=imagem_tk, bg=COR_TRANSPARENTE)
    bg.place(x=0, y=0, relwidth=1, relheight=1)
    permitir_mover_janela(bg, janela)

    imagem_botao_tk = criar_imagem_botao()

    criar_botao(janela, "Iniciar", iniciar_jogo, imagem_botao_tk, (136, 172))
    criar_botao(janela, "Sair", sair_jogo, imagem_botao_tk, (136, 266))


    if inicializar_audio():
        carregar_efeito_hover()
        tocar_musica_loop()

    janela.mainloop()

    return getattr(janela, 'start_app', False)


if __name__ == "__main__":
    rodar_interface_entrada()