import pandas as pd
import pandas_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
from pathlib import Path
import os
import pickle
import sys

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from carregar_dados import carregar_uci_dados, carregar_oulad_dados

st.set_page_config(
    page_title="Pandas Profiling - Análise de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Pandas Profiling - Análise de Dados")
st.divider()

# Carregar dados se não estiverem no session_state
if "df_uci" not in st.session_state:
    try:
        with st.spinner("🔄 Carregando dados UCI..."):
            st.session_state.df_uci = carregar_uci_dados()
    except Exception as e:
        st.error(f"Erro ao carregar dados UCI: {e}")
        st.session_state.df_uci = pd.DataFrame()

if "df_oulad" not in st.session_state:
    try:
        with st.spinner("🔄 Carregando dados OULAD (pode levar alguns minutos na primeira vez)..."):
            st.session_state.df_oulad = carregar_oulad_dados()
    except Exception as e:
        st.error(f"Erro ao carregar dados OULAD: {e}")
        st.session_state.df_oulad = pd.DataFrame()

# Sidebar para seleção do dataset
with st.sidebar:
    st.markdown("### 📊 Seleção do Dataset")
    
    # Caixa de seleção para escolher o dataset
    dataset_options = {
        "📚 UCI Dataset": "df_uci",
        "🌐 OULAD Dataset": "df_oulad"
    }
    
    selected_dataset = st.selectbox(
        "Escolha o dataset para análise:",
        options=list(dataset_options.keys()),
        index=0,
        help="Selecione qual dataset você deseja analisar com o Pandas Profiling"
    )
    
    st.markdown("---")
    
    # Informações sobre o dataset selecionado
    if selected_dataset == "📚 UCI Dataset":
        st.markdown("### 📚 Sobre o Dataset UCI")
        st.markdown("""
        **Dataset UCI:**
        - Escolas públicas portuguesas
        - Dados demográficos e acadêmicos
        - Análise de fatores de sucesso
        - Variáveis: notas, faltas, tempo de estudo, etc.
        """)
        
        if not st.session_state.df_uci.empty:
            st.metric("Total de Registros", f"{len(st.session_state.df_uci):,}")
            st.metric("Total de Colunas", f"{len(st.session_state.df_uci.columns)}")
        else:
            st.warning("⚠️ Dados UCI não disponíveis")
    
    else:  # OULAD Dataset
        st.markdown("### 🌐 Sobre o Dataset OULAD")
        st.markdown("""
        **Dataset OULAD:**
        - Plataforma de aprendizado online
        - Dados de engajamento digital
        - Análise de atividades online
        - Variáveis: cliques, atividades, resultados, etc.
        """)
        
        if not st.session_state.df_oulad.empty:
            st.metric("Total de Registros", f"{len(st.session_state.df_oulad):,}")
            st.metric("Total de Colunas", f"{len(st.session_state.df_oulad.columns)}")
        else:
            st.warning("⚠️ Dados OULAD não disponíveis")
    
    st.markdown("---")
    st.markdown("### ℹ️ Sobre o Pandas Profiling")
    st.markdown("""
    O Pandas Profiling gera um relatório completo de análise exploratória de dados, incluindo:
    
    - **Visão geral** dos dados
    - **Correlações** entre variáveis
    - **Valores ausentes** e duplicados
    - **Distribuições** estatísticas
    - **Avisos** sobre qualidade dos dados
    """)
    
    st.markdown("---")
    st.markdown("**Mestrado em Tecnologia Educacional - UFC**")

# Obter o dataset selecionado
df_key = dataset_options[selected_dataset]
df = st.session_state[df_key]

# Verificar se o dataset está disponível
if df.empty:
    st.error(f"❌ O dataset {selected_dataset} não está disponível. Verifique se os dados foram carregados corretamente.")
    st.stop()

# Verificar se o dataset é muito grande e oferecer opção de amostragem
if len(df) > 10000:
    st.warning(f"⚠️ O dataset {selected_dataset} tem {len(df):,} registros. Para melhor performance, considere usar uma amostra.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        usar_amostra = st.checkbox("Usar amostra de 10.000 registros", value=True)
    with col2:
        if usar_amostra:
            df = df.sample(n=10000, random_state=42)
            st.info(f"📊 Usando amostra de {len(df):,} registros")

# Exibir informações básicas do dataset selecionado
st.markdown(f"### 📋 Informações do Dataset: {selected_dataset}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total de Registros", f"{len(df):,}")
with col2:
    st.metric("📋 Total de Colunas", f"{len(df.columns)}")
with col3:
    st.metric("❌ Valores Ausentes", f"{df.isnull().sum().sum():,}")
with col4:
    st.metric("🔄 Valores Duplicados", f"{df.duplicated().sum():,}")

st.markdown("---")

# Gerar e exibir o relatório do Pandas Profiling
st.markdown("### 🔍 Relatório de Análise Exploratória de Dados")

with st.spinner("🔄 Gerando relatório do Pandas Profiling... Isso pode levar alguns minutos para datasets grandes."):
    try:
        # Configurar o relatório do Pandas Profiling
        pr = df.profile_report(
            title=f"Relatório de Análise - {selected_dataset}",
            explorative=True,
            minimal=False,
            progress_bar=True,
            correlations={
                "auto": {"calculate": False},
                "pearson": {"calculate": True},
                "spearman": {"calculate": True},
                "kendall": {"calculate": False}
            }
        )
        
        # Exibir o relatório
        st_profile_report(pr)
        
    except Exception as e:
        st.error(f"❌ Erro ao gerar relatório do Pandas Profiling: {e}")
        st.markdown("""
        **Possíveis soluções:**
        - Verifique se o dataset não está vazio
        - Tente com um dataset menor
        - Verifique se há problemas de memória
        """)

# Informações adicionais
st.markdown("---")
st.markdown("### 💡 Dicas de Uso")
st.markdown("""
- **Navegue** pelas diferentes seções do relatório usando o menu lateral
- **Explore** as correlações entre variáveis
- **Analise** os avisos sobre qualidade dos dados
- **Use** os filtros interativos para explorar os dados
- **Exporte** o relatório se necessário usando o botão de download
""")