from modelo import (
    carregar_cultivos,
    carregar_eventos,
    criar_calendario,
    anotar_feriados,
    listar_plantas_possiveis
)
from metricas_input import metrica_obg

if __name__ == "__main__":
    cultivos_df = carregar_cultivos()
    eventos_df = carregar_eventos()

    todas_estacoes = ["Primavera", "Verão", "Outono", "Inverno"]
    calendario_completo = []
    for est in todas_estacoes:
        calendario_completo.extend(criar_calendario(est))
    calendario_completo = anotar_feriados(calendario_completo, eventos_df)

    metricas = metrica_obg()
    sementes_disponiveis = metricas["aspersores_nivel2"] * 8
    plantas_possiveis = listar_plantas_possiveis(metricas, cultivos_df)

    if not plantas_possiveis:
        print("Nenhuma planta pode ser cultivada no intervalo selecionado.")
    else:
        print("\nPlantas possíveis no intervalo selecionado:\n")
        for p in plantas_possiveis:
            lucro_total_area = p["lucro_total"] * sementes_disponiveis
            custo_area = p["lucro_unit"] * sementes_disponiveis
            print(
                f"- {p['planta'].capitalize()} (Estação: {p['estacoes']}) → "
                f"Colheitas possíveis: {p['colheitas_possiveis']} → "
                f"Lucro unitário: {p['lucro_unit']} → "
                f"Lucro total por unidade: {p['lucro_total']} → "
                f"Lucro total área ({sementes_disponiveis} sementes): {lucro_total_area} → "
                f"Custo total de sementes: {custo_area}"
            )

    estacoes = ["primavera", "verão", "outono", "inverno"]
    idx_ini = estacoes.index(metricas["estacao_ini"].lower())
    idx_fim = estacoes.index(metricas["estacao_fim"].lower())

    calendario_intervalo = []
    for dia in calendario_completo:
        idx_atual = estacoes.index(dia["estacao"])
        if idx_ini < idx_fim or (idx_ini == idx_fim and metricas["dia_ini"] <= metricas["dia_fim"]):
            if idx_ini < idx_atual < idx_fim or \
               (idx_atual == idx_ini and dia["dia"] >= metricas["dia_ini"]) or \
               (idx_atual == idx_fim and dia["dia"] <= metricas["dia_fim"]):
                calendario_intervalo.append(dia)
        else:
            if idx_atual >= idx_ini or idx_atual <= idx_fim:
                calendario_intervalo.append(dia)

    feriados_encontrados = [d for d in calendario_intervalo if d["feriado"]]
    if feriados_encontrados:
        print("\n⚠️ Feriados no período selecionado:\n")
        for f in feriados_encontrados:
            print(
                f"- Dia {f['dia']} de {f['estacao'].capitalize()} "
                f"({f['dia_semana']}) → {f['festival'].capitalize()} | Motivo: {f['obs']}"
            )
    else:
        print("\n✅ Nenhum feriado relevante no período selecionado.\n")
