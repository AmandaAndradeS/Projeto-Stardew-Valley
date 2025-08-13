from unidecode import unidecode

def metrica_obg():
    print("Bem vindo ao ajudante Stardew Valley!\n"
          "Abaixo estão as duas métricas importantes que você precisa preencher\n")

    estacao_list = ["Primavera", "Verão", "Outono", "Inverno"]
    estacoes_normalizadas = [unidecode(e.lower()) for e in estacao_list]

    while True:
        entrada = input("Em qual estação você está?: ").strip().lower()
        entrada_normalizada = unidecode(entrada)

        if entrada_normalizada not in estacoes_normalizadas:
            print("Estação inválida! Digite uma das opções: Primavera, Verão, Outono, Inverno.")
        else:
            indice = estacoes_normalizadas.index(entrada_normalizada)
            estacao = estacao_list[indice]
            break

    while True:
        try:
            dias_restantes = int(input("Quantos dias restam para o final da estação? "))
            if dias_restantes < 0:
                print("Por favor, digite um número positivo.")
                continue
            break
        except ValueError:
            print("Entrada inválida! Por favor, digite um número válido.")

    return {
        "estacao": estacao,
        "dias_restantes": dias_restantes
    }
