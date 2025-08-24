from unidecode import unidecode

estacoes = ["primavera", "verão", "outono", "inverno"]
estacoes_normalizadas = [unidecode(e.lower()) for e in estacoes]

def escolher_estacao(msg):
    while True:
        entrada = input(msg).strip().lower()
        entrada_norm = unidecode(entrada)
        if entrada_norm in estacoes_normalizadas:
            indice = estacoes_normalizadas.index(entrada_norm)
            return estacoes[indice], indice
        print("estação inválida! digite: primavera, verão, outono, inverno.")

def escolher_dia(msg):
    while True:
        try:
            dia = int(input(msg))
            if 1 <= dia <= 28:
                return dia
            print("digite um dia entre 1 e 28.")
        except ValueError:
            print("entrada inválida! digite um número.")

def metrica_obg():
    print("bem-vindo ao ajudante stardew valley!\n"
          "abaixo você preencherá as métricas importantes para o plantio.\n")

    estacao_ini, idx_ini = escolher_estacao("em qual estação você deseja começar?: ")
    estacao_fim, idx_fim = escolher_estacao("em qual estação você deseja terminar?: ")

    while idx_fim < idx_ini:
        print("intervalo impossível! a estação final não pode ser anterior à inicial.")
        estacao_fim, idx_fim = escolher_estacao("em qual estação você deseja terminar?: ")

    dia_ini = escolher_dia(f"dia de início em {estacao_ini} (1-28): ")
    dia_fim = escolher_dia(f"dia de término em {estacao_fim} (1-28): ")

    while estacao_ini == estacao_fim and dia_fim < dia_ini:
        print("dia de término deve ser maior ou igual ao dia de início na mesma estação.")
        dia_fim = escolher_dia(f"dia de término em {estacao_fim} (1-28): ")

    return {
        "estacao_ini": estacao_ini,
        "dia_ini": dia_ini,
        "estacao_fim": estacao_fim,
        "dia_fim": dia_fim
    }
