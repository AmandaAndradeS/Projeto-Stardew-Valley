import os
import platform
import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk, ImageDraw
import subprocess
import sys

# ────────────────────────────────────────────────
# Caminhos absolutos
# ────────────────────────────────────────────────
BASE_DIR = r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\assets"
FONTE_PERSONALIZADA = os.path.join(BASE_DIR, "LondrinaSolid-Regular.ttf")
IMAGEM_FUNDO = os.path.join(BASE_DIR, "images", "img_projeto.png")

# ────────────────────────────────────────────────
# Configurações gerais
# ────────────────────────────────────────────────
APP_TITLE = "Farm Planning Assistant"
COR_TRANSPARENTE = "#abcdef"
BOTAO_TAMANHO = (130, 42)
CORES_BOTAO = {
    "normal": ("#f3b874", "#be8053"),
    "hover": ("#daa363", "#a66f49"),
    "click": ("#b8864f", "#8a5737")
}

# ────────────────────────────────────────────────
# Funções auxiliares
# ────────────────────────────────────────────────
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
            print("🔹 Carregamento de fonte customizada para sistemas não-Windows não implementado aqui.")
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


def criar_estados_botao():
    w, h = BOTAO_TAMANHO
    return {
        estado: ImageTk.PhotoImage(criar_gradiente(w, h, *cores))
        for estado, cores in CORES_BOTAO.items()
    }

# ────────────────────────────────────────────────
# Funções dos botões
# ────────────────────────────────────────────────
def iniciar_jogo():
    print("✅ Iniciando o aplicativo principal...")
    janela.destroy()
    caminho_script = os.path.join(os.path.dirname(__file__), "interface_sistema.py")
    subprocess.Popen([sys.executable, caminho_script])


def sair_jogo():
    print("👋 Saindo do aplicativo...")
    janela.destroy()

# ────────────────────────────────────────────────
# Configuração da janela
# ────────────────────────────────────────────────
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


def criar_botao(root, texto, comando, imagens, pos):
    botao = tk.Button(
        root, text=texto, font=("Londrina Solid", 14),
        image=imagens["normal"], compound="center", fg="black",
        relief="flat", borderwidth=0, cursor="hand2", command=comando
    )

    botao.bind("<Enter>", lambda e: botao.config(image=imagens["hover"]))
    botao.bind("<Leave>", lambda e: botao.config(image=imagens["normal"]))
    botao.bind("<ButtonPress-1>", lambda e: botao.config(image=imagens["click"]))
    botao.bind("<ButtonRelease-1>", lambda e: botao.config(image=imagens["hover"]))
    botao.place(x=pos[0], y=pos[1], width=BOTAO_TAMANHO[0], height=BOTAO_TAMANHO[1])
    return botao


# ────────────────────────────────────────────────
# Execução principal
# ────────────────────────────────────────────────
if __name__ == "__main__":
    carregar_fonte(FONTE_PERSONALIZADA)

    janela = tk.Tk()

    fonte_padrao = tkFont.nametofont("TkDefaultFont")
    fonte_padrao.configure(family="Londrina Solid", size=12)
    janela.option_add("*Font", fonte_padrao)

    try:
        imagem_pil = arredondar_cantos(Image.open(IMAGEM_FUNDO).convert("RGBA"), 24)
        imagem_tk = ImageTk.PhotoImage(imagem_pil)
    except FileNotFoundError:
        print(f"❌ Imagem não encontrada: {IMAGEM_FUNDO}")
        exit()

    configurar_janela(janela, imagem_tk)

    bg = tk.Label(janela, image=imagem_tk, bg=COR_TRANSPARENTE)
    bg.place(x=0, y=0, relwidth=1, relheight=1)
    permitir_mover_janela(bg, janela)

    imagens_botao = criar_estados_botao()
    criar_botao(janela, "Iniciar", iniciar_jogo, imagens_botao, (136, 172))
    criar_botao(janela, "Sair", sair_jogo, imagens_botao, (136, 266))

    janela.mainloop()
