
# DASHBOARD STREAMLIT E DASH - EBAC - PROJETO FINAL MÓDULO 7

import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# Leitura dos dados
df = pd.read_csv("dados.csv")

# --- STREAMLIT APP ---
def run_streamlit():
    st.title("Análise de Produtos de Supermercado")

    st.sidebar.header("Filtros")
    categoria = st.sidebar.selectbox("Escolha a categoria", ["Todas"] + sorted(df['Categoria'].dropna().unique().tolist()))

    if categoria != "Todas":
        filtered_df = df[df['Categoria'] == categoria]
    else:
        filtered_df = df

    st.subheader("Distribuição de Produtos por Categoria")
    cat_count = filtered_df['Categoria'].value_counts().reset_index()
    fig_cat = px.bar(cat_count, x='index', y='Categoria', labels={'index': 'Categoria', 'Categoria': 'Quantidade'})
    st.plotly_chart(fig_cat)

    st.subheader("Boxplot dos Preços Normais")
    fig_box = px.box(filtered_df[filtered_df['Preco_Normal'] > 0], y='Preco_Normal', points="outliers")
    st.plotly_chart(fig_box)

    st.subheader("Top 10 Maiores Descontos")
    top_descontos = filtered_df.sort_values(by="Desconto", ascending=False).head(10)
    st.dataframe(top_descontos[['title', 'Marca', 'Preco_Normal', 'Desconto']])

    st.subheader("Análise Estatística dos Descontos por Categoria")
    stats_df = df.groupby("Categoria").agg(
        media_desc=("Desconto", "mean"),
        mediana_desc=("Desconto", "median"),
        desvio_desc=("Desconto", "std"),
        qtd=("Desconto", "count")
    ).reset_index()

    mediana_geral = stats_df["media_desc"].median()
    stats_df["acima_mediana_geral"] = stats_df["media_desc"] > mediana_geral

    st.dataframe(stats_df)

    st.markdown("### 🧠 Insights")
    acima = stats_df[stats_df["acima_mediana_geral"]]["Categoria"].tolist()
    abaixo = stats_df[~stats_df["acima_mediana_geral"]]["Categoria"].tolist()

    st.markdown(f"🔺 Categorias com média de desconto acima da mediana geral: {', '.join(acima)}")
    st.markdown(f"🔻 Categorias com média de desconto abaixo da mediana geral: {', '.join(abaixo)}")

    categoria_maior_desvio = stats_df.sort_values("desvio_desc", ascending=False).iloc[0]
    st.markdown(f"⚠️ Categoria com maior variação nos descontos: **{categoria_maior_desvio['Categoria']}** com desvio padrão de **{categoria_maior_desvio['desvio_desc']:.2f}**")

    st.warning("🌍 Mapa não incluído no projeto. Você pode adicionar uma visualização geográfica com Plotly ou Folium caso os dados contenham localização.")

# Executar o Streamlit
if __name__ == "__main__":
    run_streamlit()
