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
    exibir_cartoes_informativos,
    exibir_cartoes_detalhados,
    obter_insights_uci,
    obter_insights_oulad,
    obter_metricas_principais_uci,
    obter_metricas_principais_oulad,
    criar_sidebar_dashboard,
    criar_grafico_feature_importance_uci,
    criar_grafico_feature_importance_oulad,
    criar_secao_pygwalker
)
from src.vizualizacoes import (
    criar_grafico_sugerido_uci,
    criar_grafico_sugerido_oulad,
    criar_grafico_comparativo_insights
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

# Criar sidebar
periodo, genero = criar_sidebar_dashboard()

# Exibir cartões informativos principais
exibir_cartoes_informativos()

# Exibir cartões detalhados por dataset
exibir_cartoes_detalhados()

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

# Seção de visualizações sugeridas
st.markdown("## 📊 Gráficos Sugeridos com Insights")

# Tabs para organizar as visualizações
tab1, tab2, tab3, tab4 = st.tabs(["📚 Análises UCI", "🌐 Análises OULAD", "🔄 Comparações", "🎯 Feature Importance"])

with tab1:
    st.markdown("### 📚 Dataset UCI - Escolas Públicas Portuguesas")
    
    # Gráfico sugerido para UCI
    fig_uci = criar_grafico_sugerido_uci()
    if fig_uci:
        st.pyplot(fig_uci)
        plt.clf()
    
    # Insights UCI
    insights_uci = obter_insights_uci()
    st.markdown(f"### {insights_uci['titulo']}")
    for insight in insights_uci['insights']:
        st.markdown(f"- {insight}")

with tab2:
    st.markdown("### 🌐 Dataset OULAD - Plataforma de Aprendizado Online")
    
    # Gráfico sugerido para OULAD
    fig_oulad = criar_grafico_sugerido_oulad()
    if fig_oulad:
        st.pyplot(fig_oulad)
        plt.clf()
    
    # Insights OULAD
    insights_oulad = obter_insights_oulad()
    st.markdown(f"### {insights_oulad['titulo']}")
    for insight in insights_oulad['insights']:
        st.markdown(f"- {insight}")

with tab3:
    st.markdown("### 🔄 Comparações entre Datasets")
    
    # Gráfico comparativo
    fig_comparativo = criar_grafico_comparativo_insights()
    if fig_comparativo:
        st.pyplot(fig_comparativo)
        plt.clf()
    
    # Resumo comparativo dinâmico
    st.markdown("### 📈 Resumo Comparativo")
    
    # Carregar métricas para comparação dinâmica
    metricas_uci = obter_metricas_principais_uci()
    metricas_oulad = obter_metricas_principais_oulad()
    
    # Determinar gênero predominante
    uci_genero_maioria = max(metricas_uci['distribuicao_genero'], key=metricas_uci['distribuicao_genero'].get) if metricas_uci['distribuicao_genero'] else 'N/A'
    oulad_genero_maioria = max(metricas_oulad['distribuicao_genero'], key=metricas_oulad['distribuicao_genero'].get) if metricas_oulad['distribuicao_genero'] else 'N/A'
    
    st.markdown(f"""
    **Principais Diferenças:**
    - **Modalidade**: UCI (presencial) vs OULAD (online)
    - **Taxa de Aprovação**: OULAD ({metricas_oulad['taxa_aprovacao']:.1f}%) vs UCI ({metricas_uci['taxa_aprovacao']:.1f}%)
    - **Total de Estudantes**: UCI ({metricas_uci['total_estudantes']:,}) vs OULAD ({metricas_oulad['total_estudantes']:,})
    - **Demografia**: UCI tem mais {uci_genero_maioria} ({metricas_uci['distribuicao_genero'].get(uci_genero_maioria, 0):.1f}%), OULAD tem mais {oulad_genero_maioria} ({metricas_oulad['distribuicao_genero'].get(oulad_genero_maioria, 0):.1f}%)
    - **Faixa Etária**: UCI (15-19 anos) vs OULAD ({metricas_oulad['faixa_etaria_principal']})
    - **Engajamento**: OULAD permite medir cliques ({metricas_oulad['media_cliques']:.1f} cliques/estudante) e atividades online
    """)

with tab4:
    st.markdown("### 🎯 Análise de Feature Importance")
    st.markdown("Esta seção mostra quais variáveis são mais importantes para prever o desempenho dos estudantes.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📚 Feature Importance - Dataset UCI")
        fig_importance_uci = criar_grafico_feature_importance_uci()
        if fig_importance_uci:
            st.pyplot(fig_importance_uci)
            plt.clf()
        
        st.markdown("""
        **Principais Features UCI:**
        - **G1, G2**: Notas dos bimestres (maior importância)
        - **absences**: Número de faltas (impacto negativo)
        - **studytime**: Tempo de estudo semanal
        - **Medu, Fedu**: Escolaridade dos pais
        """)
    
    with col2:
        st.markdown("#### 🌐 Feature Importance - Dataset OULAD")
        fig_importance_oulad = criar_grafico_feature_importance_oulad()
        if fig_importance_oulad:
            st.pyplot(fig_importance_oulad)
            plt.clf()
        
        st.markdown("""
        **Principais Features OULAD:**
        - **clicks**: Engajamento na plataforma
        - **activity_type**: Tipo de atividade realizada
        - **age_band**: Faixa etária do estudante
        - **gender**: Gênero do estudante
        """)
    
    # Seção PyGWalker
    criar_secao_pygwalker()

# Seção de conclusões
st.markdown("## 🎯 Conclusões e Recomendações")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📚 Para Escolas Públicas (UCI)")
    
    # Carregar métricas UCI para insights dinâmicos
    metricas_uci = obter_metricas_principais_uci()
    
    st.markdown(f"""
    **Pontos de Atenção:**
    - Focar em redução de faltas (média atual: {metricas_uci['media_faltas']:.1f} faltas/estudante)
    - Incentivar tempo de estudo adequado (média atual: {metricas_uci['media_tempo_estudo']:.1f}h/semana)
    - Apoiar estudantes com baixo consumo de álcool ({metricas_uci['estudantes_alcool_baixo']:.1f}% têm baixo consumo)
    - Considerar influência da escolaridade dos pais
    - Taxa de aprovação atual: {metricas_uci['taxa_aprovacao']:.1f}%
    
    **Recomendações:**
    - Programas de acompanhamento para estudantes com muitas faltas
    - Workshops sobre gestão de tempo de estudo
    - Envolvimento das famílias no processo educacional
    - Foco em melhorar a taxa de aprovação de {metricas_uci['taxa_aprovacao']:.1f}%
    """)

with col2:
    st.markdown("### 🌐 Para Plataformas Online (OULAD)")
    
    # Carregar métricas OULAD para insights dinâmicos
    metricas_oulad = obter_metricas_principais_oulad()
    
    st.markdown(f"""
    **Pontos Fortes:**
    - Alta taxa de aprovação ({metricas_oulad['taxa_aprovacao']:.1f}%)
    - Boa distribuição de atividades (principal: {metricas_oulad['atividade_mais_comum']})
    - Engajamento moderado mas efetivo ({metricas_oulad['media_cliques']:.1f} cliques/estudante)
    - {metricas_oulad['estudantes_distincao']:.1f}% dos estudantes obtêm distinção
    
    **Recomendações:**
    - Aumentar atividades do tipo '{metricas_oulad['atividade_mais_comum']}'
    - Focar em estudantes da faixa {metricas_oulad['faixa_etaria_principal']}
    - Desenvolver estratégias para reduzir taxa de reprovação ({metricas_oulad['estudantes_reprovados']:.1f}%)
    - Manter foco na região {metricas_oulad['regiao_principal']}
    """)

# Footer
st.markdown("---")
st.markdown("**Mestrado em Tecnologia Educacional - UFC** | Dashboard desenvolvido para análise de dados educacionais")