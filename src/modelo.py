import pandas as pd

#======================================
# Funções de limpesa e leitura de csv
#======================================
def carregar_cultivos(caminho=r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\data\Cultivos.csv"):
    df = pd.read_csv(caminho, sep=";")

    # Remove espaços e tabulações das colunas de texto
    # Loop que pega as colunas chamadas do tipo objeto (em pandas objeto são colunas d texto) no pandas e usa a função de limpeza
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].str.strip() # strip é função de limpeza

    # Converte campos numéricos corretamente para int ou float (usando to_numeric) e se houver erro d correção ele transforma em nan com (errors)
    df["dias_cresc"] = pd.to_numeric(df["dias_cresc"], errors="coerce")
    df["intervalo_colheita"] = pd.to_numeric(df["intervalo_colheita"], errors="coerce")
    df["preco_semente"] = pd.to_numeric(df["preco_semente"], errors="coerce")
    df["preco_venda"] = pd.to_numeric(df["preco_venda"], errors="coerce")

    return df

def carregar_eventos(caminho=r"F:\Visual Studio Code\Workspace\Github Projetos\Stardew project\data\Estações e Festivais.csv"):
    df = pd.read_csv(caminho, sep=";")

    # Remove espaços e tabulações das colunas de texto
    # Loop que pega as colunas chamadas do tipo objeto (em pandas objeto são colunas d texto) no pandas e usa a função de limpeza
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].astype(str).str.strip()

    # Converte campos numéricos corretamente para int ou float (usando to_numeric) e se houver erro d correção ele transforma em nan com (errors)
    df["dia_festival"] = pd.to_numeric(df["dia_festival"], errors="coerce").astype("Int64")

    return df
#=====================================
# Funções de limpesa e leitura de csv
#=====================================


#===============================
#Função de criação de calendário 
#===============================
def criar_calendario(estacao):
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    calendario = []
    for dia in range(1, 29):
        dia_semana = dias_semana[(dia - 1) % 7]
        calendario.append({
            "estacao": estacao,
            "dia": dia,
            "dia_semana": dia_semana
        })
    return calendario
#===============================
#Função de criação de calendário 
#===============================


#===============================
#Função anota feriados
#===============================
def anotar_feriados(calendario, eventos_df):
    for dia in calendario:
        evento = eventos_df[
            (eventos_df["estacao"] == dia["estacao"]) &
            (eventos_df["dia_festival"] == dia["dia"])
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

    return calendario  # retorna o calendário modificado

#===============================
#Função anota feriados
#===============================

#===============================
#Função de cultivo
#===============================
def plantas_por_estacao(cultivos_df, estacao):
    df_filtrado = cultivos_df[cultivos_df["estacao"] == estacao]
    return df_filtrado["cultivo"].tolist()

#===============================
#Função de cultivo
#===============================


eventos_df = carregar_eventos()
cultivos_df = carregar_cultivos()

# Cria o calendário completo (4 estações x 28 dias)
todas_estacoes = ["Primavera", "Verão", "Outono", "Inverno"]
calendario_completo = []

for est in todas_estacoes:
    calendario_completo += criar_calendario(est)

calendario_completo = anotar_feriados(calendario_completo, eventos_df)


from metricas_input import metrica_obg

metricas = metrica_obg()

# Agora você pode usar o retorno
print("Métricas coletadas:")
print(f"Estação: {metricas['estacao']}")
print(f"Dias restantes: {metricas['dias_restantes']}")





