import streamlit as st
import pandas as pd
import altair as alt

def configurar_pagina():
    """Configurações iniciais da página do Streamlit."""
    st.set_page_config(page_title="Painel de Vendas", page_icon="📊")
    st.title("Painel de Vendas")
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def exibir_metricas(receitas: pd.DataFrame, cidades: list[str], ano: int):
    """Exibe as métricas principais por cidade."""
    colunas = st.columns(len(cidades))
    for coluna, cidade in zip(colunas, cidades):
        with coluna:
            # Verifica se a variação está disponível (não é None)
            variacao = receitas.loc[cidade, "variacao"]
            if variacao is None:
                delta_text = "Sem variação disponível"
            else:
                delta_text = f"{variacao:.2f}% vs. Último ano"

            # Exibe a métrica
            st.metric(
                label=cidade,
                value=f"R$ {receitas.loc[cidade, ano]:,.2f}",
                delta=delta_text,
            )


def exibir_graficos(dados_filtrados: pd.DataFrame):
    """Exibe gráficos em abas para análise mensal e por categoria."""
    aba_mensal, aba_categoria = st.tabs(["Análise Mensal", "Análise por Categoria"])

    # Gráfico de Análise Mensal
    with aba_mensal:
        dados_filtrados["mes_nome"] = dados_filtrados["mes"].map(
            {
                1: "Janeiro",
                2: "Fevereiro",
                3: "Março",
                4: "Abril",
                5: "Maio",
                6: "Junho",
                7: "Julho",
                8: "Agosto",
                9: "Setembro",
                10: "Outubro",
                11: "Novembro",
                12: "Dezembro",
            }
        )
        mensal = dados_filtrados.groupby("mes_nome", as_index=False)[
            "valor_venda"
        ].sum()

        grafico_mensal = (
            alt.Chart(mensal)
            .mark_bar()
            .encode(
                x=alt.X(
                    "mes_nome:N",
                    sort=[
                        "Janeiro",
                        "Fevereiro",
                        "Março",
                        "Abril",
                        "Maio",
                        "Junho",
                        "Julho",
                        "Agosto",
                        "Setembro",
                        "Outubro",
                        "Novembro",
                        "Dezembro",
                    ],
                    title="Mês",
                    axis=alt.Axis(labelAngle=-45),
                ),
                y=alt.Y("valor_venda:Q", title="Valor Vendido (R$)"),
                tooltip=["mes_nome", "valor_venda"],
            )
            .properties(width=700, height=400, title="Vendas Mensais")
        )

        st.altair_chart(grafico_mensal, use_container_width=True)

    # Gráfico de Análise por Categoria
    with aba_categoria:
        categoria = dados_filtrados.groupby("categoria_produto", as_index=False)[
            "valor_venda"
        ].sum()

        grafico_categoria = (
            alt.Chart(categoria)
            .mark_bar()
            .encode(
                x=alt.X(
                    "categoria_produto:N",
                    title="Categoria do Produto",
                    sort=None,
                    axis=alt.Axis(labelAngle=360),
                ),
                y=alt.Y("valor_venda:Q", title="Valor Vendido (R$)"),
                color=alt.Color("categoria_produto:N", legend=None),
                tooltip=["categoria_produto", "valor_venda"],
            )
            .properties(width=700, height=400, title="Vendas por Categoria")
        )

        st.altair_chart(grafico_categoria, use_container_width=True)
