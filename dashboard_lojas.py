#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados das planilhas "Lojas" e "Cidades"
df_lojas = pd.read_excel('Case 2 - Base de Dados.xlsx', sheet_name='Lojas')
df_cidades = pd.read_excel('Case 2 - Base de Dados.xlsx', sheet_name='Cidades')

# Configurar a interface do Streamlit
st.title("Hipotético Mercados")

# Criar abas para separar as funçoes
tab1, tab2 = st.tabs(["Visualização e Comparação", "Ordenação por Desempenho"])

with tab1:
    st.header("Visualização e Comparação Direta")
    
    # Seleção de cidades
    cidades_selecionadas = st.multiselect('Selecione as Cidades:', options=list(df_cidades['CIDADES'].unique()), key='cidades_selecionadas')
    # Filtrar lojas disponíveis com base nas cidades selecionadas
    lojas_disponiveis = df_lojas[df_lojas['Cidade'].isin(cidades_selecionadas)]['Loja'].unique()
    # Seleção de lojas
    lojas_selecionadas = st.multiselect('Selecione as Lojas:', options=lojas_disponiveis, key='lojas_visualizacao')

    # Tabela de Resum
    st.subheader("Resumo das Cidades ou Lojas Selecionadas")
    
    if not lojas_selecionadas:
        # Resumo por Cidades
        resumo_cidades = df_cidades[df_cidades['CIDADES'].isin(cidades_selecionadas)].set_index('CIDADES')[['Habitantes', 'Área da loja (m²)']]
        # Adicionando a contagem de lojas para cada cidade
        resumo_cidades['Número de Lojas'] = df_lojas[df_lojas['Cidade'].isin(cidades_selecionadas)].groupby('Cidade').size()
        st.dataframe(resumo_cidades.T.rename_axis("Informação", axis=0), use_container_width=True)
    else:
        # Resumo por Lojas
        resumo_lojas = df_lojas[df_lojas['Loja'].isin(lojas_selecionadas)].set_index('Loja')[['População', 'Área da loja (m²)', 'Tamanho cidade(Quilômetros quadrados)']]
        st.dataframe(resumo_lojas.T.rename_axis("Informação", axis=0), use_container_width=True)
    
    # Visualização por cidade
    if not lojas_selecionadas:
        st.subheader("Resultados por Cidade")

        # Filtrar os dados para as cidades selecionadas
        df_filtrado = df_cidades[df_cidades['CIDADES'].isin(cidades_selecionadas)]

        st.write("### Receita Bruta por Cidade")
        receita_por_ano_cidade = df_filtrado[['CIDADES'] + [col for col in df_cidades.columns if 'Receita Bruta' in col]].set_index('CIDADES').T
        st.dataframe(receita_por_ano_cidade.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_cidade = px.bar(receita_por_ano_cidade, title='Receita Bruta por Cidade', barmode='group')
        st.plotly_chart(fig_receita_cidade, use_container_width=True)

        st.write("### EBITDA Bruto por Cidade")
        ebitda_por_ano_cidade = df_filtrado[['CIDADES'] + [col for col in df_cidades.columns if 'EBITDA' in col and not 'habitante' in col and not 'm2' in col and not 'Margem' in col]].set_index('CIDADES').T
        st.dataframe(ebitda_por_ano_cidade.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_cidade = px.bar(ebitda_por_ano_cidade, title='EBITDA Bruto por Cidade', barmode='group')
        st.plotly_chart(fig_ebitda_cidade, use_container_width=True)

        st.write("### Margem EBITDA por Cidade")
        margem_ebitda_cidade = df_filtrado[['CIDADES'] + [col for col in df_cidades.columns if 'Margem EBITDA' in col]].set_index('CIDADES').T
        st.dataframe(margem_ebitda_cidade.rename_axis("Ano", axis=0), use_container_width=True)
        fig_margem_ebitda_cidade = px.bar(margem_ebitda_cidade, title='Margem EBITDA por Cidade', barmode='group')
        st.plotly_chart(fig_margem_ebitda_cidade, use_container_width=True)

        st.write("### Receita/habitante por Cidade")
        receita_hab_cidade = df_filtrado[['CIDADES'] + [col for col in df_cidades.columns if 'Receita/habitante' in col]].set_index('CIDADES').T
        st.dataframe(receita_hab_cidade.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_hab_cidade = px.bar(receita_hab_cidade, title='Receita/habitante por Cidade', barmode='group')
        st.plotly_chart(fig_receita_hab_cidade, use_container_width=True)

        st.write("### EBITDA/habitante por Cidade")
        ebitda_hab_cidade = df_filtrado[['CIDADES'] + [col for col in df_cidades.columns if 'EBITDA/habitante' in col]].set_index('CIDADES').T
        st.dataframe(ebitda_hab_cidade.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_hab_cidade = px.bar(ebitda_hab_cidade, title='EBITDA/habitante por Cidade', barmode='group')
        st.plotly_chart(fig_ebitda_hab_cidade, use_container_width=True)

        st.write("### Receita/m² por Cidade")
        receita_m2_cidade = df_filtrado[['CIDADES'] + [col for col in df_cidades.columns if 'Receita/m2' in col]].set_index('CIDADES').T
        st.dataframe(receita_m2_cidade.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_m2_cidade = px.bar(receita_m2_cidade, title='Receita/m² por Cidade', barmode='group')
        st.plotly_chart(fig_receita_m2_cidade, use_container_width=True)

        st.write("### EBITDA/m² por Cidade")
        ebitda_m2_cidade = df_filtrado[['CIDADES'] + [col for col in df_cidades.columns if 'EBITDA/m2' in col]].set_index('CIDADES').T
        st.dataframe(ebitda_m2_cidade.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_m2_cidade = px.bar(ebitda_m2_cidade, title='EBITDA/m² por Cidade', barmode='group')
        st.plotly_chart(fig_ebitda_m2_cidade, use_container_width=True)

    # Visualização por loja
    else:
        st.subheader("Métricas de Eficiência por Loja")

        df_filtrado = df_lojas[df_lojas['Loja'].isin(lojas_selecionadas)]

        st.write("### Receita Bruta por Loja")
        receita_bruta_por_ano = df_filtrado[['Loja'] + [col for col in df_lojas.columns if 'Receita Bruta' in col]].set_index('Loja').T
        st.dataframe(receita_bruta_por_ano.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_loja = px.bar(receita_bruta_por_ano, title='Receita Bruta por Loja', barmode='group')
        st.plotly_chart(fig_receita_loja, use_container_width=True)

        st.write("### EBITDA Bruto por Loja")
        ebitda_por_ano = df_filtrado[['Loja'] + [col for col in df_lojas.columns if 'EBITDA' in col and not 'habitante' in col and not 'm2' in col and not 'Margem' in col]].set_index('Loja').T
        st.dataframe(ebitda_por_ano.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_loja = px.bar(ebitda_por_ano, title='EBITDA Bruto por Loja', barmode='group')
        st.plotly_chart(fig_ebitda_loja, use_container_width=True)

        st.write("### Margem EBITDA por Loja")
        margem_ebitda_loja = df_filtrado[['Loja'] + [col for col in df_lojas.columns if 'Margem EBITDA' in col]].set_index('Loja').T
        st.dataframe(margem_ebitda_loja.rename_axis("Ano", axis=0), use_container_width=True)
        fig_margem_ebitda_loja = px.bar(margem_ebitda_loja, title='Margem EBITDA por Loja', barmode='group')
        st.plotly_chart(fig_margem_ebitda_loja, use_container_width=True)

        st.write("### Receita/habitante por Loja")
        receita_hab_loja = df_filtrado[['Loja'] + [col for col in df_lojas.columns if 'Receita/habitante' in col]].set_index('Loja').T
        st.dataframe(receita_hab_loja.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_hab_loja = px.bar(receita_hab_loja, title='Receita/habitante por Loja', barmode='group')
        st.plotly_chart(fig_receita_hab_loja, use_container_width=True)

        st.write("### EBITDA/habitante por Loja")
        ebitda_hab_loja = df_filtrado[['Loja'] + [col for col in df_lojas.columns if 'EBITDA/habitante' in col]].set_index('Loja').T
        st.dataframe(ebitda_hab_loja.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_hab_loja = px.bar(ebitda_hab_loja, title='EBITDA/habitante por Loja', barmode='group')
        st.plotly_chart(fig_ebitda_hab_loja, use_container_width=True)

        st.write("### Receita/m² por Loja")
        receita_m2_loja = df_filtrado[['Loja'] + [col for col in df_lojas.columns if 'Receita/m2' in col]].set_index('Loja').T
        st.dataframe(receita_m2_loja.rename_axis("Ano", axis=0), use_container_width=True)
        fig_receita_m2_loja = px.bar(receita_m2_loja, title='Receita/m² por Loja', barmode='group')
        st.plotly_chart(fig_receita_m2_loja, use_container_width=True)

        st.write("### EBITDA/m² por Loja")
        ebitda_m2_loja = df_filtrado[['Loja'] + [col for col in df_lojas.columns if 'EBITDA/m2' in col]].set_index('Loja').T
        st.dataframe(ebitda_m2_loja.rename_axis("Ano", axis=0), use_container_width=True)
        fig_ebitda_m2_loja = px.bar(ebitda_m2_loja, title='EBITDA/m² por Loja', barmode='group')
        st.plotly_chart(fig_ebitda_m2_loja, use_container_width=True)

with tab2:
    st.header("Ordenação por Desempenho")

    # seleção para escolher entre Lojas e Cidades
    tipo_selecao = st.selectbox("Deseja classificar por:", ["Lojas", "Cidades"], key='tipo_selecao')

    # Seletor de ano
    ano_selecionado = st.selectbox("Selecione o ano:", [2018, 2019, 2020, 2021, 2022, 2023], key='ano_selection')
    
    # Ajustar as métricas disponíveis com base no ano selecionado e na escolha entre lojas ou cidades
    if tipo_selecao == "Lojas":
        if ano_selecionado in [2018, 2019, 2020]:
            metric_options = [
                f"Receita Bruta {ano_selecionado}",
                f"Receita/m2 {ano_selecionado}",
                f"Receita/habitante {ano_selecionado}",
            ]
        else:
            metric_options = [
                f"Receita Bruta {ano_selecionado}",
                f"EBITDA {ano_selecionado}",
                f"Receita/m2 {ano_selecionado}",
                f"EBITDA/m2 {ano_selecionado}",
                f"Receita/habitante {ano_selecionado}",
                f"EBITDA/habitante {ano_selecionado}",
                f"Margem EBITDA {ano_selecionado}"
            ]
    else:  
        if ano_selecionado in [2018, 2019, 2020]:
            metric_options = [
                f"Receita Bruta {ano_selecionado}",
                f"Receita/m2 {ano_selecionado}",
                f"Receita/habitante {ano_selecionado}",
            ]
        else:
            metric_options = [
                f"Receita Bruta {ano_selecionado}",
                f"EBITDA {ano_selecionado}",
                f"Receita/m2 {ano_selecionado}",
                f"EBITDA/m2 {ano_selecionado}",
                f"Receita/habitante {ano_selecionado}",
                f"EBITDA/habitante {ano_selecionado}",
                f"Margem EBITDA {ano_selecionado}"
            ]
    
    metric = st.selectbox("Selecione a métrica para classificação:", metric_options, key='metric_selection')
    ordem = st.selectbox("Ordem de classificação:", ["Crescente", "Decrescente"], key='order_selection')

    # Classificar e exibir
    if tipo_selecao == "Lojas":
        df_sorted = df_lojas.sort_values(by=[metric], ascending=(ordem == "Crescente"))
        st.write(f"Ranking das lojas baseado em {metric}:")
        st.dataframe(df_sorted[['Loja', 'Cidade', metric]])
        fig_ranking_lojas = px.bar(df_sorted, x=metric, y='Loja', title=f"Ranking das Lojas por {metric}", orientation='h', height=800)
        st.plotly_chart(fig_ranking_lojas, use_container_width=True)
    else:  # Cidades
        # Remover a linha TOTAL antes de ordenar
        df_sorted = df_cidades[df_cidades['CIDADES'] != 'TOTAL']
        df_sorted = df_sorted.sort_values(by=[metric], ascending=(ordem == "Crescente"))
        st.write(f"Ranking das cidades baseado em {metric}:")
        st.dataframe(df_sorted[['CIDADES', metric]])
        fig_ranking_cidades = px.bar(df_sorted, x=metric, y='CIDADES', title=f"Ranking das Cidades por {metric}", orientation='h', height=800)
        st.plotly_chart(fig_ranking_cidades, use_container_width=True)

