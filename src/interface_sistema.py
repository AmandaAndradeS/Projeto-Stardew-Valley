import tkinter as tk
from tkinter import ttk, font as tkFont, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageEnhance
import random
import platform
import os
import traceback
import sys
import time

try:
    import pygame
except ImportError:
    print("⚠️ Biblioteca Pygame não encontrada. Instale com 'pip install pygame'")
    PYGAME_AVAILABLE = False
else:
    PYGAME_AVAILABLE = True


from calendario import abrir_calendario_popup, TKCALENDAR_AVAILABLE
from tratamento_dados import tratar_e_processar_dados

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

CAMINHO_ASSETS = os.path.join(PROJECT_ROOT, "assets")
CAMINHO_IMAGENS = os.path.join(CAMINHO_ASSETS, "images")
CAMINHO_IMAGENS_PERSONAGENS = os.path.join(CAMINHO_IMAGENS, "images personagens")
CAMINHO_FONTE = os.path.join(CAMINHO_ASSETS, "LondrinaSolid-Regular.ttf")

MUSICA_TEMA_SISTEMA = os.path.join(CAMINHO_ASSETS, "11. Distant Banjo (mp3cut.net).mp3")

CAMINHO_SOM_HOVER = os.path.join(CAMINHO_ASSETS, "Voicy_List selection.mp3")
SOM_HOVER = None

FONT_NAME_PDF = 'LondrinaSolid'
if REPORTLAB_AVAILABLE:
    try:
        if os.path.exists(CAMINHO_FONTE):
            pdfmetrics.registerFont(TTFont(FONT_NAME_PDF, CAMINHO_FONTE))
            print(f"✅ Fonte '{FONT_NAME_PDF}' registrada com sucesso no ReportLab.")
        else:
            raise FileNotFoundError("Arquivo da fonte não encontrado.")
    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível registrar a fonte '{FONT_NAME_PDF}' para o PDF. Usando 'Helvetica'. Erro: {e}")
        FONT_NAME_PDF = 'Helvetica'
else:
    FONT_NAME_PDF = 'Helvetica'


def _hex_to_rgb(hex_color):

    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def _rgb_to_hex(rgb_tuple):

    return f'#{int(rgb_tuple[0]):02x}{int(rgb_tuple[1]):02x}{int(rgb_tuple[2]):02x}'

def _interpolate_color(start_color, end_color, fraction):

    start_rgb = _hex_to_rgb(start_color)
    end_rgb = _hex_to_rgb(end_color)

    new_rgb = []
    for i in range(3):
        diff = end_rgb[i] - start_rgb[i]
        new_val = int(start_rgb[i] + (diff * fraction))
        new_rgb.append(new_val)

    return _rgb_to_hex(tuple(new_rgb))

def animate_hover_color(widget, start_color, end_color, duration_ms=150):

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

    global PYGAME_AVAILABLE, SOM_HOVER

    if not PYGAME_AVAILABLE:
        return False

    try:
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        print("✅ Pygame Mixer inicializado.")

        if pygame.mixer.get_init():
            if os.path.exists(CAMINHO_SOM_HOVER):
                try:
                    SOM_HOVER = pygame.mixer.Sound(CAMINHO_SOM_HOVER)
                    SOM_HOVER.set_volume(0.3)
                    print("✅ Som de hover carregado.")
                except pygame.error as e:
                    print(f"❌ Erro ao carregar o som de hover: {e}. Verifique o formato.")
            else:
                print(f"⚠️ Arquivo de som de hover não encontrado: {CAMINHO_SOM_HOVER}")

        return True
    except pygame.error as e:
        print(f"❌ Erro ao inicializar o Pygame Mixer: {e}")
        return False

def tocar_musica():

    if PYGAME_AVAILABLE and os.path.exists(MUSICA_TEMA_SISTEMA):
        try:
            pygame.mixer.music.load(MUSICA_TEMA_SISTEMA)
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            print("▶️ Música tema tocando.")
        except pygame.error as e:
            print(f"❌ Erro ao tocar música: {e}")

def parar_musica():

    if PYGAME_AVAILABLE:
        pygame.mixer.music.stop()

def tocar_som_hover(event):

    global SOM_HOVER
    if PYGAME_AVAILABLE and SOM_HOVER:
        SOM_HOVER.play()

def adicionar_som_hover(widget):

    if PYGAME_AVAILABLE and SOM_HOVER:
        widget.bind("<Enter>", tocar_som_hover, add=True)


def carregar_fonte(caminho_fonte):
    caminho_absoluto = os.path.abspath(caminho_fonte)
    if not os.path.exists(caminho_absoluto):
        print(f"Erro: Arquivo da fonte não encontrado em '{caminho_absoluto}'")
        return False
    try:
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

    if hasattr(janela, 'calendario_popup') and janela.calendario_popup.winfo_exists():
        cal_x = janela.winfo_x() + botao_calendario.winfo_x() - (janela.calendario_popup.winfo_width() // 2) + (botao_calendario.winfo_width() // 2)
        cal_y = janela.winfo_y() + botao_calendario.winfo_y() + botao_calendario.winfo_height() + 5
        janela.calendario_popup.geometry(f"+{cal_x}+{cal_y}")

def fechar_janela(event=None):
    parar_musica()
    janela.quit()
    janela.destroy()


def on_press_gerar(event):
    pass

def on_release_gerar(event=None):

    if event:
        x, y = event.x_root, event.y_root
        widget_atual = event.widget.winfo_containing(x, y)
        if widget_atual == botao_GerarPlano:
            mostrar_plano()
    else:
        mostrar_plano()

def resetar_plano(event=None):

    try:
        texto_plano.config(state="normal")
        texto_plano.delete(1.0, "end")
        texto_plano.config(state="disabled")

        scrollbar.pack_forget()
        texto_plano.pack_forget()
        texto_plano.pack(side="left", fill="both", expand=True)

        combobox.set("Selecione uma opção")

        entrada_quantidade.config(validate='none')
        entrada_quantidade.delete(0, "end")
        entrada_quantidade.insert(0, "Digite a quantidade")
        entrada_quantidade.config(fg='grey')
        janela.focus_set()

        janela.data_selecionada = "Nenhuma data selecionada"
        if hasattr(janela, "intervalo_selecionado"):
            janela.intervalo_selecionado = {"inicio": None, "fim": None}

        if hasattr(janela, 'calendario_popup') and janela.calendario_popup.winfo_exists():
            janela.calendario_popup.destroy()

    except Exception as e:
        print(f"Erro ao resetar: {e}")

def on_press_reset(event):
    pass

def on_release_reset(event=None):

    if event:
        x, y = event.x_root, event.y_root
        widget_atual = event.widget.winfo_containing(x, y)
        if widget_atual == botao_Resetar:
            resetar_plano()
    else:
        resetar_plano()

def on_press_ajuda(event):
    try:
        botao_ajuda.config(image=icone_fruta_pressed_tk)
    except NameError:
        pass

def on_release_ajuda(event=None):
    try:
        botao_ajuda.config(image=icone_fruta_tk)
        mostrar_ajuda_popup()
    except NameError:
        pass


def _add_footer_pdf(canvas, doc):

    canvas.saveState()
    try:
        canvas.setFont(FONT_NAME_PDF, 9)
    except:
        canvas.setFont('Helvetica', 9)

    page_text = f"Página {canvas.getPageNumber()}"
    canvas.drawRightString(doc.width + doc.leftMargin - (0.5*inch),
                           doc.bottomMargin / 2,
                           page_text)
    canvas.restoreState()

def on_press_download(event):
    pass

def on_release_download(event=None):

    if event:
        x, y = event.x_root, event.y_root
        widget_atual = event.widget.winfo_containing(x, y)
        if widget_atual == botao_Download:
            salvar_como_pdf()
    else:
        salvar_como_pdf()

def salvar_como_pdf():

    if not REPORTLAB_AVAILABLE:
        mostrar_popup_customizado(janela, "Erro de Dependência",
                                  "A biblioteca 'reportlab' é necessária para exportar PDF.\n\n"
                                  "Feche o app, instale-a com:\n"
                                  "py -m pip install reportlab\n\n"
                                  "E tente novamente.",
                                  tipo='erro')
        return

    plano_texto = texto_plano.get(1.0, "end").strip()

    if not plano_texto:
        mostrar_popup_customizado(janela, "Aviso", "Não há plano gerado para salvar.", tipo='aviso')
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Documents", "*.pdf")],
        title="Salvar Plano de Colheita como PDF",
        initialfile="Plano_de_Colheita.pdf"
    )

    if not filepath:
        return

    try:
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                                rightMargin=0.75*inch, leftMargin=0.75*inch,
                                topMargin=0.75*inch, bottomMargin=0.75*inch)

        story = []

        COR_TITULO = HexColor("#6B3710")
        COR_HEADING = HexColor("#8a5737")
        COR_TEXTO = HexColor("#222222")

        style_title = ParagraphStyle(
            name='TitleStyle',
            fontName=FONT_NAME_PDF,
            fontSize=20,
            textColor=COR_TITULO,
            alignment=1,
            spaceAfter=12
        )

        style_heading = ParagraphStyle(
            name='HeadingStyle',
            fontName=FONT_NAME_PDF,
            fontSize=14,
            textColor=COR_HEADING,
            spaceBefore=10,
            spaceAfter=6,
            alignment=0
        )

        style_body = ParagraphStyle(
            name='BodyStyle',
            fontName=FONT_NAME_PDF,
            fontSize=10,
            textColor=COR_TEXTO,
            leading=14,
            alignment=0
        )

        style_body_indent = ParagraphStyle(
            name='BodyIndentStyle',
            parent=style_body,
            leftIndent=0.25 * inch,
            firstLineIndent=0
        )


        story.append(Paragraph("Plano de Colheita", style_title))

        linhas = plano_texto.split('\n')

        for linha in linhas:
            linha_strip = linha.strip()

            if not linha_strip:
                story.append(Spacer(1, 0.1 * inch))
                continue

            if linha_strip.startswith('---'):
                texto_limpo = linha_strip.replace('---', '').strip()
                story.append(Paragraph(texto_limpo, style_heading))

            elif (linha_strip.startswith('▪️') or
                  linha_strip.startswith('>') or
                  linha_strip.startswith('(') or
                  linha_strip.startswith('✅') or
                  linha_strip.startswith('[AVISO:')):
                story.append(Paragraph(linha, style_body_indent))

            else:
                story.append(Paragraph(linha, style_body))

        doc.build(story,
                  onFirstPage=_add_footer_pdf,
                  onLaterPages=_add_footer_pdf)

        mostrar_popup_customizado(janela, "Sucesso", f"Plano customizado salvo com sucesso em:\n{filepath}", tipo='info')

    except PermissionError:
          mostrar_popup_customizado(janela, "Erro de Permissão",
                                    "Não foi possível salvar o arquivo.\n\n"
                                    "Verifique se você tem permissão para salvar neste local "
                                    "ou se o arquivo já está aberto em outro programa.",
                                    tipo='erro')
    except Exception as e:
        mostrar_popup_customizado(janela, "Erro ao Salvar PDF", f"Não foi possível salvar o arquivo PDF.\n\nDetalhe: {e}\n\n(Verifique se a fonte '{FONT_NAME_PDF}' está acessível)", tipo='erro')



def verificar_clique(event):
    janela.focus_set()
    area_fechar = (largura_janela - 36, 6, largura_janela - 16, 26)

    if area_fechar[0] <= event.x <= area_fechar[2] and area_fechar[1] <= event.y <= area_fechar[3]:
        fechar_janela()
    else:
        if event.widget == background_label:
            iniciar_movimento(event)

def gerenciar_cursor(event):
    area_fechar = (largura_janela - 36, 6, largura_janela - 16, 26)

    if area_fechar[0] <= event.x <= area_fechar[2] and area_fechar[1] <= area_fechar[3]:
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
    abrir_calendario_popup(janela, botao_calendario)

def criar_dados_entrada(opcao, quantidade, data):
    return {
        "opcao_estrategia": opcao,
        "quantidade": quantidade,
        "data_inicio": data
    }

def mostrar_plano():
    opcao = combobox.get()
    quantidade = entrada_quantidade.get()
    data = getattr(janela, 'data_selecionada', 'Nenhuma data selecionada')

    if opcao == "Selecione uma opção":
        mostrar_popup_customizado(janela, "Aviso", "Por favor, selecione uma opção antes de continuar.", tipo='aviso')
        return

    if not quantidade or quantidade.strip() == "" or quantidade == "Digite a quantidade":
        mostrar_popup_customizado(janela, "Aviso", "Por favor, digite uma quantidade válida.", tipo='aviso')
        return

    try:
        quantidade_valor = int(quantidade)
        if quantidade_valor <= 0:
            mostrar_popup_customizado(janela, "Aviso", "A quantidade deve ser um número positivo.", tipo='aviso')
            return
    except ValueError:
        mostrar_popup_customizado(janela, "Aviso", "A quantidade deve ser um número inteiro.", tipo='aviso')
        return

    if not data or "->" not in data:
        mostrar_popup_customizado(janela, "Aviso", "Por favor, selecione um INTERVALO completo no calendário (clique em 2 dias).", tipo='aviso')
        return

    dados_entrada = criar_dados_entrada(opcao, quantidade_valor, data)
    texto_final = ""

    try:
        texto_final = tratar_e_processar_dados(dados_entrada)

    except Exception as e:
        print("--- ERRO NO PROCESSAMENTO DE DADOS/NARRATIVA ---")
        traceback.print_exc()
        print("-------------------------------------------------")

        mostrar_popup_customizado(janela, "Erro de Processamento", f"Ocorreu um erro interno na lógica: {e}. Verifique o terminal para detalhes.", tipo='erro')
        texto_final = f"📋 Plano de Colheita\nOpção: {opcao}\nQuantidade: {quantidade}\nData: {data}\n\n[ERRO: Falha ao processar dados.]"

    if not isinstance(texto_final, str):
        texto_final = "ERRO CRÍTICO: O resultado final não foi formatado como texto."
        mostrar_popup_customizado(janela, "Erro Crítico", "Falha interna ao gerar o texto do plano.", tipo='erro')

    try:
        img_limpa_tk = ImageTk.PhotoImage(janela.imagem_base_pil)
        background_label.config(image=img_limpa_tk)
        background_label.image = img_limpa_tk

        texto_plano.config(state="normal")

        texto_plano.delete(1.0, "end")

        texto_plano.insert("end", texto_final)

        janela.update_idletasks()

        top, bottom = texto_plano.yview()

        if bottom < 1.0:

            texto_plano.pack_forget()
            scrollbar.pack(side="right", fill="y", padx=(0, 4), pady=4)
            texto_plano.pack(side="left", fill="both", expand=True)
        else:
            scrollbar.pack_forget()
            texto_plano.pack_forget()
            texto_plano.pack(side="left", fill="both", expand=True)

        texto_plano.config(state="disabled")

    except Exception as e:
        mostrar_popup_customizado(janela, "Erro de UI", f"Não foi possível exibir o plano: {e}", tipo='erro')

def mostrar_ajuda_popup():
    if hasattr(janela, 'ajuda_popup') and janela.ajuda_popup.winfo_exists():
        janela.ajuda_popup.destroy()
        return

    ajuda_popup = tk.Toplevel(janela)
    janela.ajuda_popup = ajuda_popup
    ajuda_popup.overrideredirect(True)
    ajuda_popup.attributes('-topmost', True)
    ajuda_popup.config(bg="#f3b874", highlightbackground="#6B3710", highlightcolor="#6B3710", highlightthickness=3)

    texto_ajuda = """
Olá! Seja bem-vindo(a) ao
✨🌱 Farm Planning Assistant 🌱✨

========================================
    Pronto(a) para a colheita perfeita?
    É simples assim:

1. Selecione sua opção de plantio (área/aspersor) e a quantidade.
2. Clique em '📅' para definir o período no calendário.
3. Aperte 'Gerar' e veja a mágica acontecer!
4. Quer guardar o plano? Use 'Download'.
5. Para recomeçar, clique em 'Resetar'.

========================================

🎉 Divirta-se planejando! 🌿 Boa sorte e ótimas plantações! 💖
"""

    label_ajuda = tk.Label(ajuda_popup,
                           text=texto_ajuda,
                           font=("Londrina Solid", 11),
                           bg="#f3b874",
                           justify=tk.LEFT,
                           wraplength=280,
                           padx=10, pady=10)
    label_ajuda.pack()

    janela.update_idletasks()
    ajuda_popup.update_idletasks()

    largura_popup = ajuda_popup.winfo_reqwidth()

    pos_x = janela.winfo_x() + botao_ajuda.winfo_x() + (botao_ajuda.winfo_width() // 2) - (largura_popup // 2)
    pos_y = janela.winfo_y() + botao_ajuda.winfo_y() + botao_ajuda.winfo_height() + 8

    ajuda_popup.geometry(f"+{pos_x}+{pos_y}")

    ajuda_popup.bind("<FocusOut>", lambda e: ajuda_popup.destroy())
    ajuda_popup.focus_set()


def mostrar_popup_customizado(janela_pai, titulo, mensagem, tipo='aviso'):

    COR_FUNDO_POPUP = "#f3b874"
    COR_BORDA_POPUP = "#6B3710"
    COR_CABECALHO_BG = "#be8053"
    COR_CABECALHO_FG = "#fdf5e6"
    COR_BOTAO_ACTIVE = "#f3a166"
    COR_TEXTO_MENSAGEM = "#6B3710"

    popup = tk.Toplevel(janela_pai)
    popup.overrideredirect(True)
    popup.attributes('-topmost', True)
    popup.config(bg=COR_FUNDO_POPUP,
                 highlightbackground=COR_BORDA_POPUP,
                 highlightcolor=COR_BORDA_POPUP,
                 highlightthickness=3)

    if tipo == 'aviso':
        icone = "⚠️"
    elif tipo == 'erro':
        icone = "❌"
    else:
        icone = "✅"

    frame_titulo = tk.Frame(popup, bg=COR_CABECALHO_BG)
    label_titulo = tk.Label(frame_titulo,
                            text=f" {icone} {titulo} ",
                            font=("Londrina Solid", 14, "bold"),
                            bg=COR_CABECALHO_BG,
                            fg=COR_CABECALHO_FG)
    label_titulo.pack(pady=4)
    frame_titulo.pack(fill="x", padx=0, pady=0)

    label_msg = tk.Label(popup,
                         text=mensagem,
                         font=("Londrina Solid", 12),
                         bg=COR_FUNDO_POPUP,
                         fg=COR_TEXTO_MENSAGEM,
                         wraplength=300,
                         justify=tk.LEFT,
                         padx=20, pady=15)
    label_msg.pack(fill="x")

    btn_ok = tk.Button(popup,
                     text="OK",
                     command=popup.destroy,
                     bg=COR_CABECALHO_BG,
                     fg=COR_CABECALHO_FG,
                     activebackground=COR_BOTAO_ACTIVE,
                     activeforeground=COR_CABECALHO_FG,
                     relief="flat",
                     font=("Londrina Solid", 11, "bold"),
                     width=8,
                     cursor="hand2")
    btn_ok.pack(pady=(5, 15))

    janela_pai.update_idletasks()
    popup.update_idletasks()

    popup_width = popup.winfo_reqwidth()
    popup_height = popup.winfo_reqheight()

    pai_x = janela_pai.winfo_x()
    pai_y = janela_pai.winfo_y()
    pai_width = janela_pai.winfo_width()
    pai_height = janela_pai.winfo_height()

    pos_x = pai_x + (pai_width // 2) - (popup_width // 2)
    pos_y = pai_y + (pai_height // 2) - (popup_height // 2)

    popup.geometry(f"+{pos_x}+{pos_y}")

    popup.grab_set()
    popup.focus_set()
    janela_pai.wait_window(popup)


PYGAME_INITIALIZED = False
if PYGAME_AVAILABLE:
    PYGAME_INITIALIZED = inicializar_audio()
    if PYGAME_INITIALIZED:
        tocar_musica()


janela = tk.Tk()
janela.title("Farm Planning Assistant")
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

try:
    imagem_pil_original = Image.open(os.path.join(CAMINHO_IMAGENS, "img_tela_2.png")).convert("RGBA")

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
            imagem_pil_original.paste(imagem_personagem_pil, (8, 455), imagem_personagem_pil)
        else:
            print("⚠️ Nenhuma imagem encontrada em 'images personagens'.")

    except Exception as e:
        print(f"⚠️ Erro ao carregar personagem: {e}")

    imagem_pil_arredondada = arredondar_cantos(imagem_pil_original, 24)
    janela.imagem_base_pil = imagem_pil_arredondada.copy()
    imagem_tk = ImageTk.PhotoImage(janela.imagem_base_pil)

except FileNotFoundError:
    mostrar_popup_customizado(janela, "Erro", f"Imagem base não encontrada em {os.path.join(CAMINHO_IMAGENS, 'img_tela_2.png')}.", tipo='erro')
    janela.destroy()
    exit()

try:
    fonte_para_desenho = ImageFont.truetype(CAMINHO_FONTE, 14)
except IOError:
    fonte_para_desenho = ImageFont.load_default()

icone_disponivel = False
try:
    icone_fruta_pil = Image.open(os.path.join(CAMINHO_IMAGENS, "fruta_icone.png")).convert("RGBA")
    icone_fruta_pil = icone_fruta_pil.resize((32, 32), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Brightness(icone_fruta_pil)
    icone_fruta_pressed_pil = enhancer.enhance(0.7)
    icone_fruta_tk = ImageTk.PhotoImage(icone_fruta_pil)
    icone_fruta_pressed_tk = ImageTk.PhotoImage(icone_fruta_pressed_pil)
    icone_disponivel = True
except FileNotFoundError:
    print(f"Erro de Imagem: O arquivo 'fruta_icone.png' não foi encontrado em {CAMINHO_IMAGENS}.")
    icone_disponivel = False


largura_janela, altura_janela = imagem_tk.width(), imagem_tk.height()
pos_x = (janela.winfo_screenwidth() // 2) - (largura_janela // 2)
pos_y = (janela.winfo_screenheight() // 2) - (altura_janela // 2)
janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
janela.config(bg="#abcdef")
janela.attributes("-transparentcolor", "#abcdef")

style = ttk.Style(janela)
style.theme_use('clam')

COR_FUNDO_CAMPO = '#f3b874'
COR_TEXTO = 'black'
COR_FUNDO_SETA = '#f3b874'
COR_SETA = 'black'
COR_SETA_HOVER = 'white'
COR_FUNDO_SETA_HOVER = '#f3b874'

style.configure('TCombobox',
                fieldbackground=COR_FUNDO_CAMPO,
                background=COR_FUNDO_SETA,
                foreground=COR_TEXTO,
                arrowcolor=COR_SETA,
                borderwidth=0,
                highlightthickness=0,
                padding=0,
                selectbackground=COR_FUNDO_CAMPO,
                selectforeground=COR_TEXTO
                )

style.configure('TCombobox.field',
                background=COR_FUNDO_CAMPO,
                borderwidth=0,
                relief='flat',
                highlightthickness=0)

style.map('TCombobox',
          fieldbackground=[('readonly', COR_FUNDO_CAMPO)],
          foreground=[('readonly', COR_TEXTO)],
          background=[('readonly', COR_FUNDO_SETA),
                      ('active', COR_FUNDO_SETA_HOVER)],
          arrowcolor=[('readonly', COR_SETA),
                      ('active', COR_SETA_HOVER)],
          selectbackground=[('readonly', COR_FUNDO_CAMPO), ('focus', COR_FUNDO_CAMPO)],
          selectforeground=[('readonly', COR_TEXTO), ('focus', COR_TEXTO)]
          )

style.map('TCombobox.field',
          background=[('readonly', COR_FUNDO_CAMPO)])

style.layout('TCombobox', [
    ('Combobox.field', {'sticky': 'nswe', 'children': [
        ('Combobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [
            ('Combobox.textarea', {'sticky': 'nswe'})
        ]})
    ]}),
    ('Combobox.arrow', {'sticky': 'ns', 'side': 'right'})
])


COR_TROUGH = '#f3b874'
COR_THUMB = '#be8053'
COR_THUMB_ACTIVE = '#8a5737'
COR_BORDER = '#6B3710'
COR_ARROW = '#6B3710'

style.configure('Custom.Vertical.TScrollbar',
                gripcount=0,
                background=COR_THUMB,
                darkcolor=COR_THUMB,
                lightcolor=COR_THUMB,
                troughcolor=COR_TROUGH,
                bordercolor=COR_BORDER,
                arrowcolor=COR_ARROW,
                relief='flat',
                arrowsize=14
                )

style.map('Custom.Vertical.TScrollbar',
          background=[('active', COR_THUMB_ACTIVE),
                      ('!active', COR_THUMB)],
          arrowcolor=[('pressed', 'white'),
                      ('!pressed', COR_ARROW)]
          )


background_label = tk.Label(janela, image=imagem_tk, bg="#abcdef", borderwidth=0)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = imagem_tk


frame_plano = tk.Frame(janela, bg="#f3b874", borderwidth=0, highlightthickness=0)

scrollbar = ttk.Scrollbar(frame_plano,
                          orient="vertical",
                          style='Custom.Vertical.TScrollbar',
                          cursor="hand2")

texto_plano = tk.Text(frame_plano,
                      wrap="word",
                      bg="#f3b874",
                      fg="black",
                      font=("Londrina Solid", 12),
                      borderwidth=0,
                      highlightthickness=0,
                      padx=5,
                      pady=5,
                      yscrollcommand=scrollbar.set)

texto_plano.pack(side="left", fill="both", expand=True)

scrollbar.config(command=texto_plano.yview)

frame_plano.place(x=378, y=85, width=400, height=450)
texto_plano.config(state="disabled")


vcmd = (janela.register(validate_input), '%P')

combobox = ttk.Combobox(janela, values=["Aspersor - Nível 2", "Área Plantável"], state="readonly")
combobox.set("Selecione uma opção")
combobox.place(x=28, y=122, width=182, height=33)
janela.option_add('*TCombobox*Listbox.cursor', 'hand2')
combobox.bind('<Enter>', lambda event: janela.config(cursor='hand2'))
combobox.bind('<Leave>', lambda event: janela.config(cursor=''))
adicionar_som_hover(combobox)


entrada_quantidade = tk.Entry(janela, borderwidth=0, bg="#f3b874", fg='grey')
entrada_quantidade.insert(0, "Digite a quantidade")
entrada_quantidade.bind('<FocusIn>', on_focus_in)
entrada_quantidade.bind('<FocusOut>', on_focus_out)
entrada_quantidade.place(x=22, y=174, width=182, height=37)

botao_calendario = tk.Label(janela, text="📅", font=("Arial", 16), bg="#f3b874", cursor="hand2")
botao_calendario.place(x=250, y=123)
botao_calendario.bind("<Button-1>", lambda e: call_abrir_calendario())
adicionar_som_hover(botao_calendario)

largura_botao, altura_botao = 80, 32
padding_botoes = 37

img_grad = criar_imagem_gradiente(largura_botao, altura_botao, "#f3b874", "#be8053")
img_grad_tk = ImageTk.PhotoImage(img_grad)


pos_x_gerar = 20
pos_y_linha1 = 235
botao_GerarPlano = tk.Label(janela, text="Gerar Plano", font=("Londrina Solid", 12),
                            image=img_grad_tk, compound="center", fg="black",
                            bg="#abcdef", borderwidth=0, cursor="hand2")
botao_GerarPlano.image = img_grad_tk
botao_GerarPlano.place(x=pos_x_gerar, y=pos_y_linha1, width=largura_botao, height=altura_botao)
botao_GerarPlano.bind("<ButtonPress-1>", on_press_gerar)
botao_GerarPlano.bind("<ButtonRelease-1>", on_release_gerar)
botao_GerarPlano.bind("<Enter>", lambda e: animate_hover_color(e.widget, "#000000", "#FFFFFF", 150))
botao_GerarPlano.bind("<Leave>", lambda e: animate_hover_color(e.widget, "#FFFFFF", "#000000", 150))
adicionar_som_hover(botao_GerarPlano)


pos_x_resetar = pos_x_gerar + largura_botao + padding_botoes
botao_Resetar = tk.Label(janela, text="Resetar", font=("Londrina Solid", 12),
                            image=img_grad_tk, compound="center", fg="black",
                            bg="#abcdef", borderwidth=0, cursor="hand2")
botao_Resetar.image = img_grad_tk
botao_Resetar.place(x=pos_x_resetar, y=pos_y_linha1, width=largura_botao, height=altura_botao)
botao_Resetar.bind("<ButtonPress-1>", on_press_reset)
botao_Resetar.bind("<ButtonRelease-1>", on_release_reset)
botao_Resetar.bind("<Enter>", lambda e: animate_hover_color(e.widget, "#000000", "#FFFFFF", 150))
botao_Resetar.bind("<Leave>", lambda e: animate_hover_color(e.widget, "#FFFFFF", "#000000", 150))
adicionar_som_hover(botao_Resetar)


pos_y_linha2 = pos_y_linha1 + altura_botao + 24
pos_x_download = (pos_x_gerar + pos_x_resetar) // 2

botao_Download = tk.Label(janela, text="Download", font=("Londrina Solid", 12),
                            image=img_grad_tk, compound="center", fg="black",
                            bg="#abcdef", borderwidth=0, cursor="hand2")
botao_Download.image = img_grad_tk
botao_Download.place(x=pos_x_download, y=pos_y_linha2, width=largura_botao, height=altura_botao)
botao_Download.bind("<ButtonPress-1>", on_press_download)
botao_Download.bind("<ButtonRelease-1>", on_release_download)
botao_Download.bind("<Enter>", lambda e: animate_hover_color(e.widget, "#000000", "#FFFFFF", 150))
botao_Download.bind("<Leave>", lambda e: animate_hover_color(e.widget, "#FFFFFF", "#000000", 150))
adicionar_som_hover(botao_Download)


if icone_disponivel:
    botao_ajuda = tk.Label(janela, image=icone_fruta_tk, borderwidth=0, cursor="hand2")
    botao_ajuda.config(bg="#e4a96a")
    botao_ajuda.image = icone_fruta_tk
    botao_ajuda.place(x=248, y=177)

    botao_ajuda.bind("<ButtonPress-1>", on_press_ajuda)
    botao_ajuda.bind("<ButtonRelease-1>", on_release_ajuda)
    adicionar_som_hover(botao_ajuda)

background_label.bind("<Button-1>", verificar_clique)
background_label.bind("<B1-Motion>", mover_janela)
background_label.bind("<Motion>", gerenciar_cursor)


janela.mainloop()