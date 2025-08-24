import pandas as pd

def carregar_cultivos(caminho=r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\data\Cultivos.csv"):
    df = pd.read_csv(caminho, sep=";")
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].str.strip().str.lower()
    for coluna in ["dias_cresc", "intervalo_colheita", "preco_semente", "preco_venda"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    return df

def carregar_eventos(caminho=r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\data\Estações e Festivais.csv"):
    df = pd.read_csv(caminho, sep=";")
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].str.strip().str.lower()
    df["dia_festival"] = pd.to_numeric(df["dia_festival"], errors="coerce").astype("Int64")
    return df

def criar_calendario(estacao):
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    return [
        {"estacao": estacao.lower(), "dia": dia, "dia_semana": dias_semana[(dia - 1) % 7]}
        for dia in range(1, 29)
    ]

def anotar_feriados(calendario, eventos_df):
    for dia in calendario:
        evento = eventos_df[
            (eventos_df["estacao"] == dia["estacao"]) & (eventos_df["dia_festival"] == dia["dia"])
        ]
        if not evento.empty:
            info = evento.iloc[0]
            dia["feriado"] = True
            dia["festival"] = info["festival"]
            dia["afeta_cultivo"] = info["afeta_cultivo"]
        else:
            dia["feriado"] = False
            dia["festival"] = None
            dia["afeta_cultivo"] = None
    return calendario

def transformar_intervalo_em_dias(metricas):
    estacoes = ["primavera", "verão", "outono", "inverno"]
    idx_ini = estacoes.index(metricas["estacao_ini"].strip().lower())
    idx_fim = estacoes.index(metricas["estacao_fim"].strip().lower())
    if idx_ini == idx_fim:
        return metricas["dia_fim"] - metricas["dia_ini"] + 1
    dias_na_ini = 28 - metricas["dia_ini"] + 1
    dias_intermediarios = (idx_fim - idx_ini - 1) * 28 if (idx_fim - idx_ini - 1) > 0 else 0
    dias_na_fim = metricas["dia_fim"]
    return dias_na_ini + dias_intermediarios + dias_na_fim

def cresce_na_estacao(estacao_cultivo, estacao_verificar):
    return estacao_verificar in [e.strip().lower() for e in estacao_cultivo.split(",")]

def cultivos_por_estacao(metricas, cultivos_df):
    estacao_ini = metricas["estacao_ini"].strip().lower()
    estacao_fim = metricas["estacao_fim"].strip().lower()
    if estacao_ini == estacao_fim:
        return cultivos_df[cultivos_df["estacao"].apply(lambda x: cresce_na_estacao(x, estacao_ini))]
    plantas_ambas = cultivos_df[cultivos_df["estacao"].apply(
        lambda x: cresce_na_estacao(x, estacao_ini) and cresce_na_estacao(x, estacao_fim)
    )]
    if not plantas_ambas.empty:
        return plantas_ambas
    return pd.concat([
        cultivos_df[cultivos_df["estacao"].apply(lambda x: cresce_na_estacao(x, estacao_ini))],
        cultivos_df[cultivos_df["estacao"].apply(lambda x: cresce_na_estacao(x, estacao_fim))]
    ])

def calcular_colheitas_simples(dias_totais, dias_cresc, intervalo_colheita):
    if pd.isna(intervalo_colheita) or intervalo_colheita == 0:
        return dias_totais // dias_cresc
    primeiro_dia_colheita = dias_cresc + 1
    if primeiro_dia_colheita > dias_totais:
        return 0
    colheitas = 1
    dia_atual = primeiro_dia_colheita
    while True:
        proxima_colheita = dia_atual + intervalo_colheita
        if proxima_colheita > dias_totais:
            break
        colheitas += 1
        dia_atual = proxima_colheita
    return colheitas

def cultivos_com_intervalo(metricas, cultivos_df):
    plantas_filtradas = cultivos_por_estacao(metricas, cultivos_df)
    dias_totais = transformar_intervalo_em_dias(metricas)
    cultivos_possiveis = []
    for _, row in plantas_filtradas.iterrows():
        n_colheitas = calcular_colheitas_simples(
            dias_totais,
            row["dias_cresc"],
            row["intervalo_colheita"]
        )
        if n_colheitas > 0:
            cultivos_possiveis.append({
                "planta": row["cultivo"],
                "estacoes": row["estacao"],
                "dias_cresc": row["dias_cresc"],
                "colheitas": n_colheitas
            })
    return pd.DataFrame(cultivos_possiveis)
