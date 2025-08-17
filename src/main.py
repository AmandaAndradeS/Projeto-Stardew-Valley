# main.py

# Importa funções do arquivo modelo.py
from modelo import carregar_cultivos, carregar_eventos, criar_calendario, anotar_feriados, cultivos_duas_estacoes
# Importa função de métricas do arquivo metricas_input.py
from metricas_input import metrica_obg

if __name__ == "__main__":
    # Carrega dados dos arquivos CSV
    eventos_df = carregar_eventos()
    cultivos_df = carregar_cultivos()

    # Cria calendário completo (4 estações x 28 dias)
    todas_estacoes = ["Primavera", "Verão", "Outono", "Inverno"]
    calendario_completo = []
    for est in todas_estacoes:
        calendario_completo += criar_calendario(est)
    calendario_completo = anotar_feriados(calendario_completo, eventos_df)

    # Coleta métricas do usuário
    metricas = metrica_obg()

    # Filtra cultivos de acordo com as estações escolhidas
    resultado = cultivos_duas_estacoes(metricas, cultivos_df)

    # Exibe resultado
    if "mesma_estacao" in resultado:
        print(f"Plantas na estação {metricas['estacao_ini']}:")
        print(resultado["mesma_estacao"][["cultivo", "estacao"]])
    elif "crescem_nas_duas" in resultado:
        print("Plantas que crescem nas duas estações escolhidas:")
        print(resultado["crescem_nas_duas"][["cultivo", "estacao"]])
    else:
        print(f"Plantas na estação {metricas['estacao_ini']}:")
        print(resultado["estacao_ini"][["cultivo", "estacao"]])
        print(f"\nPlantas na estação {metricas['estacao_fim']}:")
        print(resultado["estacao_fim"][["cultivo", "estacao"]])
