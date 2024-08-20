#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar os dados da planilha
df = pd.read_excel('Case 2 - Base de Dados.xlsx', sheet_name='Lojas')

# Calcular métricas adicionais
df["Receita/m²"] = df["Receita Bruta 2023"] / df["Área da loja (m²)"]
df["EBITDA/m²"] = df["EBITDA 2023"] / df["Área da loja (m²)"]
df["Receita/habitante"] = df["Receita Bruta 2023"] / df["População"]
df["EBITDA/habitante"] = df["EBITDA 2023"] / df["População"]

# Configurar a interface do Streamlit
st.title("Análise de Lojas e Cidades")

# Seletor de cidades e lojas (fora das abas)
cidades_selecionadas = st.multiselect('Selecione as Cidades:', options=df['Cidade'].unique(), key='cidades_selecionadas')
lojas_disponiveis = df[df['Cidade'].isin(cidades_selecionadas)]['Loja'].unique() if cidades_selecionadas else df['Loja'].unique()
lojas_selecionadas = st.multiselect('Selecione as Lojas:', options=lojas_disponiveis, key='lojas_visualizacao')

# Criar abas para separar as funcionalidades
tab1, tab2 = st.tabs(["Visualização e Comparação", "Ordenação por Desempenho"])

with tab1:
    st.header("Visualização e Comparação Direta")
    
    if not lojas_selecionadas:
        st.subheader("Resultados Agregados por Cidade")

        receita_por_ano_cidade = df[df['Cidade'].isin(cidades_selecionadas)].groupby('Cidade')[['Receita Bruta 2018', 'Receita Bruta 2019', 'Receita Bruta 2020',
                                                                                                 'Receita Bruta 2021', 'Receita Bruta 2022', 'Receita Bruta 2023']].sum()
        ebitda_por_ano_cidade = df[df['Cidade'].isin(cidades_selecionadas)].groupby('Cidade')[['EBITDA 2021', 'EBITDA 2022', 'EBITDA 2023']].sum()
        area_total_cidade = df[df['Cidade'].isin(cidades_selecionadas)].groupby('Cidade')['Área da loja (m²)'].sum()
        populacao_total_cidade = df[df['Cidade'].isin(cidades_selecionadas)].groupby('Cidade')['População'].first()

        receita_por_habitante = receita_por_ano_cidade.div(populacao_total_cidade, axis=0).T
        ebitda_por_habitante = ebitda_por_ano_cidade.div(populacao_total_cidade, axis=0).T
        receita_por_m2_cidade = receita_por_ano_cidade.div(area_total_cidade, axis=0).T
        ebitda_por_m2_cidade = ebitda_por_ano_cidade.div(area_total_cidade, axis=0).T

        # Renomear corretamente os índices para exibir apenas o ano
        receita_por_habitante.index = receita_por_habitante.index.str[-4:]
        ebitda_por_habitante.index = ebitda_por_habitante.index.str[-4:]
        receita_por_m2_cidade.index = receita_por_m2_cidade.index.str[-4:]
        ebitda_por_m2_cidade.index = ebitda_por_m2_cidade.index.str[-4:]

        # Renomear as colunas das tabelas calculadas
        receita_por_habitante.columns = [f"Receita/habitante {cidade}" for cidade in receita_por_habitante.columns]
        ebitda_por_habitante.columns = [f"EBITDA/habitante {cidade}" for cidade in ebitda_por_habitante.columns]
        receita_por_m2_cidade.columns = [f"Receita/m² {cidade}" for cidade in receita_por_m2_cidade.columns]
        ebitda_por_m2_cidade.columns = [f"EBITDA/m² {cidade}" for cidade in ebitda_por_m2_cidade.columns]

        # Tabelas e gráficos

        st.write("### Receita Bruta por Cidade")
        st.dataframe(receita_por_ano_cidade.T.rename_axis("Ano", axis=1), use_container_width=True)
        fig_receita_cidade = px.bar(receita_por_ano_cidade.T, title='Receita Bruta por Cidade', barmode='group')
        st.plotly_chart(fig_receita_cidade, use_container_width=True)

        st.write("### EBITDA Bruto por Cidade")
        st.dataframe(ebitda_por_ano_cidade.T.rename_axis("Ano", axis=1), use_container_width=True)
        fig_ebitda_cidade = px.bar(ebitda_por_ano_cidade.T, title='EBITDA Bruto por Cidade', barmode='group')
        st.plotly_chart(fig_ebitda_cidade, use_container_width=True)

        st.write("### Receita/habitante por Cidade")
        st.dataframe(receita_por_habitante.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_hab_cidade = px.bar(receita_por_habitante, title='Receita/habitante por Cidade', barmode='group')
        st.plotly_chart(fig_receita_hab_cidade, use_container_width=True)

        st.write("### EBITDA/habitante por Cidade")
        st.dataframe(ebitda_por_habitante.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_hab_cidade = px.bar(ebitda_por_habitante, title='EBITDA/habitante por Cidade', barmode='group')
        st.plotly_chart(fig_ebitda_hab_cidade, use_container_width=True)

        st.write("### Receita/m² por Cidade")
        st.dataframe(receita_por_m2_cidade.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_m2_cidade = px.bar(receita_por_m2_cidade, title='Receita/m² por Cidade', barmode='group')
        st.plotly_chart(fig_receita_m2_cidade, use_container_width=True)

        st.write("### EBITDA/m² por Cidade")
        st.dataframe(ebitda_por_m2_cidade.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_m2_cidade = px.bar(ebitda_por_m2_cidade, title='EBITDA/m² por Cidade', barmode='group')
        st.plotly_chart(fig_ebitda_m2_cidade, use_container_width=True)

    else:
        st.subheader("Métricas de Eficiência por Loja")

        df_filtrado = df[df['Loja'].isin(lojas_selecionadas)]

        receita_bruta_por_ano = df_filtrado.groupby(['Loja'])[['Receita Bruta 2018', 'Receita Bruta 2019', 'Receita Bruta 2020',
                                                               'Receita Bruta 2021', 'Receita Bruta 2022', 'Receita Bruta 2023']].sum().T
        ebitda_por_ano = df_filtrado.groupby(['Loja'])[['EBITDA 2021', 'EBITDA 2022', 'EBITDA 2023']].sum().T
        area_total_loja = df_filtrado.groupby('Loja')['Área da loja (m²)'].first()
        populacao_total_loja = df_filtrado.groupby('Loja')['População'].first()

        receita_por_habitante_loja = receita_bruta_por_ano.div(populacao_total_loja, axis=1)
        ebitda_por_habitante_loja = ebitda_por_ano.div(populacao_total_loja, axis=1)
        receita_por_m2_loja = receita_bruta_por_ano.div(area_total_loja, axis=1)
        ebitda_por_m2_loja = ebitda_por_ano.div(area_total_loja, axis=1)

        # Renomear corretamente os índices para exibir apenas o ano
        receita_por_habitante_loja.index = receita_por_habitante_loja.index.str[-4:]
        ebitda_por_habitante_loja.index = ebitda_por_habitante_loja.index.str[-4:]
        receita_por_m2_loja.index = receita_por_m2_loja.index.str[-4:]
        ebitda_por_m2_loja.index = ebitda_por_m2_loja.index.str[-4:]

        # Renomear as colunas das tabelas calculadas
        receita_por_habitante_loja.columns = [f"Receita/habitante {loja}" for loja in receita_por_habitante_loja.columns]
        ebitda_por_habitante_loja.columns = [f"EBITDA/habitante {loja}" for loja in ebitda_por_habitante_loja.columns]
        receita_por_m2_loja.columns = [f"Receita/m² {loja}" for loja in receita_por_m2_loja.columns]
        ebitda_por_m2_loja.columns = [f"EBITDA/m² {loja}" for loja in ebitda_por_m2_loja.columns]

        # Tabelas e gráficos

        st.write("### Receita Bruta por Loja")
        st.dataframe(receita_bruta_por_ano.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_loja = px.bar(receita_bruta_por_ano, title='Receita Bruta por Loja', barmode='group')
        st.plotly_chart(fig_receita_loja, use_container_width=True)

        st.write("### EBITDA Bruto por Loja")
        st.dataframe(ebitda_por_ano.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_loja = px.bar(ebitda_por_ano, title='EBITDA Bruto por Loja', barmode='group')
        st.plotly_chart(fig_ebitda_loja, use_container_width=True)

        st.write("### Receita/habitante por Loja")
        st.dataframe(receita_por_habitante_loja.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_hab_loja = px.bar(receita_por_habitante_loja, title='Receita/habitante por Loja', barmode='group')
        st.plotly_chart(fig_receita_hab_loja, use_container_width=True)

        st.write("### EBITDA/habitante por Loja")
        st.dataframe(ebitda_por_habitante_loja.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_hab_loja = px.bar(ebitda_por_habitante_loja, title='EBITDA/habitante por Loja', barmode='group')
        st.plotly_chart(fig_ebitda_hab_loja, use_container_width=True)

        st.write("### Receita/m² por Loja")
        st.dataframe(receita_por_m2_loja.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_m2_loja = px.bar(receita_por_m2_loja, title='Receita/m² por Loja', barmode='group')
        st.plotly_chart(fig_receita_m2_loja, use_container_width=True)

        st.write("### EBITDA/m² por Loja")
        st.dataframe(ebitda_por_m2_loja.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_m2_loja = px.bar(ebitda_por_m2_loja, title='EBITDA/m² por Loja', barmode='group')
        st.plotly_chart(fig_ebitda_m2_loja, use_container_width=True)

with tab2:
    st.header("Ordenação por Desempenho")
    
    # Seletor de Métrica para Classificação
    st.subheader("Classificação das Lojas/Cidades por Métrica")
    metric = st.selectbox("Selecione a métrica para classificação:", [
        "Receita Bruta 2023", "EBITDA 2023", 
        "Receita/m²", "EBITDA/m²", 
        "Receita/habitante", "EBITDA/habitante"
    ], key='metric_selection')
    ordem = st.selectbox("Ordem de classificação:", ["Crescente", "Decrescente"], key='order_selection')

    # Classificar e exibir
    df_sorted = df.sort_values(by=[metric], ascending=(ordem == "Crescente"))
    st.write(f"Ranking das lojas/cidades baseado em {metric}:")
    st.dataframe(df_sorted[['Loja', 'Cidade', metric]])

    # Análise Comparativa Automática
    st.subheader("Análise Comparativa Automática")
    for loja in lojas_selecionadas:
        loja_data = df[df["Loja"] == loja]
        receita_media = df["Receita Bruta 2023"].mean()
        ebitda_media = df["EBITDA 2023"].mean()
        receita_por_m2_media = df["Receita/m²"].mean()
        ebitda_por_m2_media = df["EBITDA/m²"].mean()
        receita_por_hab_media = df["Receita/habitante"].mean()
        ebitda_por_hab_media = df["EBITDA/habitante"].mean()

        analise = f"Análise da loja {loja}: "
        if loja_data["Receita Bruta 2023"].iloc[0] > receita_media:
            analise += "Receita maior do que a média. "
        else:
            analise += "Receita menor do que a média. "

        if loja_data["EBITDA 2023"].iloc[0] > ebitda_media:
            analise += "EBITDA maior do que a média. "
        else:
            analise += "EBITDA menor do que a média. "

        if loja_data["Receita/m²"].iloc[0] > receita_por_m2_media:
            analise += "Receita/m² maior do que a média. "
        else:
            analise += "Receita/m² menor do que a média. "

        if loja_data["EBITDA/m²"].iloc[0] > ebitda_por_m2_media:
            analise += "EBITDA/m² maior do que a média. "
        else:
            analise += "EBITDA/m² menor do que a média. "

        if loja_data["Receita/habitante"].iloc[0] > receita_por_hab_media:
            analise += "Receita/habitante maior do que a média. "
        else:
            analise += "Receita/habitante menor do que a média. "

        if loja_data["EBITDA/habitante"].iloc[0] > ebitda_por_hab_media:
            analise += "EBITDA/habitante maior do que a média. "
        else:
            analise += "EBITDA/habitante menor do que a média. "

        if loja_data["Receita Bruta 2023"].iloc[0] > loja_data["Receita Bruta 2022"].iloc[0]:
            analise += "Receita crescente. "
        else:
            analise += "Receita decrescente. "

        st.write(analise)

