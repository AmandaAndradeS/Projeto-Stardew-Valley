from modelo import carregar_cultivos, carregar_eventos, criar_calendario, anotar_feriados, cultivos_com_intervalo
from metricas_input import metrica_obg

if __name__ == "__main__":
    # Carrega dados dos CSVs
    eventos_df = carregar_eventos()
    cultivos_df = carregar_cultivos()

    # Cria calendário completo
    todas_estacoes = ["Primavera", "Verão", "Outono", "Inverno"]
    calendario_completo = []
    for est in todas_estacoes:
        calendario_completo += criar_calendario(est)
    calendario_completo = anotar_feriados(calendario_completo, eventos_df)

    # Coleta métricas do usuário
    metricas = metrica_obg()

    # Calcula cultivos possíveis no intervalo
    cultivos_possiveis = cultivos_com_intervalo(metricas, cultivos_df)

    if cultivos_possiveis.empty:
        print("Nenhuma planta disponível para o intervalo selecionado.")
    else:
        print("Cultivos possíveis e número de colheitas:")
        for _, row in cultivos_possiveis.iterrows():
            print(f"- {row['planta'].capitalize()}: {row['colheitas']} colheita(s)")
