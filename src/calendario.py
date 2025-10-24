import tkinter as tk
import time 

TKCALENDAR_AVAILABLE = True

ESTACOES = ["Primavera", "Verão", "Outono", "Inverno"]
DIAS_POR_ESTACAO = 28
DIAS_SEMANA = ["S", "T", "Q", "Q", "S", "S", "D"]

COR_FUNDO_POPUP = "#f3b874"
COR_BORDA_POPUP = "#6B3710"
COR_CABECALHO = "#be8053"
COR_TEXTO_CABECALHO = "#fdf5e6"

COR_DIA_BG = "#fdf5e6"
COR_DIA_HOVER = "#f0e6d2"
COR_DIA_FG = "#6B3710"

COR_INICIO = "#4a934a"
COR_FIM = "#4a934a"
COR_INTERVALO = "#a9e3b3"


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

def animate_hover_bg(widget, start_color, end_color, duration_ms=150):
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
                widget.config(bg=end_color)
            if hasattr(widget, "_animation_id"):
                delattr(widget, "_animation_id")
            return
            
        current_color = _interpolate_color(start_color, end_color, fraction)
        
        try:
            if widget.winfo_exists():
                widget.config(bg=current_color)
                widget._animation_id = widget.after(16, animation_step)
            else:
                if hasattr(widget, "_animation_id"):
                    delattr(widget, "_animation_id")
        except tk.TclError:
            if hasattr(widget, "_animation_id"):
                delattr(widget, "_animation_id")

    animation_step()


def data_para_dia_global(data):
    if not data:
        return -1
    try:
        estacao_idx = ESTACOES.index(data["estacao"])
        return (estacao_idx * DIAS_POR_ESTACAO) + data["dia"]
    except ValueError:
        return -1

def comparar_datas(a, b):
    dia_a = data_para_dia_global(a)
    dia_b = data_para_dia_global(b)
    return dia_a - dia_b

def dentro_do_intervalo(data, inicio, fim):
    if not inicio or not fim:
        return False
        
    dia_data = data_para_dia_global(data)
    dia_inicio = data_para_dia_global(inicio)
    dia_fim = data_para_dia_global(fim)
    
    return dia_inicio <= dia_data <= dia_fim


def abrir_calendario_popup(janela, botao_calendario):
    if hasattr(janela, 'calendario_popup') and janela.calendario_popup.winfo_exists():
        janela.calendario_popup.focus_set()
        return

    top = tk.Toplevel(janela)
    janela.calendario_popup = top
    top.overrideredirect(True)
    top.attributes('-topmost', True)
    top.config(bg=COR_FUNDO_POPUP, highlightbackground=COR_BORDA_POPUP, highlightcolor=COR_BORDA_POPUP, highlightthickness=3)
    
    estacao_idx = getattr(janela, "estacao_idx", 0)
    if not hasattr(janela, "intervalo_selecionado"):
        janela.intervalo_selecionado = {"inicio": None, "fim": None}
    dias_labels = {}

    def atualizar_dias():
        for d, lbl in dias_labels.items():
            if hasattr(lbl, "_animation_id"):
                try:
                    lbl.after_cancel(lbl._animation_id)
                    delattr(lbl, "_animation_id")
                except (tk.TclError, AttributeError):
                    pass
            lbl.config(bg=COR_DIA_BG, fg=COR_DIA_FG)

        inicio = janela.intervalo_selecionado["inicio"]
        fim = janela.intervalo_selecionado["fim"]

        for d, lbl in dias_labels.items():
            data_atual = {"estacao": ESTACOES[estacao_idx], "dia": d}

            if inicio and fim and dentro_do_intervalo(data_atual, inicio, fim):
                lbl.config(bg=COR_INTERVALO)

            if inicio and comparar_datas(data_atual, inicio) == 0:
                lbl.config(bg=COR_INICIO, fg=COR_TEXTO_CABECALHO)
                
            if fim and comparar_datas(data_atual, fim) == 0:
                lbl.config(bg=COR_FIM, fg=COR_TEXTO_CABECALHO)

    def selecionar_dia(dia):
        data_selecionada = {"estacao": ESTACOES[estacao_idx], "dia": dia}
        
        inicio = janela.intervalo_selecionado["inicio"]
        fim = janela.intervalo_selecionado["fim"]

        if not inicio or (inicio and fim):
            janela.intervalo_selecionado["inicio"] = data_selecionada
            janela.intervalo_selecionado["fim"] = None
        elif comparar_datas(data_selecionada, inicio) < 0:
            janela.intervalo_selecionado["inicio"] = data_selecionada
            janela.intervalo_selecionado["fim"] = None
        else:
            janela.intervalo_selecionado["fim"] = data_selecionada

        inicio = janela.intervalo_selecionado["inicio"]
        fim = janela.intervalo_selecionado["fim"]

        if inicio and fim and comparar_datas(inicio, fim) > 0:
            janela.intervalo_selecionado["inicio"], janela.intervalo_selecionado["fim"] = fim, inicio

        data_ini_str = f"{janela.intervalo_selecionado['inicio']['estacao']} D{janela.intervalo_selecionado['inicio']['dia']}"
        
        if janela.intervalo_selecionado["fim"]:
            data_fim_str = f"{janela.intervalo_selecionado['fim']['estacao']} D{janela.intervalo_selecionado['fim']['dia']}"
            janela.data_selecionada = f"{data_ini_str} -> {data_fim_str}"
        else:
            janela.data_selecionada = data_ini_str

        janela.focus_set()
        top.destroy()
        
    def mudar_estacao(delta):
        nonlocal estacao_idx
        estacao_idx = (estacao_idx + delta) % len(ESTACOES)
        janela.estacao_idx = estacao_idx
        header_label.config(text=ESTACOES[estacao_idx])
        atualizar_dias()

    def on_day_enter(event, dia):
        lbl = dias_labels[dia]
        animate_hover_bg(lbl, lbl.cget("bg"), COR_DIA_HOVER)

    def on_day_leave(event, dia):
        lbl = dias_labels[dia]
        
        inicio = janela.intervalo_selecionado["inicio"]
        fim = janela.intervalo_selecionado["fim"]
        data_atual = {"estacao": ESTACOES[estacao_idx], "dia": dia}

        cor_original = COR_DIA_BG
        cor_final = COR_DIA_FG

        if inicio and fim and dentro_do_intervalo(data_atual, inicio, fim):
            cor_original = COR_INTERVALO
        if inicio and comparar_datas(data_atual, inicio) == 0:
            cor_original = COR_INICIO
            cor_final = COR_TEXTO_CABECALHO
        if fim and comparar_datas(data_atual, fim) == 0:
            cor_original = COR_FIM
            cor_final = COR_TEXTO_CABECALHO

        animate_hover_bg(lbl, lbl.cget("bg"), cor_original)
        lbl.config(fg=cor_final)
        
    frame_header = tk.Frame(top, bg=COR_CABECALHO)
    frame_header.pack(fill="x")

    btn_prev = tk.Label(frame_header, text="<", font=("Londrina Solid", 14), bg=COR_CABECALHO, fg=COR_TEXTO_CABECALHO, cursor="hand2")
    btn_prev.pack(side="left", padx=10, pady=5)
    btn_prev.bind("<Button-1>", lambda e: mudar_estacao(-1))

    header_label = tk.Label(frame_header, text=ESTACOES[estacao_idx], font=("Londrina Solid", 14), bg=COR_CABECALHO, fg=COR_TEXTO_CABECALHO)
    header_label.pack(side="left", expand=True)

    btn_next = tk.Label(frame_header, text=">", font=("Londrina Solid", 14), bg=COR_CABECALHO, fg=COR_TEXTO_CABECALHO, cursor="hand2")
    btn_next.pack(side="right", padx=10, pady=5)
    btn_next.bind("<Button-1>", lambda e: mudar_estacao(1))

    frame_cal = tk.Frame(top, bg=COR_FUNDO_POPUP, padx=5, pady=5)
    frame_cal.pack(pady=(0, 5))

    for i, dia_semana in enumerate(DIAS_SEMANA):
        lbl = tk.Label(frame_cal, text=dia_semana, font=("Londrina Solid", 11), bg=COR_FUNDO_POPUP, fg=COR_BORDA_POPUP)
        lbl.grid(row=0, column=i, padx=3, pady=3)

    dia = 1
    for linha in range(1, 5):
        for coluna in range(7):
            if dia > DIAS_POR_ESTACAO:
                break
            lbl = tk.Label(frame_cal, text=str(dia), bg=COR_DIA_BG, fg=COR_DIA_FG,
                           width=4, height=2, relief="flat", font=("Londrina Solid", 11),
                           cursor="hand2")
            lbl.grid(row=linha, column=coluna, padx=3, pady=3)
            
            lbl.bind("<Button-1>", lambda e, d=dia: selecionar_dia(d))
            lbl.bind("<Enter>", lambda e, d=dia: on_day_enter(e, d))
            lbl.bind("<Leave>", lambda e, d=dia: on_day_leave(e, d))
            
            dias_labels[dia] = lbl
            dia += 1

    atualizar_dias()

    btn_ok = tk.Button(top, text="Fechar", command=top.destroy,
                   bg=COR_CABECALHO, fg=COR_TEXTO_CABECALHO, relief="flat", width=8, font=("Londrina Solid", 11),
                   activebackground="#f3a166")
    btn_ok.pack(side="bottom", pady=(0, 8))

    janela.update_idletasks()
    top.update_idletasks()

    cal_x = janela.winfo_x() + botao_calendario.winfo_x() + (botao_calendario.winfo_width() // 2) - (top.winfo_width() // 2)
    cal_y = janela.winfo_y() + botao_calendario.winfo_y() + botao_calendario.winfo_height() + 5
    top.geometry(f"+{cal_x}+{cal_y}")
    top.update_idletasks()

    top.bind("<FocusOut>", lambda e: (top.destroy() if e.widget == top else None))