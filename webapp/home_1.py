import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import pickle
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utilidades import (
    carregar_dados_dashboard, 
    gerar_metricas_consolidadas, 
    exibir_metricas_principais,
    criar_sidebar_dashboard
)
from src.vizualizacoes import (
    criar_grafico_distribuicao_notas,
    criar_grafico_distribuicao_cliques,
    criar_grafico_desempenho_por_genero_uci,
    criar_grafico_desempenho_por_genero_oulad,
    criar_grafico_correlacao_uci,
    criar_grafico_atividades_oulad,
    criar_grafico_faltas_vs_desempenho,
    criar_grafico_tempo_estudo_vs_desempenho,
    criar_grafico_distribuicao_idade_oulad,
    criar_grafico_resultado_final_oulad,
    criar_grafico_consumo_alcool_vs_desempenho,
    criar_grafico_escolaridade_pais_vs_desempenho,
    criar_grafico_comparativo_aprovacao
)

# Configuração da página Streamlit
st.set_page_config(
    page_title="Dashboard Educacional Consolidado", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📊 Dashboard Educacional Consolidado")
st.markdown("---")

# Carregar dados
with st.spinner("Carregando dados..."):
    df_uci, df_oulad = carregar_dados_dashboard()

# Criar sidebar
periodo, genero = criar_sidebar_dashboard()

# Verificar se os dados foram carregados
if df_uci.empty and df_oulad.empty:
    st.error("❌ Nenhum dado foi carregado. Verifique se os arquivos pickle existem.")
    st.stop()

# Gerar métricas consolidadas
metricas_consolidadas = gerar_metricas_consolidadas(df_uci, df_oulad)

# Exibir métricas principais
st.markdown("## 📈 Métricas Principais")
exibir_metricas_principais(metricas_consolidadas)

# Contexto do dashboard
st.markdown("## ℹ️ Sobre o Dashboard")
st.markdown("""
Este dashboard consolida informações de duas bases de dados educacionais públicas:

- **📚 UCI (University of California Irvine)**: Dados de estudantes de escolas públicas portuguesas, 
  incluindo informações demográficas, acadêmicas e comportamentais.

- **🌐 OULAD (Open University Learning Analytics Dataset)**: Dados de uma plataforma de 
  aprendizado online, incluindo atividades dos estudantes e resultados acadêmicos.

Essas análises ajudam gestores educacionais e professores a identificar padrões, 
fatores de sucesso e áreas que necessitam de intervenção.
""")

# Seção de visualizações
st.markdown("## 📊 Visualizações Principais")

# Tabs para organizar as visualizações
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Desempenho Geral", "👥 Demografia", "📚 Análises UCI", "🌐 Análises OULAD"])

with tab1:
    st.markdown("### Comparação de Desempenho entre Datasets")
    
    # Gráfico comparativo de aprovação
    fig_comparativo = criar_grafico_comparativo_aprovacao(df_uci, df_oulad)
    if fig_comparativo:
        st.pyplot(fig_comparativo)
        plt.clf()
    
    # Distribuições lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Distribuição de Notas (UCI)")
        fig_notas = criar_grafico_distribuicao_notas(df_uci)
        if fig_notas:
            st.pyplot(fig_notas)
            plt.clf()
    
    with col2:
        st.markdown("#### Distribuição de Cliques (OULAD)")
        fig_cliques = criar_grafico_distribuicao_cliques(df_oulad)
        if fig_cliques:
            st.pyplot(fig_cliques)
            plt.clf()

with tab2:
    st.markdown("### Análise Demográfica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Desempenho por Gênero - UCI")
        fig_genero_uci = criar_grafico_desempenho_por_genero_uci(df_uci)
        if fig_genero_uci:
            st.pyplot(fig_genero_uci)
            plt.clf()
    
    with col2:
        st.markdown("#### Resultado por Gênero - OULAD")
        fig_genero_oulad = criar_grafico_desempenho_por_genero_oulad(df_oulad)
        if fig_genero_oulad:
            st.pyplot(fig_genero_oulad)
            plt.clf()
    
    # Distribuição de idade OULAD
    st.markdown("#### Distribuição por Faixa Etária - OULAD")
    fig_idade = criar_grafico_distribuicao_idade_oulad(df_oulad)
    if fig_idade:
        st.pyplot(fig_idade)
        plt.clf()

with tab3:
    st.markdown("### Análises Detalhadas - Dataset UCI")
    
    # Faltas vs Desempenho
    st.markdown("#### Relação entre Faltas e Desempenho")
    fig_faltas = criar_grafico_faltas_vs_desempenho(df_uci)
    if fig_faltas:
        st.pyplot(fig_faltas)
        plt.clf()
    
    # Tempo de estudo vs Desempenho
    st.markdown("#### Tempo de Estudo vs Desempenho")
    fig_estudo = criar_grafico_tempo_estudo_vs_desempenho(df_uci)
    if fig_estudo:
        st.pyplot(fig_estudo)
        plt.clf()
    
    # Consumo de álcool vs Desempenho
    st.markdown("#### Consumo de Álcool vs Desempenho")
    fig_alcool = criar_grafico_consumo_alcool_vs_desempenho(df_uci)
    if fig_alcool:
        st.pyplot(fig_alcool)
        plt.clf()
    
    # Escolaridade dos pais vs Desempenho
    st.markdown("#### Escolaridade dos Pais vs Desempenho")
    fig_escolaridade = criar_grafico_escolaridade_pais_vs_desempenho(df_uci)
    if fig_escolaridade:
        st.pyplot(fig_escolaridade)
        plt.clf()
    
    # Matriz de correlação
    st.markdown("#### Matriz de Correlação")
    fig_corr = criar_grafico_correlacao_uci(df_uci)
    if fig_corr:
        st.pyplot(fig_corr)
        plt.clf()

with tab4:
    st.markdown("### Análises Detalhadas - Dataset OULAD")
    
    # Distribuição de atividades
    st.markdown("#### Distribuição de Atividades por Tipo")
    fig_atividades = criar_grafico_atividades_oulad(df_oulad)
    if fig_atividades:
        st.pyplot(fig_atividades)
        plt.clf()
    
    # Resultado final
    st.markdown("#### Distribuição de Resultados Finais")
    fig_resultado = criar_grafico_resultado_final_oulad(df_oulad)
    if fig_resultado:
        st.pyplot(fig_resultado)
        plt.clf()

# Seção de insights
st.markdown("## 💡 Principais Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📚 Dataset UCI")
    if not df_uci.empty:
        uci_metricas = metricas_consolidadas['metricas_uci']
        st.markdown(f"""
        - **Total de estudantes**: {uci_metricas.get('total_alunos', 0):,}
        - **Média de notas finais**: {uci_metricas.get('media_nota_final', 0):.1f}
        - **Taxa de aprovação**: {uci_metricas.get('taxa_aprovacao', 0):.1f}%
        - **Média de faltas**: {uci_metricas.get('media_faltas', 0):.1f}
        """)

with col2:
    st.markdown("### 🌐 Dataset OULAD")
    if not df_oulad.empty:
        oulad_metricas = metricas_consolidadas['metricas_oulad']
        st.markdown(f"""
        - **Total de estudantes**: {oulad_metricas.get('total_estudantes', 0):,}
        - **Média de cliques**: {oulad_metricas.get('media_cliques', 0):.1f}
        - **Taxa de aprovação**: {oulad_metricas.get('taxa_aprovacao', 0):.1f}%
        - **Atividade mais comum**: {oulad_metricas.get('atividade_mais_comum', 'N/A')}
        """)

# Footer
st.markdown("---")
st.markdown("**Mestrado em Tecnologia Educacional - UFC** | Dashboard desenvolvido para análise de dados educacionais")