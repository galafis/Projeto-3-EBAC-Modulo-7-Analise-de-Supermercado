# DASHBOARD STREAMLIT E DASH - EBAC - PROJETO FINAL MÓDULO 7

import pandas as pd
import plotly.express as px
import streamlit as st
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

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

# --- DASH APP ---
def run_dash():
    dash_app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    dash_app.layout = dbc.Container([
        html.H1("Dashboard Supermercado - Dash"),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='categoria-dropdown',
                    options=[{'label': c, 'value': c} for c in sorted(df['Categoria'].dropna().unique())],
                    placeholder="Selecione uma categoria"
                ),
                dcc.Graph(id='bar-categoria')
            ], width=6),
            dbc.Col([
                dcc.Graph(id='box-preco')
            ], width=6)
        ]),
        dbc.Row([
            html.H3("Top 10 Descontos"),
            html.Div(id='tabela-descontos')
        ])
    ])

    @dash_app.callback(
        Output('bar-categoria', 'figure'),
        Output('box-preco', 'figure'),
        Output('tabela-descontos', 'children'),
        Input('categoria-dropdown', 'value')
    )
    def update_dash(categoria):
        dff = df[df['Categoria'] == categoria] if categoria else df

        bar_fig = px.bar(dff['Categoria'].value_counts().reset_index(), x='index', y='Categoria',
                         labels={'index': 'Categoria', 'Categoria': 'Quantidade'})

        box_fig = px.box(dff[dff['Preco_Normal'] > 0], y='Preco_Normal', points="outliers")

        top10 = dff.sort_values(by="Desconto", ascending=False).head(10)
        table = dbc.Table.from_dataframe(top10[['title', 'Marca', 'Preco_Normal', 'Desconto']], striped=True, bordered=True, hover=True)

        return bar_fig, box_fig, table

    return dash_app

# Escolha do modo de execução
if __name__ == '__main__':
    # Para executar Streamlit, use: streamlit run dashboard_supermercado.py
    # Para executar Dash, chame run_dash().run_server(debug=True)
    pass
