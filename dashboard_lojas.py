#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar os dados da planilha
df = pd.read_excel('Case 2 - Base de Dados.xlsx', sheet_name='Lojas')

# Configurar a interface do Streamlit
st.title("Hipotético Mercados")

# Checklist para selecionar as cidades
cidades_selecionadas = st.multiselect(
    'Selecione as Cidades:',
    options=df['Cidade'].unique()
)

# Filtrar lojas com base nas cidades selecionadas
if cidades_selecionadas:
    lojas_disponiveis = df[df['Cidade'].isin(cidades_selecionadas)]['Loja'].unique()
    lojas_selecionadas = st.multiselect(
        'Selecione as Lojas:',
        options=lojas_disponiveis
    )

    if not lojas_selecionadas:
        st.subheader("Resumo da Cidade")

        # Resumo da cidade
        num_lojas = df[df['Cidade'].isin(cidades_selecionadas)]['Loja'].nunique()
        area_total_lojas = df[df['Cidade'].isin(cidades_selecionadas)]['Área da loja (m²)'].sum()
        tamanho_cidade = df[df['Cidade'].isin(cidades_selecionadas)]['Tamanho cidade(Quilômetros quadrados)'].max()
        populacao_cidade = df[df['Cidade'].isin(cidades_selecionadas)]['População'].max()

        st.write(f"**Número total de lojas:** {num_lojas}")
        st.write(f"**Área total das lojas:** {area_total_lojas:.2f} m²")
        st.write(f"**Tamanho da cidade:** {tamanho_cidade:.2f} km²")
        st.write(f"**Número de habitantes da cidade:** {populacao_cidade}")

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
        st.subheader("Resumo da Loja")

        # Resumo da loja
        tamanho_loja = df[df['Loja'].isin(lojas_selecionadas)]['Tamanho cidade(Quilômetros quadrados)'].unique()[0]
        area_loja = df[df['Loja'].isin(lojas_selecionadas)]['Área da loja (m²)'].unique()[0]
        populacao_loja = df[df['Loja'].isin(lojas_selecionadas)]['População'].unique()[0]

        st.write(f"**Tamanho da cidade:** {tamanho_loja:.2f} km²")
        st.write(f"**Área da loja:** {area_loja:.2f} m²")
        st.write(f"**Número de habitantes da cidade:** {populacao_loja}")

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

