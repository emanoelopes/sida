from pathlib import Path
import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import numpy as np

st.set_page_config(
    page_title="Informações Básicas dos Dados do OULAD",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown('# Informações Básicas dos Dados do OULAD')
st.divider()

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


st.sidebar.selectbox('Escolha o dataframe para visualizar informações básicas:', 
             options=list(dataframes_oulad.keys()),
             key='selected_oulad_dataframe')

# apresentar o dataframe selecionado
#st.dataframe(dataframes_oulad[st.session_state['selected_oulad_dataframe']])

# apresentar informações básicas do dataframe selecionado
st.markdown("### Informações básicas do DataFrame:")
selected_df = dataframes_oulad[st.session_state['selected_oulad_dataframe']]

st.markdown("#### Head:")
st.dataframe(selected_df.head(3))

st.markdown("#### Shape:")
st.write(selected_df.shape)

st.markdown("#### Info:")
# Capture the output of info() to a string
import io
buffer = io.StringIO()
selected_df.info(buf=buffer)
info_string = buffer.getvalue()

# Display the string in a st.code block for better formatting
st.code(info_string, language='text')

st.markdown("#### Describe:")
st.dataframe(selected_df.describe().T.round(2))

st.markdown("#### Null Values:")
st.write(selected_df.isnull().sum())

st.markdown("#### Unique Values:")
st.write(selected_df.nunique())

st.markdown("#### Duplicated Values:")
st.write(selected_df.duplicated().sum())

st.markdown("#### Value Counts (Object Columns):")
st.write(selected_df.select_dtypes(include=['object']).nunique())

# Visualização de dados faltantes usando missingno
st.markdown("### Visualização de Dados Faltantes:")
st.markdown("#### Matriz de Dados Faltantes:")

fig, ax = plt.subplots()
msno.matrix(selected_df, figsize=(6, 4), ax=ax)
st.pyplot(fig)


# Imputando valores ausentes em 'date_registration' e 'date_unregistration'
# Criar uma cópia explícita do dataframe para evitar SettingWithCopyWarning
df_studentregistration_copy = df_studentregistration.copy()

mean_date_registration = df_studentregistration_copy['date_registration'].mean()
df_studentregistration_copy['date_unregistration'] = df_studentregistration_copy['date_unregistration'].fillna(df_studentregistration_copy['date_unregistration'].max())
df_studentregistration_copy['date_registration'] = df_studentregistration_copy['date_registration'].fillna(mean_date_registration)

# Display null values after imputation
print("Null values after imputing date_registration and date_unregistration:")
st.write(df_studentregistration_copy.isnull().sum())


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

vle_activities = pd.merge(df_studentvle, new_vle, on=['code_module','code_presentation','id_site'], how='inner')
assessments_activities = pd.merge(df_studentassessment, df_assessments, on='id_assessment', how='inner')
studentinfo_activities = pd.merge(vle_activities, new_studentInfo, on=['code_module','code_presentation','id_student'], how='inner')
merged_df = pd.merge(studentinfo_activities, assessments_activities, on=['code_module','code_presentation','id_student'], how='inner')

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

st.write("Merged DataFrame after handling missing values:")
st.dataframe(merged_df.isnull().sum())

st.write('# Análise Exploratória de Dados (EDA) - OULAD')
st.write('## Distribuição de Notas Finais dos Estudantes')

st.markdown("#### Describe (Numerical Columns):")
st.dataframe(merged_df.select_dtypes('number').describe().T.round(2))

plt.figure(figsize=(10, 6))
sns.histplot(merged_df['score'], bins=30, kde=True)
plt.title('Distribuição de Notas Finais dos Estudantes')
plt.xlabel('Nota Final')
plt.ylabel('Frequência')
st.pyplot(plt)
plt.clf()
