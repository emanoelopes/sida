"""
Dashboard Consolidado - Visão geral dos datasets UCI e OULAD
Página separada para análise consolidada dos datasets
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.utilidades import (
    obter_metricas_principais_uci,
    obter_metricas_principais_oulad,
    exibir_cartoes_informativos,
    calcular_feature_importance_uci,
    calcular_feature_importance_oulad
)
from src.openai_interpreter import criar_sidebar_padrao

# Configuração da página
st.set_page_config(
    page_title="Dashboard Educacional",
    page_icon="📊",
    layout="wide"
)

# Sidebar padrão
criar_sidebar_padrao()

# Título principal
st.title("📊 Dashboard Consolidado")
st.markdown("Visão geral dos datasets UCI e OULAD")

# Métricas principais
st.markdown("## 📈 Métricas Principais")
exibir_cartoes_informativos()

# Gráficos comparativos
st.markdown("## 📊 Análise Comparativa")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📚 Dataset UCI")
    st.markdown("**Características:**")
    st.markdown("""
    - Escolas públicas portuguesas
    - Dados demográficos e comportamentais
    - Foco em educação tradicional
    - Features: faltas, notas, tempo de estudo, etc.
    """)
    
    # Feature importance UCI
    try:
        df_importance_uci = calcular_feature_importance_uci()
        if not df_importance_uci.empty:
            st.markdown("**Top Features UCI:**")
            top_uci = df_importance_uci.nlargest(5, 'importance')
            for idx, row in top_uci.iterrows():
                st.markdown(f"- **{row['feature']}**: {row['importance']:.3f}")
        else:
            st.warning("Feature importance UCI não disponível")
    except Exception as e:
        st.error(f"Erro ao carregar feature importance UCI: {e}")

with col2:
    st.markdown("### 🌐 Dataset OULAD")
    st.markdown("**Características:**")
    st.markdown("""
    - Plataforma de aprendizado online
    - Dados de engajamento digital
    - Foco em educação online
    - Features: cliques, pontuações, atividades, etc.
    """)
    
    # Feature importance OULAD
    try:
        df_importance_oulad = calcular_feature_importance_oulad()
        if not df_importance_oulad.empty:
            st.markdown("**Top Features OULAD:**")
            top_oulad = df_importance_oulad.nlargest(5, 'importance')
            for idx, row in top_oulad.iterrows():
                st.markdown(f"- **{row['feature']}**: {row['importance']:.3f}")
        else:
            st.warning("Feature importance OULAD não disponível")
    except Exception as e:
        st.error(f"Erro ao carregar feature importance OULAD: {e}")

# Análise de Feature Importance Combinada
st.markdown("## 🎯 Análise de Feature Importance Combinada")

try:
    # Combinar top features de ambos os datasets
    df_importance_uci = calcular_feature_importance_uci()
    df_importance_oulad = calcular_feature_importance_oulad()
    
    if not df_importance_uci.empty and not df_importance_oulad.empty:
        # Top 2 de cada dataset
        top_uci = df_importance_uci.nlargest(2, 'importance')
        top_oulad = df_importance_oulad.nlargest(2, 'importance')
        
        st.markdown("### 📋 Features Selecionadas para Template Unificado")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**UCI (Educação Tradicional):**")
            for idx, row in top_uci.iterrows():
                st.markdown(f"- **{row['feature']}**: {row['importance']:.3f}")
        
        with col2:
            st.markdown("**OULAD (Educação Online):**")
            for idx, row in top_oulad.iterrows():
                st.markdown(f"- **{row['feature']}**: {row['importance']:.3f}")
        
        st.markdown("### 💡 Insights")
        st.info("""
        **Combinação Estratégica:**
        - UCI fornece insights sobre comportamento tradicional (faltas, notas)
        - OULAD fornece insights sobre engajamento digital (cliques, atividades)
        - Template unificado combina o melhor dos dois mundos
        - Análise mais abrangente para educadores
        """)
        
    else:
        st.warning("Não foi possível carregar feature importance de ambos os datasets")
        
except Exception as e:
    st.error(f"Erro na análise combinada: {e}")

# Estatísticas dos Datasets
st.markdown("## 📊 Estatísticas dos Datasets")

try:
    # Carregar dados para estatísticas
    from src.carregar_dados import carregar_dados_uci, carregar_dados_oulad
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📚 Dataset UCI")
        try:
            df_uci = carregar_dados_uci()
            if not df_uci.empty:
                st.markdown(f"**Total de registros:** {len(df_uci)}")
                st.markdown(f"**Features:** {len(df_uci.columns)}")
                st.markdown(f"**Período:** Dados históricos de escolas portuguesas")
                
                # Estatísticas básicas
                if 'G3' in df_uci.columns:
                    media_notas = df_uci['G3'].mean()
                    st.metric("Média das Notas Finais", f"{media_notas:.2f}")
            else:
                st.warning("Dataset UCI não disponível")
        except Exception as e:
            st.error(f"Erro ao carregar UCI: {e}")
    
    with col2:
        st.markdown("### 🌐 Dataset OULAD")
        try:
            df_oulad = carregar_dados_oulad()
            if not df_oulad.empty:
                st.markdown(f"**Total de registros:** {len(df_oulad)}")
                st.markdown(f"**Features:** {len(df_oulad.columns)}")
                st.markdown(f"**Período:** Dados de plataforma online")
                
                # Estatísticas básicas
                if 'final_result' in df_oulad.columns:
                    taxa_aprovacao = (df_oulad['final_result'] == 'Pass').mean() * 100
                    st.metric("Taxa de Aprovação", f"{taxa_aprovacao:.1f}%")
            else:
                st.warning("Dataset OULAD não disponível")
        except Exception as e:
            st.error(f"Erro ao carregar OULAD: {e}")
            
except Exception as e:
    st.error(f"Erro ao carregar estatísticas: {e}")

# Recomendações
st.markdown("## 💡 Recomendações de Uso")

st.markdown("""
### 🎯 Para Professores e Coordenadores:

1. **Use o Template Unificado** (página inicial)
   - Combina insights de educação tradicional e online
   - Inclui campo para nome do aluno
   - Análise personalizada para sua turma

2. **Configure sua OpenAI API Key**
   - Permite interpretação automática dos gráficos
   - Insights em linguagem acessível
   - Foco em ações práticas

3. **Analise os Resultados**
   - Gráficos com rótulos em português
   - Interpretações para gestores escolares
   - Sugestões de intervenção pedagógica

### 🔧 Para Desenvolvedores:

1. **Estrutura Modular**
   - `utilidades.py`: Lógica de negócio
   - `openai_interpreter.py`: Interpretação IA
   - `home.py`: Landing page
   - `1_dashboard.py`: Dashboard consolidado

2. **Extensibilidade**
   - Fácil adição de novos datasets
   - Novos tipos de análise
   - Integração com outras APIs
""")

# Rodapé
st.markdown("---")
st.markdown("### ℹ️ Sobre o Sistema")
st.caption("""
**SIDA - Sistema Inteligente de Análise Educacional**

Mestrado em Tecnologia Educacional  
Programa de Pós-Graduação em Tecnologias Educacionais (PPGTE)  
Instituto UFC Virtual (IUVI)  
Universidade Federal do Ceará (UFC)

Versão 1.0.0 - 2025
""")
