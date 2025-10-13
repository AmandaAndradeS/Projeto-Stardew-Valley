import pandas as pd
from unidecode import unidecode

def carregar_cultivos(caminho=r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\data\Cultivos.csv"):
    df = pd.read_csv(caminho, sep=";")
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].astype(str).str.strip().str.lower().apply(unidecode)
    for coluna in ["dias_cresc", "intervalo_colheita", "preco_semente", "preco_venda"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    return df

def carregar_eventos(caminho=r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\data\Estações e Festivais.csv"):
    df = pd.read_csv(caminho, sep=";")
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].astype(str).str.strip().str.lower().apply(unidecode)
    df["dia_festival"] = pd.to_numeric(df["dia_festival"], errors="coerce").astype("Int64")
    return df

def criar_calendario(estacao):
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    estacao_normalizada = unidecode(estacao.strip().lower())
    return [
        {"estacao": estacao_normalizada, "dia": dia, "dia_semana": dias_semana[(dia - 1) % 7]}
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
            dia["obs"] = info["obs"]
        else:
            dia["feriado"] = False
            dia["festival"] = None
            dia["afeta_cultivo"] = None
            dia["obs"] = None
    return calendario

def transformar_intervalo_em_dias(metricas):
    estacoes = ["primavera", "verao", "outono", "inverno"]
    idx_ini = estacoes.index(metricas["estacao_ini"].strip().lower())
    idx_fim = estacoes.index(metricas["estacao_fim"].strip().lower())
    if idx_ini == idx_fim:
        return metricas["dia_fim"] - metricas["dia_ini"] + 1
    dias_na_ini = 28 - metricas["dia_ini"] + 1
    dias_intermediarios = (idx_fim - idx_ini - 1) * 28 if (idx_fim - idx_ini - 1) > 0 else 0
    dias_na_fim = metricas["dia_fim"]
    return dias_na_ini + dias_intermediarios + dias_na_fim

def cresce_na_estacao(estacoes, estacao):
    return estacao in {unidecode(e.strip().lower()) for e in estacoes.split(",")}

def cultivos_por_estacao(metricas, cultivos_df):
    est_ini = metricas["estacao_ini"].strip().lower()
    est_fim = metricas["estacao_fim"].strip().lower()
    if est_ini == est_fim:
        return cultivos_df.loc[cultivos_df["estacao"].apply(lambda e: cresce_na_estacao(e, est_ini))]
    df = cultivos_df.loc[cultivos_df["estacao"].apply(
        lambda e: cresce_na_estacao(e, est_ini) and cresce_na_estacao(e, est_fim)
    )]
    if not df.empty:
        return df
    return cultivos_df.loc[cultivos_df["estacao"].apply(
        lambda e: cresce_na_estacao(e, est_ini) or cresce_na_estacao(e, est_fim)
    )]

def calcular_colheitas(dias_totais, dias_cresc, intervalo):
    if not intervalo or pd.isna(intervalo):  
        return dias_totais // dias_cresc
    if dias_totais < dias_cresc:
        return 0
    return 1 + (dias_totais - dias_cresc) // intervalo

def lucro_esperado(planta, colheitas, preco_venda):
    multiplos = {"cafe": 4, "mirtilo": 3, "oxicoco": 2}
    qtd = multiplos.get(planta.lower(), 1)
    return preco_venda * colheitas * qtd 

def listar_plantas_possiveis(metricas, cultivos_df):
    dias_totais = transformar_intervalo_em_dias(metricas)
    plantas = cultivos_por_estacao(metricas, cultivos_df)
    resultado = []
    for _, row in plantas.iterrows():
        if row["cultivo"] == "morango":
            if metricas["estacao_ini"].lower() == "primavera":
                dias_totais = (28 - 13) + 1
            else:
                continue
        colheitas = calcular_colheitas(dias_totais, row["dias_cresc"], row["intervalo_colheita"])
        if colheitas > 0:
            resultado.append({
                "planta": row["cultivo"],
                "estacoes": row["estacao"],
                "colheitas_possiveis": colheitas,
                "lucro_unit": lucro_esperado(row["cultivo"], 1, row["preco_venda"]),
                "lucro_total": lucro_esperado(row["cultivo"], colheitas, row["preco_venda"])
            })
    resultado.sort(key=lambda x: x["lucro_unit"], reverse=True)
    return resultado
