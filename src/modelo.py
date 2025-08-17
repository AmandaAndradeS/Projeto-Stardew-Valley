import pandas as pd

# Funções de limpeza e leitura de CSV
def carregar_cultivos(caminho=r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\data\Cultivos.csv"):
    df = pd.read_csv(caminho, sep=";")
    # Limpeza e normalização de texto
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].str.strip().str.lower()
    # Converte campos numéricos
    df["dias_cresc"] = pd.to_numeric(df["dias_cresc"], errors="coerce")
    df["intervalo_colheita"] = pd.to_numeric(df["intervalo_colheita"], errors="coerce")
    df["preco_semente"] = pd.to_numeric(df["preco_semente"], errors="coerce")
    df["preco_venda"] = pd.to_numeric(df["preco_venda"], errors="coerce")
    return df

def carregar_eventos(caminho=r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\data\Estações e Festivais.csv"):
    df = pd.read_csv(caminho, sep=";")
    # Limpeza e normalização de texto
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].astype(str).str.strip().str.lower()
    df["dia_festival"] = pd.to_numeric(df["dia_festival"], errors="coerce").astype("Int64")
    return df

# Cria calendário de 28 dias por estação
def criar_calendario(estacao):
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    calendario = []
    for dia in range(1, 29):
        dia_semana = dias_semana[(dia - 1) % 7]
        calendario.append({
            "estacao": estacao.lower(),
            "dia": dia,
            "dia_semana": dia_semana
        })
    return calendario #retorna uma lista de dicionários

# Anota feriados/festivais no calendário
def anotar_feriados(calendario, eventos_df):
    for dia in calendario:
        evento = eventos_df[
            (eventos_df["estacao"] == dia["estacao"]) & #verifica feriados de mesma estação
            (eventos_df["dia_festival"] == dia["dia"])# verifica feriado do mesmo dia do mês
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
            dia["obs"] = None
    return calendario

# Filtra cultivos por uma ou duas estações
def cultivos_duas_estacoes(metricas, cultivos_df):
    estacao_ini = metricas["estacao_ini"].strip().lower()
    estacao_fim = metricas["estacao_fim"].strip().lower()

    def cresce_na_estacao(estacao_cultivo, estacao_verificar):#função interna
        estacoes = [e.strip().lower() for e in estacao_cultivo.split(",")]
        return estacao_verificar in estacoes

    # Mesma estação
    if estacao_ini == estacao_fim:
        plantas_disponiveis = cultivos_df[
            cultivos_df["estacao"].apply(lambda x: cresce_na_estacao(x, estacao_ini))
        ]
        return {"mesma_estacao": plantas_disponiveis}

    # Estações diferentes
    plantas_ambas = cultivos_df[
        cultivos_df["estacao"].apply(
            lambda x: cresce_na_estacao(x, estacao_ini) and cresce_na_estacao(x, estacao_fim)
        )
    ]
    if not plantas_ambas.empty:
        return {"crescem_nas_duas": plantas_ambas}

    # Se não houver plantas nas duas, retorna separadamente
    plantas_ini = cultivos_df[
        cultivos_df["estacao"].apply(lambda x: cresce_na_estacao(x, estacao_ini))
    ]
    plantas_fim = cultivos_df[
        cultivos_df["estacao"].apply(lambda x: cresce_na_estacao(x, estacao_fim))
    ]
    return {"estacao_ini": plantas_ini, "estacao_fim": plantas_fim}

