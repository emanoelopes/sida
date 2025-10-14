import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Educacional", layout="wide")

def leitura_oulad_data():
    datasets_path = Path(__file__).parent.parents / 'datasets' / 'oulad_data'
    st.write(f"Path dos datasets: {datasets_path}")

# --------------------------------------------------------------------------- #
# 1. Função que carrega os dados do banco UCI
# --------------------------------------------------------------------------- #
@st.cache_data(show_spinner=False)
def carregar_dados_uci(pickle_path: str = "uci.pkl") -> pd.DataFrame:
    """
    Lê o arquivo pickle com os dados do banco UCI e devolve um DataFrame.

    Parameters
    ----------
    pickle_path : str | Path, opcional
        Caminho relativo (ou absoluto) para o arquivo 'uci.pkl'.
        O padrão aponta para o arquivo que costuma ser salvo na raiz
        do projeto (conforme o trecho que salva o pickle – [2]).

    Returns
    -------
    pd.DataFrame
        O conjunto de dados da UCI.

    Raises
    ------
    FileNotFoundError
        Se o arquivo não existir.
    ValueError
        Se o conteúdo não puder ser des‑serializado como pickle.
    """
    p = Path(pickle_path)
    if not p.is_file():
        st.warning(f"Arquivo {p} não encontrado.")
        return pd.DataFrame()   # Retorna DataFrame vazio

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

# --------------------------------------------------------------------------- #
# 2. Função que carrega os dados do banco OULAD
# --------------------------------------------------------------------------- #
@st.cache_data(show_spinner=False)
def carregar_dados_oulad(pickle_path: str = "oulad.pkl") -> pd.DataFrame:
    """
    Lê o arquivo pickle contendo os dados do banco OULAD e devolve um DataFrame.

    O padrão de caminho segue o mesmo princípio da função anterior.
    """
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

if "df_uci" not in st.session_state:
    st.session_state.df_uci = carregar_dados_uci("uci.pkl") 

if "df_oulad" not in st.session_state:
    st.session_state.df_oulad = carregar_dados_oulad("caminho/para/oulad.pkl")

st.write("Dados da UCI:")
st.dataframe(st.session_state.df_uci)

st.write("Dados do OULAD:")
st.dataframe(st.session_state.df_oulad)

# 1. Cabeçalho
st.title("Dashboard de Desempenho Educacional")
# st.image("logo.png", width=150)

# 2. Visão geral
col1, col2, col3, col4 = st.columns(4)
col1.metric("Alunos ativos", "1,200")
col2.metric("Média de notas", "78,5")
col3.metric("Taxa de abandono", "3,2 %")
col4.metric("Engajamento médio", "2,3 cliques/dia")

# 3. Contexto
st.markdown("""
Esta página mostra uma visão consolidada dos dados de duas bases públicas:
- **UCI**: informações de escolas públicas.
- **OULAD**: plataforma de aprendizado online.
Essas análises ajudam gestores e professores a identificar áreas de melhoria e a planejar intervenções.
""")

# 4. Distribuição de notas (UCI)
fig, ax = plt.subplots(figsize=(6,4))
sns.histplot(st.session_state.df_uci['G3'], bins=20, kde=True, ax=ax)
ax.set_title("Distribuição de Notas (UCI)")
st.pyplot(fig)

# 5. Engajamento (OULAD)
fig, ax = plt.subplots(figsize=(6,4))
sns.histplot(st.session_state.df_oulad['clicks'], bins=20, kde=True, ax=ax)
ax.set_title("Distribuição de Cliques (OULAD)")
st.pyplot(fig)

# 6. Filtros
periodo = st.selectbox("Período", ["2021", "2022", "2023"])
gênero = st.multiselect("Gênero", ["Masculino", "Feminino", "Outro"])

# 7. Tabela de correlação
corr = st.session_state.df_uci.corr()
st.dataframe(corr.style.background_gradient(cmap="coolwarm"))