import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import pickle

# Configuração da página Streamlit
st.set_page_config(page_title="Dashboard Educacional", layout="wide")

# Funções para carregar dados
@st.cache_data(show_spinner=False)
def load_uci_data(pickle_path: str = "uci.pkl") -> pd.DataFrame:
    """Carrega o arquivo pickle com os dados do banco UCI."""
    p = Path(pickle_path)
    if not p.is_file():
        st.warning(f"Arquivo {p} não encontrado.")
        return pd.DataFrame()
    
    try:
        with p.open("rb") as f:
            df = pickle.load(f)
    except Exception as e:
        st.error(f"Falha ao ler {p}: {e}")
        return pd.DataFrame()
    
    if not isinstance(df, pd.DataFrame):
        st.error(f"O conteúdo de {p} não é um DataFrame.")
        return pd.DataFrame()
    
    return df

@st.cache_data(show_spinner=False)
def load_oulad_data(pickle_path: str = "oulad.pkl") -> pd.DataFrame:
    """Carrega o arquivo pickle com os dados do banco OULAD."""
    p = Path(pickle_path)
    if not p.is_file():
        st.warning(f"Arquivo {p} não encontrado.")
        return pd.DataFrame()
    
    try:
        with p.open("rb") as f:
            df = pickle.load(f)
    except Exception as e:
        st.error(f"Falha ao ler {p}: {e}")
        return pd.DataFrame()
    
    if not isinstance(df, pd.DataFrame):
        st.error(f"O conteúdo de {p} não é um DataFrame.")
        return pd.DataFrame()
    
    return df

# Carregar dados no estado da sessão ou do usuário
if "df_uci" not in st.session_state:
    st.session_state.df_uci = load_uci_data("uci.pkl")

if "df_oulad" not in st.session_state:
    st.session_state.df_oulad = load_oulad_data("oulad.pkl")

# Exibir dados carregados
st.write("Dados da UCI:")
st.dataframe(st.session_state.df_uci)

st.write("Dados do OULAD:")
st.dataframe(st.session_state.df_oulad)

# Título do dashboard
st.title("Dashboard de Desempenho Educacional")

# Visão geral das métricas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Alunos ativos", "1,200")
col2.metric("Média de notas", "78,5")
col3.metric("Taxa de abandono", "3,2 %")
col4.metric("Engajamento médio", "2,3 cliques/dia")

# Contexto do dashboard
st.markdown("""
Esta página mostra uma visão consolidada dos dados de duas bases públicas:
- **UCI**: informações de escolas públicas.
- **OULAD**: plataforma de aprendizado online.
Essas análises ajudam gestores e professores a identificar áreas de melhoria e a planejar intervenções.
""")

# Distribuição de notas (UCI)
fig, ax = plt.subplots(figsize=(6,4))
sns.histplot(st.session_state.df_uci['G3'], bins=20, kde=True, ax=ax)
ax.set_title("Distribuição de Notas (UCI)")
st.pyplot(fig)

# Distribuição de Cliques (OULAD)
fig, ax = plt.subplots(figsize=(6,4))
sns.histplot(st.session_state.df_oulad['clicks'], bins=20, kde=True, ax=ax)
ax.set_title("Distribuição de Cliques (OULAD)")
st.pyplot(fig)

# Filtros
periodo = st.selectbox("Período", ["2021", "2022", "2023"])
genero = st.multiselect("Gênero", ["Masculino", "Feminino", "Outro"])

# Tabela de correlação
corr = st.session_state.df_uci.corr()
st.dataframe(corr.style.background_gradient(cmap="coolwarm"))