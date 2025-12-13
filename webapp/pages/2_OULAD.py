from pathlib import Path
import sys

# Adicionar o diretório webapp ao path do Python
webapp_dir = Path(__file__).parent.parent
if str(webapp_dir) not in sys.path:
    sys.path.insert(0, str(webapp_dir))

import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import numpy as np
import pickle
from src.openai_interpreter import criar_rodape_sidebar


st.set_page_config(
    page_title="Análise Exploratória dos Dados - OULAD",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

#st.markdown('# Informações Básicas dos Dados do OULAD')
#st.divider()

# Tentar carregar dos pickles primeiro (já estão no Git LFS)
@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_dados_oulad():
    """Carrega dados OULAD, tentando primeiro dos pickles, depois dos CSVs"""
    from src.carregar_dados import carregar_oulad_dados, carregar_dados_oulad_raw
    
    # Tentar carregar do pickle primeiro
    try:
        df = carregar_oulad_dados()
        if df is not None and not df.empty:
            # Se carregou do pickle, retornar como dict para compatibilidade
            return {'oulad_processed': df}
    except Exception as e:
        st.warning(f"Não foi possível carregar do pickle: {e}")
    
    # Fallback: tentar carregar dos CSVs
    try:
        dataframes_oulad = carregar_dados_oulad_raw()
        return dataframes_oulad
    except FileNotFoundError as e:
        st.error(f"""
        **Erro ao carregar dados OULAD:**
        
        Os arquivos de dados não foram encontrados. Verifique se:
        1. Os arquivos pickle (`oulad_data.pkl` ou `oulad_dataframe.pkl`) estão no repositório
        2. Os arquivos CSV estão em `datasets/oulad_data/`
        
        Erro: {e}
        """)
        st.stop()
    except Exception as e:
        st.error(f"Erro inesperado ao carregar dados: {e}")
        st.stop()

dataframes_oulad = carregar_dados_oulad()

# Se carregou do pickle processado, tentar carregar CSVs também para ter DataFrames individuais
if 'oulad_processed' in dataframes_oulad:
    df_processed = dataframes_oulad['oulad_processed']
    st.info("📦 Dados carregados do pickle processado. Tentando carregar CSVs individuais para análises detalhadas...")
    
    # Tentar carregar CSVs individuais como fallback
    try:
        from src.carregar_dados import carregar_dados_oulad_raw
        dataframes_oulad_raw = carregar_dados_oulad_raw()
        # Usar os CSVs individuais se disponíveis
        df_assessments = dataframes_oulad_raw.get('assessments', pd.DataFrame()).head(10_000)
        df_courses = dataframes_oulad_raw.get('courses', pd.DataFrame()).head(10_000)
        df_vle = dataframes_oulad_raw.get('vle', pd.DataFrame()).head(10_000)
        df_studentinfo = dataframes_oulad_raw.get('studentInfo', pd.DataFrame()).head(10_000)
        df_studentregistration = dataframes_oulad_raw.get('studentRegistration', pd.DataFrame()).head(10_000)
        df_studentassessment = dataframes_oulad_raw.get('studentAssessment', pd.DataFrame()).head(10_000)
        df_studentvle = dataframes_oulad_raw.get('studentVle', pd.DataFrame()).head(10_000)
        # Atualizar dataframes_oulad para usar os CSVs
        dataframes_oulad = dataframes_oulad_raw
        st.success("✅ CSVs individuais carregados com sucesso!")
    except Exception as e:
        st.warning(f"⚠️ Não foi possível carregar CSVs individuais: {e}")
        st.warning("Algumas funcionalidades podem estar limitadas. Usando dados processados.")
        # Criar DataFrames vazios para evitar erros
        df_assessments = pd.DataFrame()
        df_courses = pd.DataFrame()
        df_vle = pd.DataFrame()
        df_studentinfo = pd.DataFrame()
        df_studentregistration = pd.DataFrame()
        df_studentassessment = pd.DataFrame()
        df_studentvle = pd.DataFrame()
else:
    # Carregou dos CSVs originais
    df_assessments = dataframes_oulad.get('assessments', pd.DataFrame()).head(10_000)
    df_courses = dataframes_oulad.get('courses', pd.DataFrame()).head(10_000)
    df_vle = dataframes_oulad.get('vle', pd.DataFrame()).head(10_000)
    df_studentinfo = dataframes_oulad.get('studentInfo', pd.DataFrame()).head(10_000)
    df_studentregistration = dataframes_oulad.get('studentRegistration', pd.DataFrame()).head(10_000)
    df_studentassessment = dataframes_oulad.get('studentAssessment', pd.DataFrame()).head(10_000)
    df_studentvle = dataframes_oulad.get('studentVle', pd.DataFrame()).head(10_000)

#function to display basic info for a given dataframe
def show_basic_info(df):
    if df.empty or len(df.columns) == 0:
        print("DataFrame vazio - não é possível exibir informações")
        return
    
    print("========================================================================================================")
    print("HEAD:")
    print(df.head(3))
    print("--------------------------------------------------------------------------------------------------------")
    print("SHAPE:")
    print(df.shape)
    print("--------------------------------------------------------------------------------------------------------")
    print("INFO:")
    print(df.info())
    print("--------------------------------------------------------------------------------------------------------")
    print("DESCRIBE:")
    # Verificar se há colunas numéricas antes de descrever
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(df.describe().T.round(2))
    else:
        print("Nenhuma coluna numérica para descrever")
    print("--------------------------------------------------------------------------------------------------------")
    print("NULL VALUES:")
    print(df.isnull().sum())
    print("--------------------------------------------------------------------------------------------------------")
    print("UNIQUE VALUES:")
    print(df.nunique())
    print("--------------------------------------------------------------------------------------------------------")
    print("DUPLICATED VALUES:")
    print(df.duplicated().sum())
    print("--------------------------------------------------------------------------------------------------------")
    print("VALUE COUNTS:")
    print(df.select_dtypes(include=['object']).nunique())
    print("--------------------------------------------------------------------------------------------------------")
    print("========================================================================================================")


# st.sidebar.selectbox('Escolha o dataframe para visualizar informações básicas:', 
#              options=list(dataframes_oulad.keys()),
#              key='selected_oulad_dataframe')

# apresentar o dataframe selecionado
#st.dataframe(dataframes_oulad[st.session_state['selected_oulad_dataframe']])

# # apresentar informações básicas do dataframe selecionado
# st.markdown("### Informações básicas do DataFrame:")
# selected_df = dataframes_oulad[st.session_state['selected_oulad_dataframe']]

# st.markdown("#### Head:")
# st.dataframe(selected_df.head(3))

# st.markdown("#### Shape:")
# st.write(selected_df.shape)

# st.markdown("#### Info:")
# # Capture the output of info() to a string
# import io
# buffer = io.StringIO()
# selected_df.info(buf=buffer)
# info_string = buffer.getvalue()

# # Display the string in a st.code block for better formatting
# st.code(info_string, language='text')

# st.markdown("#### Describe:")
# st.dataframe(selected_df.describe().T.round(2))

# st.markdown("#### Null Values:")
# st.write(selected_df.isnull().sum())

# st.markdown("#### Unique Values:")
# st.write(selected_df.nunique())

# st.markdown("#### Duplicated Values:")
# st.write(selected_df.duplicated().sum())

# st.markdown("#### Value Counts (Object Columns):")
# st.write(selected_df.select_dtypes(include=['object']).nunique())

# # Visualização de dados faltantes usando missingno
# st.markdown("### Visualização de Dados Faltantes:")
# st.markdown("#### Matriz de Dados Faltantes:")

# fig, ax = plt.subplots()
# msno.matrix(selected_df, figsize=(6, 4), ax=ax)
# st.pyplot(fig)


# Remover colunas apenas se existirem e se o DataFrame não estiver vazio
if not df_vle.empty:
    cols_to_drop_vle = [col for col in ['week_from', 'week_to'] if col in df_vle.columns]
    if cols_to_drop_vle:
        new_vle = df_vle.drop(cols_to_drop_vle, axis=1)
    else:
        new_vle = df_vle.copy()
    
    if not new_vle.empty:
        show_basic_info(new_vle)
else:
    new_vle = pd.DataFrame()
    st.warning("⚠️ DataFrame VLE está vazio. Algumas análises podem não estar disponíveis.")

# Imputação com os valores mais frequentes por região (apenas se studentInfo não estiver vazio)
if not df_studentinfo.empty and 'imd_band' in df_studentinfo.columns and 'region' in df_studentinfo.columns:
    if 'studentInfo' in dataframes_oulad and not dataframes_oulad['studentInfo'].empty:
        dataframes_oulad['studentInfo']['imd_band_2'] = dataframes_oulad['studentInfo'].apply(
            lambda x: dataframes_oulad['studentInfo'][dataframes_oulad['studentInfo']['region']==x['region']]['imd_band'].mode()[0] 
            if pd.isna(x['imd_band']) and len(dataframes_oulad['studentInfo'][dataframes_oulad['studentInfo']['region']==x['region']]['imd_band'].mode()) > 0 
            else x['imd_band'], axis=1
        )
    
    # Remover coluna apenas se existir
    if 'imd_band' in df_studentinfo.columns:
        new_studentInfo = df_studentinfo.drop(['imd_band'], axis=1)
    else:
        new_studentInfo = df_studentinfo.copy()
else:
    new_studentInfo = df_studentinfo.copy()
show_basic_info(new_studentInfo)

# Imputando valores ausentes em 'date_registration' e 'date_unregistration'
# Criar uma cópia explícita do dataframe para evitar SettingWithCopyWarning
df_student_registration_copy = df_studentregistration.copy()

# Verificar se o DataFrame não está vazio e se as colunas existem antes de processá-las
if not df_student_registration_copy.empty and 'date_unregistration' in df_student_registration_copy.columns:
    # Criar variável binária indicando se o estudante cancelou o registro
    df_student_registration_copy['cancelou'] = df_student_registration_copy['date_unregistration'].notna().astype(int)
    
    # Preencher date_unregistration com valor alto quando ausente (para diferenciar de valores reais)
    # Usar max + 1000 para garantir que seja claramente distinto de qualquer data real
    max_date_unregistration = df_student_registration_copy['date_unregistration'].max()
    if pd.notna(max_date_unregistration):
        valor_nao_cancelou = max_date_unregistration + 1000
    else:
        # Se todos os valores forem NaN, usar um valor padrão alto
        valor_nao_cancelou = 999999
    df_student_registration_copy['date_unregistration'] = df_student_registration_copy['date_unregistration'].fillna(valor_nao_cancelou)
else:
    # Se a coluna não existir ou o DataFrame estiver vazio, criar uma coluna 'cancelou' com valores padrão
    if not df_student_registration_copy.empty:
        df_student_registration_copy['cancelou'] = 0
        st.warning("⚠️ Coluna 'date_unregistration' não encontrada. Usando valores padrão para 'cancelou'.")
    else:
        st.warning("⚠️ DataFrame 'studentRegistration' está vazio. Pulando processamento de datas de registro.")

# Preencher date_registration com a média quando ausente
if not df_student_registration_copy.empty and 'date_registration' in df_student_registration_copy.columns:
    mean_date_registration = df_student_registration_copy['date_registration'].mean()
    df_student_registration_copy['date_registration'] = df_student_registration_copy['date_registration'].fillna(mean_date_registration)
else:
    st.warning("⚠️ Coluna 'date_registration' não encontrada.")

# Junção dos dados (apenas se os DataFrames necessários não estiverem vazios)
@st.cache_data(ttl=3600)  # Cache por 1 hora
def merge_dataframes():
    if df_studentvle.empty or new_vle.empty:
        st.warning("⚠️ DataFrames VLE estão vazios. Pulando merge de VLE.")
        vle_activities = df_studentvle.copy()
    else:
        try:
            vle_activities = pd.merge(df_studentvle, new_vle, on=['code_module','code_presentation','id_site'], how='inner')
        except Exception as e:
            st.warning(f"⚠️ Erro ao fazer merge de VLE: {e}")
            vle_activities = df_studentvle.copy()
    
    if df_studentassessment.empty or df_assessments.empty:
        st.warning("⚠️ DataFrames de assessments estão vazios. Pulando merge de assessments.")
        assessments_activities = df_studentassessment.copy()
    else:
        try:
            assessments_activities = pd.merge(df_studentassessment, df_assessments, on='id_assessment', how='inner')
        except Exception as e:
            st.warning(f"⚠️ Erro ao fazer merge de assessments: {e}")
            assessments_activities = df_studentassessment.copy()
    
    if vle_activities.empty or new_studentInfo.empty:
        st.warning("⚠️ DataFrames necessários para merge estão vazios. Pulando merge com studentInfo.")
        studentinfo_activities = vle_activities.copy()
    else:
        try:
            studentinfo_activities = pd.merge(vle_activities, new_studentInfo, on=['code_module','code_presentation','id_student'], how='inner')
        except Exception as e:
            st.warning(f"⚠️ Erro ao fazer merge com studentInfo: {e}")
            studentinfo_activities = vle_activities.copy()
    
    if studentinfo_activities.empty or assessments_activities.empty:
        st.warning("⚠️ DataFrames necessários para merge final estão vazios.")
        merged_df = studentinfo_activities.copy()
    else:
        try:
            merged_df = pd.merge(studentinfo_activities, assessments_activities, on=['code_module','code_presentation','id_student'], how='inner')
        except Exception as e:
            st.warning(f"⚠️ Erro ao fazer merge final: {e}")
            merged_df = studentinfo_activities.copy()
    
    return merged_df

merged_df = merge_dataframes()
st.session_state['merged_df'] = merged_df

# Merge with courses dataframe (apenas se não estiver vazio)
if not merged_df.empty and not df_courses.empty:
    try:
        merged_df = pd.merge(merged_df, df_courses, on=['code_presentation'], how='inner')
    except Exception as e:
        st.warning(f"⚠️ Erro ao fazer merge com courses: {e}")
elif df_courses.empty:
    st.warning("⚠️ DataFrame courses está vazio. Pulando merge com courses.")

# Merge with studentRegistration dataframe (usando a versão processada com variável cancelou)
if not merged_df.empty and not df_student_registration_copy.empty:
    try:
        merged_df = pd.merge(merged_df, df_student_registration_copy, on=['code_presentation','id_student'], how='inner')
    except Exception as e:
        st.warning(f"⚠️ Erro ao fazer merge com studentRegistration: {e}")
elif df_student_registration_copy.empty:
    st.warning("⚠️ DataFrame studentRegistration está vazio. Pulando merge com studentRegistration.")

# Imputing missing values for numerical columns with the mean
for col in merged_df.select_dtypes(include=np.number).columns:
    merged_df[col].fillna(merged_df[col].mean(), inplace=True)

# Imputing missing values for categorical columns with the most frequent value
for col in merged_df.select_dtypes(include='object').columns:
    merged_df[col].fillna(merged_df[col].mode()[0], inplace=True)

# st.write("Merged DataFrame after handling missing values:")
# st.dataframe(merged_df.isnull().sum())

# Sidebar com rodapé
with st.sidebar:
    st.markdown("### 📊 Informações")
    st.info("""
    Esta página apresenta uma análise exploratória dos dados do OULAD (Open University Learning Analytics Dataset).
    """)
    st.markdown("---")
    # Rodapé com badges de status (igual ao da home)
    criar_rodape_sidebar()

st.write('# Análise Exploratória de Dados (EDA) - OULAD')

'''
Esta página apresenta uma Análise Exploratória dos Dados do OULAD (Open University Learning Analytics Dataset), com foco em entender o perfil dos estudantes, suas atividades na plataforma e fatores que influenciam o desempenho acadêmico . Através de visualizações, são identificados padrões relevantes, como a predominância de estudantes do gênero masculino e a distribuição etária dos estudantes.
'''

st.markdown("## Descrição estatísticas das colunas numéricas:")
numeric_df = merged_df.select_dtypes('number')
if not numeric_df.empty and len(numeric_df.columns) > 0:
    st.dataframe(numeric_df.describe().T.round(2))
else:
    st.warning("⚠️ Não há colunas numéricas disponíveis para análise estatística.")

'''
A grande diferença entre a mediana (≈2) e a média (≈4.65) do número de cliques indica que a maioria dos estudantes tem engajamento moderado, mas uma pequena parcela é extremamente ativa, elevando a média geral.

O número de tentativas anteriores é zero para a vasta maioria dos estudantes (quartis e valor máximo são 0), sugerindo que o conjunto de dados está focado na performance na primeira tentativa.
'''


st.write('## Distribuição das notas finais dos estudantes')
plt.figure(figsize=(10, 6))
# Calcular nota média por estudante único
if 'score' in merged_df.columns and 'id_student' in merged_df.columns:
    notas_por_estudante = merged_df.groupby('id_student')['score'].mean()
    sns.histplot(notas_por_estudante, bins=30, kde=True)
    plt.title('Distribuição de Notas Finais dos Estudantes (Únicos)')
    plt.xlabel('Nota Final Média')
    plt.ylabel('Número de Estudantes Únicos')
    st.pyplot(plt)
    plt.clf()
elif 'score' in merged_df.columns:
    sns.histplot(merged_df['score'], bins=30, kde=True)
    plt.title('Distribuição de Notas Finais dos Estudantes')
    plt.xlabel('Nota Final')
    plt.ylabel('Frequência')
    st.pyplot(plt)
    plt.clf()
else:
    st.warning("⚠️ Coluna 'score' não encontrada nos dados. Não é possível exibir a distribuição de notas.")

'''
Com base no histograma, a maioria dos estudantes obteve notas finais elevadas, concentrando-se principalmente na faixa de 70 a 90. Há uma distribuição que parece ser bimodal ou multimodal, com picos notáveis e uma frequência menor de notas mais baixas.
'''

st.write('## Distribuição de Atividades por Tipo')
plt.figure(figsize=(10, 6))
# Dicionário de tradução dos tipos de atividades
traducao_atividades = {
    'outcontent': 'Conteúdo Externo',
    'forumng': 'Fórum NG',
    'subpage': 'Subpágina',
    'resource': 'Recurso',
    'url': 'URL',
    'homepage': 'Página Inicial',
    'quiz': 'Quiz',
    'ouwiki': 'Wiki da Open University',
    'dataplus': 'DataPlus',
    'glossary': 'Glossário',
    'htmlactivity': 'Atividade HTML',
    'questionnaire': 'Questionário',
    'page': 'Página',
    'folder': 'Pasta',
    '   llaborate': 'Atividades Colaborativas',
    'dualpane': 'Painel Duplo',
    'repeatactivity': 'Atividade Repetida',
    'sharedsubpage': 'Subpágina Compartilhada'
}

# Contar atividades únicas por tipo (não estudantes únicos, pois é sobre atividades)
atividade_counts = merged_df['activity_type'].value_counts()
# Traduzir os índices (tipos de atividades) - criar novo Series com índices traduzidos
atividades_traduzidas = [traducao_atividades.get(x, x) for x in atividade_counts.index]
atividade_counts_traduzido = pd.Series(atividade_counts.values, index=atividades_traduzidas)
sns.barplot(x=atividade_counts_traduzido.index, y=atividade_counts_traduzido.values)
plt.title('Distribuição de Atividades por Tipo')
plt.xlabel('Tipo de Atividade')
plt.ylabel('Número de Atividades')
plt.xticks(rotation=45)
st.pyplot(plt)
plt.clf()

'''
A atividade mais realizada é a 'Conteúdo Externo' com quase o dobro de execuções em relação à segunda posição que é 'Fórum NG'. A distribuição é acentuadamente desigual, com poucas atividades (como "Fórum NG" e "Subpágina") tendo uso moderado.
'''


st.markdown('## Explorando valores categóricos')
## Explorando valores categóricos
categorical_df = merged_df.select_dtypes('object')
if not categorical_df.empty and len(categorical_df.columns) > 0:
    st.dataframe(categorical_df.describe().T)
else:
    st.warning("⚠️ Não há colunas categóricas disponíveis para análise.")

"""
Por meio da análise dos dados categóricos, os estudantes são, na sua maioria, do gênero masculino, até 35 anos, que realizaram a atividade do tipo fórum na plataforma e foram aprovados.
"""

col1, col2 = st.columns(2)

with col1:
    st.write('## Distribuição de Estudantes por Idade')
    # Contar estudantes únicos por faixa etária
    idade_counts = merged_df.groupby('age_band')['id_student'].nunique()
    fig_idade, ax_idade = plt.subplots(figsize=(6, 4))
    sns.barplot(x=idade_counts.index, y=idade_counts.values, ax=ax_idade)
    ax_idade.set_title('Distribuição de Estudantes por Idade')
    ax_idade.set_xlabel('Faixa Etária')
    ax_idade.set_ylabel('Número de Estudantes Únicos')
    ax_idade.tick_params(axis='x', rotation=45)
    st.pyplot(fig_idade)

    '''
    Este histograma revela que a maioria dos estudantes se encontra na faixa etária de 35 a 55 anos e a faixa etária dentro do grupo 0-35 é o segundo maior contingente, enquanto estudantes com mais de 55 anos são a minoria.
    '''

with col2:
    st.write('## Distribuição de Estudantes por Gênero')
    # Contar estudantes únicos por gênero
    genero_counts = merged_df.groupby('gender')['id_student'].nunique()
    fig_genero, ax_genero = plt.subplots(figsize=(6, 4))
    sns.barplot(x=genero_counts.index, y=genero_counts.values, ax=ax_genero)
    ax_genero.set_title('Distribuição de Estudantes por Gênero')
    ax_genero.set_xlabel('Gênero')
    ax_genero.set_ylabel('Número de Estudantes Únicos')
    st.pyplot(fig_genero)

    # Espaço extra para alinhar com o texto do gráfico ao lado
    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

    '''
    A diferença na quantidade entre os gêneros masculino e feminino é algo em torno de 60% 
    '''

st.write('## Distribuição de Estudantes por Região')
plt.figure(figsize=(10, 6))
# Dicionário de tradução das regiões
traducao_regioes = {
    'East Anglian Region': 'Região de East Anglia',
    'East Midlands Region': 'Região dos Midlands Orientais',
    'Ireland': 'Irlanda',
    'London Region': 'Região de Londres',
    'North Region': 'Região Norte',
    'North East Region': 'Região Nordeste',
    'North Western Region': 'Região Noroeste',
    'North West Region': 'Região Noroeste',
    'Scotland': 'Escócia',
    'South East Region': 'Região Sudeste',
    'South Region': 'Região Sul',
    'South West Region': 'Região Sudoeste',
    'Wales': 'País de Gales',
    'West Midlands Region': 'Região dos Midlands Ocidentais',
    'Yorkshire and The Humber Region': 'Região de Yorkshire e Humber',
    'Yorkshire and the Humber Region': 'Região de Yorkshire e Humber'
}

# Contar estudantes únicos por região
regiao_counts = merged_df.groupby('region')['id_student'].nunique().sort_values(ascending=False)
# Traduzir os índices (regiões) - criar novo Series com índices traduzidos
regioes_traduzidas = [traducao_regioes.get(x, x) for x in regiao_counts.index]
regiao_counts_traduzido = pd.Series(regiao_counts.values, index=regioes_traduzidas)
sns.barplot(x=regiao_counts_traduzido.index, y=regiao_counts_traduzido.values)
plt.title('Distribuição de Estudantes por Região')
plt.xlabel('Região')
plt.ylabel('Número de Estudantes Únicos')
plt.xticks(rotation=45)
st.pyplot(plt)
plt.clf()

"""
As regiões do sudeste sul detêm a maior concentração de estudantes, pode ter relação com a presença de importantes universidades na região: Universidade de Cambridge, Universidade de Essex, Universidade de Artes de Norwich, entre outras.
A distribuição é relativamente decrescente e sem discrepâncias abruptas.
"""

st.write('## Distribuição dos Estudantes por Resultado Final')
# Tamanho reduzido para evitar ocupar toda a largura
fig_resultado, ax_resultado = plt.subplots(figsize=(6, 4))
# Dicionário de tradução dos resultados finais
traducao_resultados = {
    'Pass': 'Aprovado',
    'Distinction': 'Aprovação com Mérito',
    'Withdrawn': 'Desistente',
    'Fail': 'Reprovado'
}

# Contar estudantes únicos por resultado final
resultado_counts = merged_df.groupby('final_result')['id_student'].nunique().sort_values(ascending=False)
# Traduzir os índices (resultados) - criar novo Series com índices traduzidos
resultados_traduzidos = [traducao_resultados.get(x, x) for x in resultado_counts.index]
resultado_counts_traduzido = pd.Series(resultado_counts.values, index=resultados_traduzidos)
sns.barplot(x=resultado_counts_traduzido.index, y=resultado_counts_traduzido.values, ax=ax_resultado)
ax_resultado.set_title('Distribuição dos Estudantes por Resultado Final')
ax_resultado.set_xlabel('Resultado Final')
ax_resultado.set_ylabel('Número de Estudantes Únicos')
st.pyplot(fig_resultado)

'''
A grande maioria dos estudantes obteve o resultado "Aprovado", superando vastamente as outras categorias. Os resultados de "Aprovação com Mérito", "Desistente" e "Reprovado" representam uma proporção muito menor do total de alunos, indicando uma alta taxa de sucesso geral.
'''

st.markdown('## Analisando  a importância das classes (feature importance)')

st.markdown("Preparação dos dados para modelos de ML...")
Y = merged_df['final_result']
X = merged_df.loc[:, merged_df.columns != 'final_result']

st.markdown('Removendo as classes irrelevantes ou com alta cardinalidade...')
X = X.drop(['id_student', 'id_site', 'id_assessment', 'code_module', 'code_presentation', 'code_module_y', 'code_module_x'], axis=1)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

@st.cache_data(ttl=7200)  # Cache por 2 horas
def treinar_modelo_oulad(X_train, y_train):
    """Treina o modelo OULAD com cache"""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    import pandas as pd
    
    # Drop rows with NaN in y_train
    nan_rows_train = y_train.isnull()
    X_train_cleaned = X_train[~nan_rows_train].copy()
    y_train_cleaned = y_train[~nan_rows_train].copy()
    
    # Identificar colunas categóricas de forma mais robusta
    # Incluir 'object', 'category' e verificar colunas que contêm strings
    categorical_cols = []
    numerical_cols = []
    
    # Lista de colunas conhecidas como categóricas no OULAD
    known_categorical = ['activity_type', 'gender', 'region', 'highest_education', 
                        'imd_band', 'age_band', 'disability', 'code_module', 
                        'code_presentation', 'assessment_type']
    
    for col in X_train_cleaned.columns:
        # Verificar se é numérico puro
        if pd.api.types.is_numeric_dtype(X_train_cleaned[col]):
            # Verificar se não contém strings (pode ter sido convertido incorretamente)
            try:
                pd.to_numeric(X_train_cleaned[col], errors='raise')
                numerical_cols.append(col)
            except (ValueError, TypeError):
                # Se não pode ser convertido para numérico, é categórico
                categorical_cols.append(col)
        else:
            # É categórico (object, category, ou string)
            categorical_cols.append(col)
    
    # Garantir que colunas conhecidas como categóricas estejam na lista
    for col in known_categorical:
        if col in X_train_cleaned.columns and col not in categorical_cols:
            categorical_cols.append(col)
            if col in numerical_cols:
                numerical_cols.remove(col)
    
    # Converter todas as colunas categóricas para string explicitamente
    for col in categorical_cols:
        if col in X_train_cleaned.columns:
            X_train_cleaned[col] = X_train_cleaned[col].astype(str)
            # Substituir 'nan' string por np.nan
            X_train_cleaned[col] = X_train_cleaned[col].replace('nan', np.nan)
            X_train_cleaned[col] = X_train_cleaned[col].replace('None', np.nan)
    
    # Converter colunas numéricas para float, tratando inf
    for col in numerical_cols:
        if col in X_train_cleaned.columns:
            X_train_cleaned[col] = pd.to_numeric(X_train_cleaned[col], errors='coerce')
            # Substituir inf por NaN
            X_train_cleaned[col] = X_train_cleaned[col].replace([np.inf, -np.inf], np.nan)
    
    # Remover colunas que ficaram vazias após limpeza
    cols_to_drop = []
    for col in X_train_cleaned.columns:
        if X_train_cleaned[col].isna().all():
            cols_to_drop.append(col)
    
    if cols_to_drop:
        X_train_cleaned = X_train_cleaned.drop(columns=cols_to_drop)
        categorical_cols = [c for c in categorical_cols if c not in cols_to_drop]
        numerical_cols = [c for c in numerical_cols if c not in cols_to_drop]
    
    # Garantir que temos pelo menos algumas colunas
    if len(categorical_cols) == 0 and len(numerical_cols) == 0:
        raise ValueError("Nenhuma coluna válida encontrada após limpeza dos dados")
    
    # Criar transformers apenas para colunas que existem
    transformers = []
    if len(numerical_cols) > 0:
        transformers.append(('num', SimpleImputer(strategy='mean'), numerical_cols))
    if len(categorical_cols) > 0:
        transformers.append(('cat', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), categorical_cols))
    
    # Create a column transformer to apply different preprocessing steps to different column types
    # Usar 'drop' em vez de 'passthrough' para garantir que todas as colunas sejam processadas
    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder='drop'  # Drop any columns not explicitly handled
    )
    
    # Create a pipeline that first preprocesses the data and then trains the model
    ml_model = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', RandomForestClassifier(n_estimators=50, n_jobs=2, max_depth=4, random_state=42))])
    
    # Train the model
    ml_model.fit(X_train_cleaned, y_train_cleaned)
    return ml_model

ml_model = treinar_modelo_oulad(X_train, y_train)

st.markdown("Modelo treinado com sucesso!")
st.markdown("Avaliando do modelo...")

predictions = ml_model.predict(X_test)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Drop rows with NaN in y_test
nan_rows_test = y_test.isnull()
X_test_cleaned = X_test[~nan_rows_test].copy()
y_test_cleaned = y_test[~nan_rows_test].copy()
predictions_cleaned = ml_model.predict(X_test_cleaned)

# Exibir métricas do modelo
st.markdown("### Métricas de Avaliação do Modelo")

# Calcular métricas individuais
accuracy = accuracy_score(y_test_cleaned, predictions_cleaned)
precision = precision_score(y_test_cleaned, predictions_cleaned, average='weighted', zero_division=0)
recall = recall_score(y_test_cleaned, predictions_cleaned, average='weighted', zero_division=0)
f1 = f1_score(y_test_cleaned, predictions_cleaned, average='weighted', zero_division=0)

# Criar tabela com as métricas
metricas_df = pd.DataFrame({
    'Métrica': ['Acurácia', 'Precisão (weighted)', 'Recall (weighted)', 'F1-Score (weighted)'],
    'Valor': [accuracy, precision, recall, f1]
})
metricas_df['Valor'] = metricas_df['Valor'].round(4)
st.dataframe(metricas_df, use_container_width=True, hide_index=True)

from sklearn.inspection import permutation_importance

result = permutation_importance(ml_model, X_test_cleaned, y_test_cleaned, n_repeats=10, random_state=42, n_jobs=2)
sorted_idx = result.importances_mean.argsort()

# Pegar apenas as top 5 features mais importantes (ordenadas da mais importante para a menos importante)
top_5_idx = sorted_idx[-5:][::-1]  # Reverter para ter a mais importante primeiro
top_5_features = X_test_cleaned.columns[top_5_idx]
top_5_importances = result.importances_mean[top_5_idx]

# Traduzir nomes das variáveis para exibição
feature_translation = {
    'date_unregistration': 'Data de cancelamento',
    'date_registration': 'Data de registro',
    'age_band': 'Faixa etária',
    'studied_credits': 'Créditos cursados',
    'studied_credits_x': 'Créditos cursados',
    'studied_credits_y': 'Créditos cursados',
    'score': 'Nota',
    'score_x': 'Nota',
    'score_y': 'Nota',
    'activity_type': 'Tipo de atividade',
    'clicks': 'Cliques',
    'gender': 'Gênero',
    'region': 'Região',
    'disability': 'Deficiência',
    'highest_education': 'Escolaridade',
    'imd_band': 'Faixa IMD',
    'num_of_prev_attempts': 'Tentativas anteriores',
    'module_presentation_length': 'Duração do módulo',
    'cancelou': 'Cancelou',
}
top_5_features_pt = [feature_translation.get(f, f) for f in top_5_features]

# Criar gráfico de barras
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(range(len(top_5_features)), top_5_importances)
ax.set_yticks(range(len(top_5_features)))
ax.set_yticklabels(top_5_features_pt)
ax.set_xlabel('Importância por Permutação')
ax.set_title('Top 5 Variáveis Mais Importantes (OULAD)')
ax.invert_yaxis()  # Mostrar a feature mais importante no topo
fig.tight_layout()
st.pyplot(fig)
st.markdown(
    "Histograma de importância das variáveis (método de permutação). "
    "Valores mais altos indicam maior impacto na previsão do resultado final."
)
plt.clf()

st.markdown("## Conclusão")
st.markdown("Nesta análise exploratória dos dados do OULAD, conseguimos entender melhor o perfil dos estudantes, suas atividades na plataforma e os fatores que influenciam seu desempenho acadêmico. Através da visualização dos dados, identificamos padrões interessantes, como a predominância de estudantes do gênero masculino e a distribuição etária dos participantes. Além disso, o treinamento do modelo de aprendizado de máquina nos permitiu avaliar a importância das diferentes características dos dados, destacando quais fatores têm maior impacto no resultado final dos estudantes. Essas informações são valiosas para instituições educacionais que buscam melhorar a experiência de aprendizagem e o suporte oferecido aos alunos. Futuras análises podem aprofundar ainda mais esses insights, explorando outras variáveis e utilizando técnicas avançadas de modelagem preditiva.")

with open('oulad.pkl', 'wb') as f:
    pickle.dump(ml_model, f)
    f.close()