from unidecode import unidecode

estacoes = ["primavera", "verao", "outono", "inverno"]
estacoes_normalizadas = [unidecode(e.lower()) for e in estacoes]

def escolher_estacao(msg):
    while True:
        entrada = input(msg).strip().lower()
        entrada_norm = unidecode(entrada)
        if entrada_norm in estacoes_normalizadas:
            indice = estacoes_normalizadas.index(entrada_norm)
            return estacoes[indice], indice
        print("Estação inválida! Digite: primavera, verao, outono, inverno.")

def escolher_dia(msg):
    while True:
        try:
            dia = int(input(msg))
            if 1 <= dia <= 28:
                return dia
            print("Digite um dia entre 1 e 28.")
        except ValueError:
            print("Entrada inválida! Digite um número.")

def escolher_qtd_aspersores(msg):
    while True:
        try:
            qtd = int(input(msg))
            if qtd >= 0:
                return qtd
            print("Digite um número positivo.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")

def metrica_obg():
    print("Bem-vindo ao Farm Planning Assistant!\n"
          "Preencha as métricas importantes para o plantio.\n")

    estacao_ini, idx_ini = escolher_estacao("Em qual estação deseja começar?: ")
    estacao_fim, idx_fim = escolher_estacao("Em qual estação deseja terminar?: ")

    while idx_fim < idx_ini:
        print("Intervalo impossível! A estação final não pode ser anterior à inicial.")
        estacao_fim, idx_fim = escolher_estacao("Em qual estação deseja terminar?: ")

    dia_ini = escolher_dia(f"Dia de início em {estacao_ini.capitalize()} (1-28): ")
    dia_fim = escolher_dia(f"Dia de término em {estacao_fim.capitalize()} (1-28): ")

    while estacao_ini == estacao_fim and dia_fim < dia_ini:
        print("Dia de término deve ser maior ou igual ao dia de início na mesma estação.")
        dia_fim = escolher_dia(f"Dia de término em {estacao_fim.capitalize()} (1-28): ")

    qtd_aspersores = escolher_qtd_aspersores("Quantos aspersores de qualidade (nível 2) você possui?: ")

    return {
        "estacao_ini": unidecode(estacao_ini.lower()),
        "dia_ini": dia_ini,
        "estacao_fim": unidecode(estacao_fim.lower()),
        "dia_fim": dia_fim,
        "aspersores_nivel2": qtd_aspersores
    }
