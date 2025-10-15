from pathlib import Path
import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import numpy as np
import pickle


st.set_page_config(
    page_title="Análise Exploratória dos Dados - OULAD",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

#st.markdown('# Informações Básicas dos Dados do OULAD')
#st.divider()

datasets_oulad_path = Path(__file__).parent.parents[1] / 'datasets' / 'oulad_data'
#st.write(f"Path dos datasets: {datasets_oulad_path}")

dataframes_oulad = {}

for filename in os.listdir(datasets_oulad_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(datasets_oulad_path, filename)
        df_name = os.path.splitext(filename)[0] # Nome do dataframe será o nome do arquivo sem a extensão
        try:
            dataframes_oulad[df_name] = pd.read_csv(file_path, sep=',', encoding='ISO-8859-1')
            print(f"Arquivo '{filename}' carregado com sucesso como dataframe '{df_name}'.")
        except Exception as e:
            print(f"Erro ao carregar o arquivo '{filename}': {e}")


df_assessments = dataframes_oulad['assessments'].head(10_000)
df_courses = dataframes_oulad['courses'].head(10_000)
df_vle = dataframes_oulad['vle'].head(10_000)
df_studentinfo = dataframes_oulad['studentInfo'].head(10_000)
df_studentregistration = dataframes_oulad['studentRegistration'].head(10_000)
df_studentassessment = dataframes_oulad['studentAssessment'].head(10_000)
df_studentvle = dataframes_oulad['studentVle'].head(10_000)

#function to display basic info for a given dataframe
def show_basic_info(df):
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
    print(df.describe().T.round(2))
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


# Imputando valores ausentes em 'date_registration' e 'date_unregistration'
# Criar uma cópia explícita do dataframe para evitar SettingWithCopyWarning
df_studentregistration_copy = df_studentregistration.copy()

mean_date_registration = df_studentregistration_copy['date_registration'].mean()
df_studentregistration_copy['date_unregistration'] = df_studentregistration_copy['date_unregistration'].fillna(df_studentregistration_copy['date_unregistration'].max())
df_studentregistration_copy['date_registration'] = df_studentregistration_copy['date_registration'].fillna(mean_date_registration)

# Display null values after imputation
print("Null values after imputing date_registration and date_unregistration:")
# st.write(df_studentregistration_copy.isnull().sum())


new_vle = df_vle.drop(['week_from','week_to'],axis=1)
show_basic_info(new_vle)

# Imputação com os valores mais frequentes por região
dataframes_oulad['studentInfo']['imd_band_2'] = dataframes_oulad['studentInfo'].apply(lambda x: dataframes_oulad['studentInfo'][dataframes_oulad['studentInfo']['region']==x['region']]['imd_band'].mode()[0] \
    if pd.isna(x['imd_band']) else x['imd_band'], axis=1)
new_studentInfo = df_studentinfo.drop(['imd_band'], axis=1)
show_basic_info(new_studentInfo)

# Imputando valores ausentes em 'date_registration' e 'date_unregistration'
# Criar uma cópia explícita do dataframe para evitar SettingWithCopyWarning
df_student_registration_copy = df_studentregistration.copy()

mean_date_registration = df_student_registration_copy['date_registration'].mean()
df_student_registration_copy['date_unregistration'] = df_student_registration_copy['date_unregistration'].fillna(df_student_registration_copy['date_unregistration'].max())
df_student_registration_copy['date_registration'] = df_student_registration_copy['date_registration'].fillna(mean_date_registration)

# Junção dos dados
@st.cache_data(ttl=3600)  # Cache por 1 hora
def merge_dataframes():
    vle_activities = pd.merge(df_studentvle, new_vle, on=['code_module','code_presentation','id_site'], how='inner')
    assessments_activities = pd.merge(df_studentassessment, df_assessments, on='id_assessment', how='inner')
    studentinfo_activities = pd.merge(vle_activities, new_studentInfo, on=['code_module','code_presentation','id_student'], how='inner')
    merged_df = pd.merge(studentinfo_activities, assessments_activities, on=['code_module','code_presentation','id_student'], how='inner')
    return merged_df

merged_df = merge_dataframes()
st.session_state['merged_df'] = merged_df

# Merge with courses dataframe
merged_df = pd.merge(merged_df, df_courses, on=['code_presentation'], how='inner')

# Merge with studentRegistration dataframe
merged_df = pd.merge(merged_df, df_studentregistration, on=['code_presentation','id_student'], how='inner')

# Imputing missing values for numerical columns with the mean
for col in merged_df.select_dtypes(include=np.number).columns:
    merged_df[col].fillna(merged_df[col].mean(), inplace=True)

# Imputing missing values for categorical columns with the most frequent value
for col in merged_df.select_dtypes(include='object').columns:
    merged_df[col].fillna(merged_df[col].mode()[0], inplace=True)

# st.write("Merged DataFrame after handling missing values:")
# st.dataframe(merged_df.isnull().sum())

st.write('# Análise Exploratória de Dados (EDA) - OULAD')

'''
Esta página apresenta uma Análise Exploratória dos Dados do OULAD (Open University Learning Analytics Dataset), com foco em entender o perfil dos estudantes, suas atividades na plataforma e fatores que influenciam o desempenho acadêmico . Através de visualizações, são identificados padrões relevantes, como a predominância de estudantes do gênero masculino e a distribuição etária dos estudantes.
'''

st.markdown("## Descrição estatísticas das colunas numéricas:")
st.dataframe(merged_df.select_dtypes('number').describe().T.round(2))

'''
A grande diferença entre a mediana (≈2) e a média (≈4.65) do número de cliques indica que a maioria dos estudantes tem engajamento moderado, mas uma pequena parcela é extremamente ativa, elevando a média geral.

O número de tentativas anteriores é zero para a vasta maioria dos estudantes (quartis e valor máximo são 0), sugerindo que o conjunto de dados está focado na performance na primeira tentativa.
'''


st.write('## Distribuição das notas finais dos estudantes')
plt.figure(figsize=(10, 6))
sns.histplot(merged_df['score'], bins=30, kde=True)
plt.title('Distribuição de Notas Finais dos Estudantes')
plt.xlabel('Nota Final')
plt.ylabel('Frequência')
st.pyplot(plt)
plt.clf()

'''
Com base no histograma, a maioria dos estudantes obteve notas finais elevadas, concentrando-se principalmente na faixa de 70 a 90. Há uma distribuição que parece ser bimodal ou multimodal, com picos notáveis e uma frequência menor de notas mais baixas.
'''

st.write('## Distribuição de Atividades por Tipo')
plt.figure(figsize=(10, 6))
sns.countplot(data=merged_df, x='activity_type', order=merged_df['activity_type'].value_counts().index)
plt.title('Distribuição de Atividades por Tipo')
plt.xlabel('Tipo de Atividade')
plt.ylabel('Contagem')
plt.xticks(rotation=45)
st.pyplot(plt)
plt.clf()

'''
A atividade mais realizada é a 'outcontent' com quase o dobro de execuções em relação à segunda posição que é 'forumng'. A distribuição é acentuadamente desigual, com poucas atividades (como "forumng" e "subpage") tendo uso moderado.
'''


st.markdown('## Explorando valores categóricos')
## Explorando valores categóricos
st.dataframe(merged_df.select_dtypes('object').describe().T)

"""
Por meio da análise dos dados categóricos, os estudantes são, na sua maioria, do gênero masculino, até 35 anos, que realizaram a atividade do tipo fórum na plataforma e foram aprovados.
"""

st.write('## Distribuição de Estudantes por Idade')
plt.figure(figsize=(10, 6))
sns.histplot(merged_df['age_band'], bins=30)
plt.title('Distribuição de Estudantes por Idade')
plt.xlabel('Idade')
plt.ylabel('Frequência')
st.pyplot(plt)
plt.clf()

'''
Este histograma revela que a maioria dos estudantes se encontra na faixa etária de 35 a 55 anos e a faixa etária dentro do grupo 0-35 é o segundo maior contingente, enquanto estudantes com mais de 55 anos são a minoria.
'''


st.write('## Distribuição de Estudantes por Gênero')
plt.figure(figsize=(6, 6))
sns.countplot(data=merged_df['gender'])
plt.title('Distribuição de Estudantes por Gênero')
plt.xlabel('Gênero')
plt.ylabel('Contagem')
st.pyplot(plt)
plt.clf()

'''
A diferença na quantidade entre os gêneros masculino e feminino é algo em torno de 60% 
'''

st.write('## Distribuição de Estudantes por Região')
plt.figure(figsize=(10, 6))
sns.countplot(data=merged_df, x='region', order=merged_df['region'].value_counts().index)
plt.title('Distribuição de Estudantes por Região')
plt.xlabel('Região')
plt.ylabel('Contagem')
plt.xticks(rotation=45)
st.pyplot(plt)
plt.clf()

"""
As regiões "South West Region" e "South Region" detêm a maior concentração de estudantes, resultando em uma leve predominância do sul da Inglaterra. A distribuição é relativamente decrescente e sem discrepâncias abruptas.
"""

st.write('## Distribuição dos Estudantes por Resultado Final')
plt.figure(figsize=(6, 6))
sns.countplot(data=merged_df['final_result'], order=merged_df['final_result'].value_counts().index)
plt.title('Distribuição dos Estudantes por Resultado Final')
plt.xlabel('Resultado Final')
plt.ylabel('Contagem')
st.pyplot(plt)
plt.clf()

'''
a grande maioria dos estudantes obteve o resultado "Pass" (Aprovado), superando vastamente as outras categorias. Os resultados de "Distinction" (Aprovação com mérito), "Withdrawn" (Desistente) e "Fail" (Reprovado) representam uma proporção muito menor do total de alunos, indicando uma alta taxa de sucesso geral.
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
    
    # Identify categorical and numerical columns
    categorical_cols = X_train_cleaned.select_dtypes(include='object').columns
    numerical_cols = X_train_cleaned.select_dtypes(include=np.number).columns
    
    # Create a column transformer to apply different preprocessing steps to different column types
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='mean'), numerical_cols),
            ('cat', Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))]), categorical_cols)
        ],
        remainder='passthrough' # Keep other columns (numeric) as they are
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
from sklearn.metrics import confusion_matrix, classification_report

# st.write(classification_report(y_test, predictions, zero_division=0))
# st.write(confusion_matrix(y_test, predictions))

from sklearn.inspection import permutation_importance
import pandas as pd

# Drop rows with NaN in y_test
nan_rows_test = y_test.isnull()
X_test_cleaned = X_test[~nan_rows_test].copy()
y_test_cleaned = y_test[~nan_rows_test].copy()

result = permutation_importance(ml_model, X_test_cleaned, y_test_cleaned, n_repeats=10, random_state=42, n_jobs=2)
sorted_idx = result.importances_mean.argsort()


fig, ax = plt.subplots(figsize=(12, 8))

ax.boxplot(result.importances[sorted_idx].T, vert=False, labels=X_test_cleaned.columns[sorted_idx])
ax.set_title("Permutation Importances (test set)")
fig.tight_layout()
st.pyplot(fig)

st.markdown("## Conclusão")
st.markdown("Nesta análise exploratória dos dados do OULAD, conseguimos entender melhor o perfil dos estudantes, suas atividades na plataforma e os fatores que influenciam seu desempenho acadêmico. Através da visualização dos dados, identificamos padrões interessantes, como a predominância de estudantes do gênero masculino e a distribuição etária dos participantes. Além disso, o treinamento do modelo de aprendizado de máquina nos permitiu avaliar a importância das diferentes características dos dados, destacando quais fatores têm maior impacto no resultado final dos estudantes. Essas informações são valiosas para instituições educacionais que buscam melhorar a experiência de aprendizagem e o suporte oferecido aos alunos. Futuras análises podem aprofundar ainda mais esses insights, explorando outras variáveis e utilizando técnicas avançadas de modelagem preditiva.")

with open('oulad.pkl', 'wb') as f:
    pickle.dump(ml_model, f)
    f.close()