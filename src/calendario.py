import tkinter as tk

# A variável TKCALENDAR_AVAILABLE é necessária para a interface principal
TKCALENDAR_AVAILABLE = True

ESTACOES = ["Primavera", "Verão", "Outono", "Inverno"]
DIAS_POR_ESTACAO = 28
DIAS_SEMANA = ["S", "T", "Q", "Q", "S", "S", "D"]

# Cores de destaque
COR_INICIO = "#5fb878"       # Verde escuro (início)
COR_FIM = "#5fb878"          # Verde escuro (fim)
COR_INTERVALO = "#a9e3b3"    # Verde claro (dias intermediários)


def data_para_dia_global(data):
    """Converte a data {'estacao': 'Verão', 'dia': 5} para um dia de 1 a 112."""
    if not data:
        return -1 # Valor inválido
    try:
        estacao_idx = ESTACOES.index(data["estacao"])
        # Calcula o dia global: (Índice da estação * 28 dias) + Dia na estação
        return (estacao_idx * DIAS_POR_ESTACAO) + data["dia"]
    except ValueError:
        return -1

def comparar_datas(a, b):
    """Compara duas datas usando o dia global para precisão entre estações."""
    dia_a = data_para_dia_global(a)
    dia_b = data_para_dia_global(b)
    return dia_a - dia_b

def dentro_do_intervalo(data, inicio, fim):
    """Retorna True se 'data' estiver dentro do intervalo [inicio, fim]."""
    if not inicio or not fim:
        return False
        
    # Converte para o Dia Global para uma comparação simples e robusta
    dia_data = data_para_dia_global(data)
    dia_inicio = data_para_dia_global(inicio)
    dia_fim = data_para_dia_global(fim)
    
    # Verifica se o dia atual está entre o início e o fim (incluindo eles)
    return dia_inicio <= dia_data <= dia_fim


def abrir_calendario_popup(janela, botao_calendario):
    """Exibe um calendário sazonal com suporte à seleção de intervalo de tempo."""

    # Se o popup já existir, foca nele
    if hasattr(janela, 'calendario_popup') and janela.calendario_popup.winfo_exists():
        janela.calendario_popup.focus_set()
        return

    # Criação do popup
    top = tk.Toplevel(janela)
    janela.calendario_popup = top
    top.overrideredirect(True)
    top.attributes('-topmost', True)
    top.config(bg="#f3b874", highlightbackground="#be8053", highlightthickness=2)

    # --- INÍCIO DA CORREÇÃO/CENTRALIZAÇÃO ---
    
    # É necessário desenhar o conteúdo do calendário antes de calcular seu tamanho
    # O restante do código de montagem será executado logo abaixo.
    
    # Posição do popup
    janela.update_idletasks()

    # Monta temporariamente o conteúdo para obter o tamanho do popup
    # (Este é um truque do Tkinter para calcular o tamanho antes de posicionar)
    top.update_idletasks()
    
    largura_popup = top.winfo_reqwidth()
    altura_popup = top.winfo_reqheight()

    # Centraliza o popup na janela principal
    pos_x = janela.winfo_x() + (janela.winfo_width() // 2) - (largura_popup // 2)
    pos_y = janela.winfo_y() + (janela.winfo_height() // 2) - (altura_popup // 2)
    
    # Garante que ele apareça ligeiramente acima do centro para melhor visualização
    pos_y = pos_y - 20
    
    # # Código para ALINHAR AO BOTÃO (Alternativa)
    # pos_x = janela.winfo_x() + botao_calendario.winfo_x()
    # pos_y = janela.winfo_y() + botao_calendario.winfo_y() + botao_calendario.winfo_height() + 5
    
    top.geometry(f"+{pos_x}+{pos_y}")

    # --- FIM DA CORREÇÃO/CENTRALIZAÇÃO ---
    
    # Estado de navegação
    estacao_idx = getattr(janela, "estacao_idx", 0)

    # Guarda o intervalo selecionado na janela principal
    if not hasattr(janela, "intervalo_selecionado"):
        janela.intervalo_selecionado = {"inicio": None, "fim": None}
    
    # Variável para armazenar todos os labels dos dias
    dias_labels = {}

    # === Funções de Ação e Atualização ===

    def atualizar_dias():
        """Atualiza visualmente todos os dias do calendário na estação atual."""
        
        # 1. Reseta a cor de todos os dias
        for d, lbl in dias_labels.items():
            lbl.config(bg="#fff", fg="black")

        inicio = janela.intervalo_selecionado["inicio"]
        fim = janela.intervalo_selecionado["fim"]

        # 2. Aplica as cores de destaque
        for d, lbl in dias_labels.items():
            data_atual = {"estacao": ESTACOES[estacao_idx], "dia": d}

            if inicio and fim and dentro_do_intervalo(data_atual, inicio, fim):
                lbl.config(bg=COR_INTERVALO)

            # Re-aplica as cores de início e fim se estiverem no intervalo
            if inicio and data_atual["estacao"] == inicio["estacao"] and data_atual["dia"] == inicio["dia"]:
                lbl.config(bg=COR_INICIO)
            if fim and data_atual["estacao"] == fim["estacao"] and data_atual["dia"] == fim["dia"]:
                lbl.config(bg=COR_FIM)
                
            # Se apenas o início estiver selecionado, destaque apenas o início
            elif inicio and not fim:
                 if data_atual["estacao"] == inicio["estacao"] and data_atual["dia"] == inicio["dia"]:
                    lbl.config(bg=COR_INICIO)


    def selecionar_dia(dia):
        """Seleciona início/fim do intervalo."""
        estacao = ESTACOES[estacao_idx]

        inicio = janela.intervalo_selecionado["inicio"]
        fim = janela.intervalo_selecionado["fim"]
        
        nova_data = {"estacao": estacao, "dia": dia}

        # Se não há início OU se já há início e fim (inicia uma nova seleção)
        if not inicio or (inicio and fim):
            janela.intervalo_selecionado = {"inicio": nova_data, "fim": None}
            janela.data_selecionada = f"{estacao} - Dia {dia} (Início)" # Atualiza o label do plano
            
        # Se há início mas não há fim (termina a seleção)
        elif not fim:
            janela.intervalo_selecionado["fim"] = nova_data

            # Inverter se o fim for antes do início 
            if comparar_datas(janela.intervalo_selecionado["fim"], janela.intervalo_selecionado["inicio"]) < 0:
                janela.intervalo_selecionado["inicio"], janela.intervalo_selecionado["fim"] = \
                    janela.intervalo_selecionado["fim"], janela.intervalo_selecionado["inicio"]
            
            # Atualiza o label do plano com o intervalo completo
            inicio_data = janela.intervalo_selecionado['inicio']
            fim_data = janela.intervalo_selecionado['fim']

            janela.data_selecionada = (
                f"{inicio_data['estacao']} D{inicio_data['dia']} → {fim_data['estacao']} D{fim_data['dia']}"
            )
            print(f"🌿 Intervalo selecionado: {janela.data_selecionada}")

        atualizar_dias()

    def mudar_estacao(direcao):
        nonlocal estacao_idx
        estacao_idx = (estacao_idx + direcao) % len(ESTACOES)
        label_estacao.config(text=ESTACOES[estacao_idx])
        janela.estacao_idx = estacao_idx
        atualizar_dias()

    # === Montagem do Calendário (Para cálculo de tamanho) ===
    # O código abaixo é essencial para que o 'top.winfo_reqwidth()' funcione acima.

    # Cabeçalho (navegação)
    frame_topo = tk.Frame(top, bg="#be8053")
    frame_topo.pack(fill="x")

    btn_prev = tk.Button(frame_topo, text="←", command=lambda: mudar_estacao(-1),
                         bg="#be8053", fg="white", relief="flat", width=3, font=("Londrina Solid", 11, "bold"))
    btn_prev.pack(side="left", padx=5, pady=3)

    label_estacao = tk.Label(frame_topo, text=ESTACOES[estacao_idx],
                             bg="#be8053", fg="white",
                             font=("Londrina Solid", 13, "bold"))
    label_estacao.pack(side="left", padx=10, pady=3, expand=True)

    btn_next = tk.Button(frame_topo, text="→", command=lambda: mudar_estacao(1),
                         bg="#be8053", fg="white", relief="flat", width=3, font=("Londrina Solid", 11, "bold"))
    btn_next.pack(side="right", padx=5, pady=3)

    # Corpo do calendário
    frame_cal = tk.Frame(top, bg="#f3b874")
    frame_cal.pack(padx=10, pady=8)

    # Cabeçalho dos dias da semana
    for i, nome_dia in enumerate(DIAS_SEMANA):
        lbl = tk.Label(frame_cal, text=nome_dia, font=("Londrina Solid", 11, "bold"),
                       bg="#be8053", fg="white", width=4, height=1)
        lbl.grid(row=0, column=i, padx=1, pady=1)

    # Criação dos dias
    dia = 1
    for linha in range(1, 5):
        for coluna in range(7):
            if dia > DIAS_POR_ESTACAO:
                break
            lbl = tk.Label(frame_cal, text=str(dia), bg="#fff", fg="black",
                           width=4, height=2, relief="ridge", font=("Londrina Solid", 11),
                           cursor="hand2")
            lbl.grid(row=linha, column=coluna, padx=2, pady=2)
            lbl.bind("<Button-1>", lambda e, d=dia: selecionar_dia(d))
            # Armazena o label para atualização visual
            dias_labels[dia] = lbl
            dia += 1

    btn_ok = tk.Button(top, text="Fechar", command=top.destroy,
                       bg="#be8053", fg="white", relief="flat", width=8, font=("Londrina Solid", 11))
    btn_ok.pack(side="bottom", pady=5)

    top.bind("<FocusOut>", lambda e: top.destroy())
    top.focus_set()
    
    # Chama a atualização inicial para destacar o intervalo, se já houver um.
    atualizar_dias()