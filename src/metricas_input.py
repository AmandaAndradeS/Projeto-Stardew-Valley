from unidecode import unidecode

def metrica_obg():
    print("Bem-vindo ao ajudante Stardew Valley!\n"
          "Abaixo você preencherá as métricas importantes para o plantio.\n")

    estacao_list = ["Primavera", "Verão", "Outono", "Inverno"]
    estacoes_normalizadas = [unidecode(e.lower()) for e in estacao_list]

    # Escolha da estação de início
    while True:
        entrada_ini = input("Em qual estação você deseja começar?: ").strip().lower()
        entrada_ini_normalizada = unidecode(entrada_ini)

        if entrada_ini_normalizada not in estacoes_normalizadas:
            print("Estação inválida! Digite uma das opções: Primavera, Verão, Outono, Inverno.")
        else:
            indice_ini = estacoes_normalizadas.index(entrada_ini_normalizada)
            estacao_ini = estacao_list[indice_ini]
            break

    # Escolha da estação de término
    while True:
        entrada_fim = input("Em qual estação você deseja terminar?: ").strip().lower()
        entrada_fim_normalizada = unidecode(entrada_fim)

        if entrada_fim_normalizada not in estacoes_normalizadas:
            print("Estação inválida! Digite uma das opções: Primavera, Verão, Outono, Inverno.")
        else:
            indice_fim = estacoes_normalizadas.index(entrada_fim_normalizada)
            estacao_fim = estacao_list[indice_fim]

            # Bloqueia apenas se a estação final for *menor* que a inicial
            if indice_fim < indice_ini:
                print("Intervalo impossível! A estação final não pode ser anterior à inicial.")
                continue
            # Se for igual ou maior, continua normalmente
            break

    # Escolha dos dias
    while True:
        try:
            dia_ini = int(input(f"Dia de início em {estacao_ini} (1-28): "))
            dia_fim = int(input(f"Dia de término em {estacao_fim} (1-28): "))

            if not (1 <= dia_ini <= 28) or not (1 <= dia_fim <= 28):
                print("Digite dias válidos entre 1 e 28.")
                continue

            # Se início e término forem na mesma estação, verifica ordem dos dias
            if estacao_ini == estacao_fim and dia_fim < dia_ini:
                print("Dia de término deve ser maior ou igual ao dia de início na mesma estação.")
                continue

            break

        except ValueError:
            print("Entrada inválida! Digite um número válido.")

    return {
        "estacao_ini": estacao_ini,
        "dia_ini": dia_ini,
        "estacao_fim": estacao_fim,
        "dia_fim": dia_fim
    }
