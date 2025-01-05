import streamlit as st
from model import carregar_dados, calcular_receitas_por_cidade, filtrar_dados
from view import configurar_pagina, exibir_metricas, exibir_graficos


def main():
    configurar_pagina()

    try:
        dados = carregar_dados("./data/data.csv")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return

    # Seletor de ano baseado nos dados disponíveis
    anos_disponiveis = sorted(dados["ano"].unique(), reverse=True)
    ano_selecionado = st.selectbox("Selecione o ano:", anos_disponiveis)

    # Calcular receitas por cidade para o ano selecionado
    receitas = calcular_receitas_por_cidade(dados, ano_selecionado)

    # Exibir métricas principais
    cidades = ["Rio de Janeiro", "Belo Horizonte", "São Paulo"]
    exibir_metricas(receitas, cidades, ano_selecionado)

    # Seleção de cidade
    cidade_selecionada = st.selectbox("Selecione uma cidade:", cidades)
    st.write(f"**Vendas em {ano_selecionado}**")

    # Filtrar dados e exibir gráficos
    dados_filtrados = filtrar_dados(dados, cidade_selecionada, ano_selecionado)
    if dados_filtrados.empty:
        st.warning("Sem dados disponíveis para a seleção atual.")
    else:
        exibir_graficos(dados_filtrados)
