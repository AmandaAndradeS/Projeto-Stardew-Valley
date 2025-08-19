import pandas as pd

# Funções de leitura e limpeza de CSV
def carregar_cultivos(caminho=r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\data\Cultivos.csv"):
    df = pd.read_csv(caminho, sep=";")
    # Limpeza e normalização de texto
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].str.strip().str.lower()
    # Converte campos numéricos
    for coluna in ["dias_cresc", "intervalo_colheita", "preco_semente", "preco_venda"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    return df

def carregar_eventos(caminho=r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\data\Estações e Festivais.csv"):
    df = pd.read_csv(caminho, sep=";")
    # Limpeza e normalização de texto
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].str.strip().str.lower()
    df["dia_festival"] = pd.to_numeric(df["dia_festival"], errors="coerce").astype("Int64")
    return df

# Cria calendário de 28 dias por estação
def criar_calendario(estacao):
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    return [
        {"estacao": estacao.lower(), "dia": dia, "dia_semana": dias_semana[(dia - 1) % 7]}
        for dia in range(1, 29)
    ]

# Anota feriados/festivais no calendário
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

# Filtra cultivos por uma ou duas estações
def cultivos_duas_estacoes(metricas, cultivos_df):
    estacao_ini = metricas["estacao_ini"].strip().lower()
    estacao_fim = metricas["estacao_fim"].strip().lower()

    def cresce_na_estacao(estacao_cultivo, estacao_verificar):
        return estacao_verificar in [e.strip().lower() for e in estacao_cultivo.split(",")]

    if estacao_ini == estacao_fim:
        return {"mesma_estacao": cultivos_df[cultivos_df["estacao"].apply(lambda x: cresce_na_estacao(x, estacao_ini))]}

    plantas_ambas = cultivos_df[cultivos_df["estacao"].apply(
        lambda x: cresce_na_estacao(x, estacao_ini) and cresce_na_estacao(x, estacao_fim)
    )]
    if not plantas_ambas.empty:
        return {"crescem_nas_duas": plantas_ambas}

    return {
        "estacao_ini": cultivos_df[cultivos_df["estacao"].apply(lambda x: cresce_na_estacao(x, estacao_ini))],
        "estacao_fim": cultivos_df[cultivos_df["estacao"].apply(lambda x: cresce_na_estacao(x, estacao_fim))]
    }

# Converte intervalo de estações e dias em dias totais
def transformar_intervalo_em_dias(metricas):
    estacoes = ["primavera", "verão", "outono", "inverno"]
    idx_ini = estacoes.index(metricas["estacao_ini"].strip().lower())
    idx_fim = estacoes.index(metricas["estacao_fim"].strip().lower())
    return (idx_fim - idx_ini) * 28 + (metricas["dia_fim"] - metricas["dia_ini"] + 1)

# Função unificada: filtra por estação e calcula colheitas no intervalo
def cultivos_com_intervalo(metricas, cultivos_df):
    resultado_estacoes = cultivos_duas_estacoes(metricas, cultivos_df)

    # Seleção de plantas de acordo com estação
    if "mesma_estacao" in resultado_estacoes:
        plantas_filtradas = resultado_estacoes["mesma_estacao"]
    elif "crescem_nas_duas" in resultado_estacoes:
        plantas_filtradas = resultado_estacoes["crescem_nas_duas"]
    else:
        plantas_filtradas = pd.concat([resultado_estacoes["estacao_ini"], resultado_estacoes["estacao_fim"]])

    dias_totais = transformar_intervalo_em_dias(metricas)
    cultivos_possiveis = []

    for _, row in plantas_filtradas.iterrows():
        dias_cresc = row["dias_cresc"]
        intervalo_colheita = row["intervalo_colheita"]
        tipo = "única" if pd.isna(intervalo_colheita) or intervalo_colheita == 0 else "múltipla"

        if dias_cresc > dias_totais:
            continue

        n_colheitas = 1 if tipo == "única" else max(1 + (dias_totais - dias_cresc) // intervalo_colheita, 0)

        cultivos_possiveis.append({
            "planta": row["cultivo"],
            "estacoes": row["estacao"],
            "tipo": tipo,
            "dias_cresc": dias_cresc,
            "colheitas": n_colheitas
        })

    return pd.DataFrame(cultivos_possiveis)
