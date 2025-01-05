import pandas as pd
import streamlit as st


@st.cache_data
def carregar_dados(data_url: str) -> pd.DataFrame:
    """Carrega e processa os dados do CSV."""
    try:
        dados = pd.read_csv(data_url)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Arquivo não encontrado: {data_url}") from e
    except Exception as e:
        raise Exception(f"Erro ao carregar o arquivo: {e}") from e
    else:
        return dados.assign(
            data_venda=lambda df: pd.to_datetime(df["data_venda"], dayfirst=True),
            mes=lambda df: df["data_venda"].dt.month,
            ano=lambda df: df["data_venda"].dt.year,
        )


def calcular_receitas_por_cidade(
    dados: pd.DataFrame, ano_selecionado: int
) -> pd.DataFrame:
    """Calcula receitas totais por cidade e ano, além da variação percentual."""
    receitas = dados.groupby(["cidade", "ano"])["valor_venda"].sum().unstack()

    # Calcular a variação percentual com base no ano selecionado e no ano anterior
    if ano_selecionado - 1 in receitas.columns:
        receitas["variacao"] = (
            (receitas[ano_selecionado] - receitas[ano_selecionado - 1])
            / receitas[ano_selecionado - 1]
            * 100
        )
    else:
        # Se não houver ano anterior disponível, não calcula a variação
        receitas["variacao"] = None

    return receitas


def filtrar_dados(dados: pd.DataFrame, cidade: str, ano: int) -> pd.DataFrame:
    """Filtra os dados com base na cidade e no ano selecionados."""
    return dados.query("cidade == @cidade & ano == @ano")
