import tkinter as tk
from tkinter import ttk, font as tkFont, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageEnhance
import random
import platform
import os
from datetime import datetime

# Importa a função do novo arquivo
from calendario import abrir_calendario_popup, TKCALENDAR_AVAILABLE 


# === Caminhos das pastas ===
CAMINHO_ASSETS = r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\assets"
CAMINHO_IMAGENS = os.path.join(CAMINHO_ASSETS, "images")
CAMINHO_IMAGENS_PERSONAGENS = os.path.join(CAMINHO_IMAGENS, "images personagens")
CAMINHO_FONTE = os.path.join(CAMINHO_ASSETS, "LondrinaSolid-Regular.ttf")


def carregar_fonte(caminho_fonte):
    caminho_absoluto = os.path.abspath(caminho_fonte)
    if not os.path.exists(caminho_absoluto):
        print(f"Erro: Arquivo da fonte não encontrado em '{caminho_absoluto}'")
        return False
    try:
        if platform.system() == "Windows":
            import ctypes
            if ctypes.windll.gdi32.AddFontResourceW(caminho_absoluto) > 0:
                print(f"Fonte '{caminho_fonte}' carregada com sucesso no Windows.")
                return True
            else:
                return False
        else:
            print(f"Fonte '{caminho_fonte}' carregada. (Sistema não-Windows)")
            return True
    except Exception as e:
        print(f"Ocorreu um erro ao carregar a fonte: {e}")
        return False

carregar_fonte(CAMINHO_FONTE)


def arredondar_cantos(imagem_pil, raio):
    mascara = Image.new('L', imagem_pil.size, 0)
    draw = ImageDraw.Draw(mascara)
    draw.rounded_rectangle((0, 0) + imagem_pil.size, raio, fill=255)
    imagem_arredondada = imagem_pil.copy()
    imagem_arredondada.putalpha(mascara)
    return imagem_arredondada


def criar_imagem_gradiente(width, height, color_start_hex, color_end_hex):
    start_r, start_g, start_b = int(color_start_hex[1:3], 16), int(color_start_hex[3:5], 16), int(color_start_hex[5:7], 16)
    end_r, end_g, end_b = int(color_end_hex[1:3], 16), int(color_end_hex[3:5], 16), int(color_end_hex[5:7], 16)
    image = Image.new("RGB", (width, height))
    for y in range(height):
        r = int(start_r + (end_r - start_r) * (y / height))
        g = int(start_g + (end_g - start_g) * (y / height))
        b = int(start_b + (end_b - start_b) * (y / height))
        for x in range(width):
            image.putpixel((x, y), (r, g, b))
    return image


def iniciar_movimento(event):
    janela._x = event.x
    janela._y = event.y
    janela._win_x = janela.winfo_x()
    janela._win_y = janela.winfo_y()


def mover_janela(event):
    deltax = event.x - janela._x
    deltay = event.y - janela._y
    x = janela.winfo_x() + deltax
    y = janela.winfo_y() + deltay
    janela.geometry(f"+{x}+{y}")

    # Atualiza a posição do popup do calendário, se estiver aberto
    if hasattr(janela, 'calendario_popup') and janela.calendario_popup.winfo_exists():
        # Para que o popup continue alinhado ao botão
        cal_x = janela.winfo_x() + botao_calendario.winfo_x()
        cal_y = janela.winfo_y() + botao_calendario.winfo_y() + botao_calendario.winfo_height() + 5
        janela.calendario_popup.geometry(f"+{cal_x}+{cal_y}")


def fechar_janela(event=None):
    janela.quit()
    janela.destroy()


def on_press_gerar(event):
    botao_GerarPlano.config(fg="white")


def on_release_gerar(event=None):
    botao_GerarPlano.config(fg="black")
    mostrar_plano()


def on_press_ajuda(event):
    botao_ajuda.config(image=icone_fruta_pressed_tk)


def on_release_ajuda(event=None):
    botao_ajuda.config(image=icone_fruta_tk)
    mostrar_ajuda_popup()


def verificar_clique(event):
    janela.focus_set()
    area_fechar = (largura_janela - 26, 6, largura_janela - 6, 26)

    if area_fechar[0] <= event.x <= area_fechar[2] and area_fechar[1] <= event.y <= area_fechar[3]:
        fechar_janela()
    else:
        iniciar_movimento(event)


def gerenciar_cursor(event):
    area_fechar = (largura_janela - 26, 6, largura_janela - 6, 26)

    if area_fechar[0] <= event.x <= area_fechar[2] and area_fechar[1] <= event.y <= area_fechar[3]:
        background_label.config(cursor="hand2")
    else:
        background_label.config(cursor="")


def on_focus_in(event):
    if entrada_quantidade.get() == "Digite a quantidade":
        entrada_quantidade.delete(0, "end")
        entrada_quantidade.config(fg='black')
        entrada_quantidade.config(validate='key', validatecommand=vcmd)


def on_focus_out(event):
    if not entrada_quantidade.get():
        entrada_quantidade.config(validate='none')
        entrada_quantidade.config(fg='grey')
        entrada_quantidade.insert(0, "Digite a quantidade")


def validate_input(P):
    if P == "": return True
    if P.isdigit() and len(P) <= 3: return True
    return False


def call_abrir_calendario():
    """Função de 'wrapper' para chamar o calendário do módulo externo."""
    # O widget do botão do calendário é passado para que o calendário possa se posicionar
    # A janela principal (janela) é passada para ser a mãe do popup e para armazenar a data
    abrir_calendario_popup(janela, botao_calendario)


def atualizar_plano_colheita():
    opcao = combobox.get()
    quantidade = entrada_quantidade.get()
    # Pega a data armazenada na janela principal pelo módulo 'calendario.py'
    data = getattr(janela, 'data_selecionada', 'Nenhuma data selecionada')

    if opcao == "Selecione uma opção":
        opcao = "Nenhuma opção selecionada"
    if not quantidade or quantidade == "Digite a quantidade":
        quantidade = "Nenhuma"

    return f"📋 Plano de Colheita\nOpção: {opcao}\nQuantidade: {quantidade}\nData: {data}"


def mostrar_plano():
    texto = atualizar_plano_colheita()
    img = janela.imagem_base_pil.copy()
    draw = ImageDraw.Draw(img)
    draw.text((32, 382), texto, font=fonte_para_desenho, fill="black", spacing=8)
    nova_imagem_tk = ImageTk.PhotoImage(img)
    background_label.config(image=nova_imagem_tk)
    background_label.image = nova_imagem_tk


def mostrar_ajuda_popup():
    if hasattr(janela, 'ajuda_popup') and janela.ajuda_popup.winfo_exists():
        janela.ajuda_popup.destroy()
        return

    ajuda_popup = tk.Toplevel(janela)
    janela.ajuda_popup = ajuda_popup
    ajuda_popup.overrideredirect(True)
    ajuda_popup.attributes('-topmost', True)
    ajuda_popup.config(bg="#f3b874", highlightbackground="#be8053", highlightthickness=2)

    janela.update_idletasks()
    pos_x = janela.winfo_x() + botao_ajuda.winfo_x() + botao_ajuda.winfo_width() + 5
    pos_y = janela.winfo_y() + botao_ajuda.winfo_y() - 30
    ajuda_popup.geometry(f"+{pos_x}+{pos_y}")

    texto_ajuda = """
    CAMPO PARA ADICIONAR O TEXTO
    """

    label_ajuda = tk.Label(ajuda_popup,
                            text=texto_ajuda,
                            font=("Londrina Solid", 11),
                            bg="#f3b874",
                            justify=tk.LEFT,
                            wraplength=280,
                            padx=10, pady=10)
    label_ajuda.pack()

    ajuda_popup.bind("<FocusOut>", lambda e: ajuda_popup.destroy())
    ajuda_popup.focus_set()


# === Janela principal ===
janela = tk.Tk()
janela.title("Farm Planning Assistant")
# Inicializa o atributo que será usado para armazenar a data
janela.data_selecionada = "Nenhuma data selecionada"

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="Londrina Solid", size=12)
janela.option_add("*Font", default_font)
janela.overrideredirect(True)
janela.attributes('-topmost', True)
janela.option_add('*TCombobox*Listbox.selectBackground', '#be8053')
janela.option_add('*TCombobox*Listbox.selectForeground', 'white')
janela.option_add('*TCombobox*Listbox.background', '#f3b874')
janela.option_add('*TCombobox*Listbox.foreground', 'black')

# === Imagens ===
try:
    imagem_pil_original = Image.open(os.path.join(CAMINHO_IMAGENS, "img_tela_2.png")).convert("RGBA")

    # === 🔁 RANDOMIZAÇÃO DE PERSONAGEM ===
    try:
        lista_imagens_personagens = [
            os.path.join(CAMINHO_IMAGENS_PERSONAGENS, arquivo)
            for arquivo in os.listdir(CAMINHO_IMAGENS_PERSONAGENS)
            if arquivo.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        if lista_imagens_personagens:
            imagem_escolhida = random.choice(lista_imagens_personagens)
            imagem_personagem_pil = Image.open(imagem_escolhida).convert("RGBA")
            imagem_personagem_pil = imagem_personagem_pil.resize((125, 125), Image.Resampling.LANCZOS)
            imagem_pil_original.paste(imagem_personagem_pil, (194, 216), imagem_personagem_pil)
        else:
            print("⚠️ Nenhuma imagem encontrada em 'images personagens'.")

    except Exception as e:
        print(f"⚠️ Erro ao carregar personagem: {e}")

    imagem_pil_arredondada = arredondar_cantos(imagem_pil_original, 24)
    janela.imagem_base_pil = imagem_pil_arredondada.copy()
    imagem_tk = ImageTk.PhotoImage(janela.imagem_base_pil)

except FileNotFoundError:
    messagebox.showerror("Erro", "Imagem base não encontrada.")
    janela.destroy()
    exit()

# === Fonte para desenhar ===
try:
    fonte_para_desenho = ImageFont.truetype(CAMINHO_FONTE, 20)
except IOError:
    fonte_para_desenho = ImageFont.load_default()

# === Ícone ===
try:
    icone_fruta_pil = Image.open(os.path.join(CAMINHO_IMAGENS, "fruta_icone.png")).convert("RGBA")
    icone_fruta_pil = icone_fruta_pil.resize((28, 28), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Brightness(icone_fruta_pil)
    icone_fruta_pressed_pil = enhancer.enhance(0.7)
    icone_fruta_tk = ImageTk.PhotoImage(icone_fruta_pil)
    icone_fruta_pressed_tk = ImageTk.PhotoImage(icone_fruta_pressed_pil)
    icone_disponivel = True
except FileNotFoundError:
    messagebox.showerror("Erro de Imagem", "O arquivo 'fruta_icone.png' não foi encontrado.")
    icone_disponivel = False


# === Configuração da janela ===
largura_janela, altura_janela = imagem_tk.width(), imagem_tk.height()
pos_x = (janela.winfo_screenwidth() // 2) - (largura_janela // 2)
pos_y = (janela.winfo_screenheight() // 2) - (altura_janela // 2)
janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
janela.config(bg="#abcdef")
janela.attributes("-transparentcolor", "#abcdef")

background_label = tk.Label(janela, image=imagem_tk, bg="#abcdef", borderwidth=0)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = imagem_tk

vcmd = (janela.register(validate_input), '%P')

combobox = ttk.Combobox(janela, values=["Aspersor - Nível 2", "Área Plantável"], state="readonly")
combobox.set("Selecione uma opção")
combobox.place(x=21, y=107, width=168, height=28)

janela.option_add('*TCombobox*Listbox.cursor', 'hand2')

combobox.bind('<Enter>', lambda event: janela.config(cursor='hand2'))
combobox.bind('<Leave>', lambda event: janela.config(cursor=''))

entrada_quantidade = tk.Entry(janela, borderwidth=0, bg="#f3b874", fg='grey')
entrada_quantidade.insert(0, "Digite a quantidade")
entrada_quantidade.bind('<FocusIn>', on_focus_in)
entrada_quantidade.bind('<FocusOut>', on_focus_out)
entrada_quantidade.place(x=21, y=147, width=168, height=32)

# O botão agora chama a função 'wrapper'
botao_calendario = tk.Label(janela, text="📅", font=("Arial", 16), bg="#f3b874", cursor="hand2")
botao_calendario.place(x=218, y=108, width=27, height=27)
# Note que passamos call_abrir_calendario, que por sua vez chama a função do módulo externo
botao_calendario.bind("<Button-1>", lambda e: call_abrir_calendario()) 

largura_botao, altura_botao = 167, 42
img_grad = criar_imagem_gradiente(largura_botao, altura_botao, "#f3b874", "#be8053")
img_grad_tk = ImageTk.PhotoImage(img_grad)

botao_GerarPlano = tk.Label(janela, text="Gerar Plano", font=("Londrina Solid", 14),
                             image=img_grad_tk, compound="center", fg="black",
                             bg="#abcdef", borderwidth=0, cursor="hand2")
botao_GerarPlano.image = img_grad_tk
botao_GerarPlano.place(x=21, y=207, width=largura_botao, height=altura_botao)
botao_GerarPlano.bind("<ButtonPress-1>", on_press_gerar)
botao_GerarPlano.bind("<ButtonRelease-1>", on_release_gerar)

if icone_disponivel:
    botao_ajuda = tk.Label(janela, image=icone_fruta_tk, borderwidth=0, cursor="hand2")
    botao_ajuda.config(bg="#e4a96a")
    botao_ajuda.image = icone_fruta_tk
    botao_ajuda.place(x=25, y=305)
    botao_ajuda.bind("<ButtonPress-1>", on_press_ajuda)
    botao_ajuda.bind("<ButtonRelease-1>", on_release_ajuda)

background_label.bind("<Button-1>", verificar_clique)
background_label.bind("<B1-Motion>", mover_janela)
background_label.bind("<Motion>", gerenciar_cursor)

janela.mainloop()