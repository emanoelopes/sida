from pathlib import Path
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(
    page_title="Informações Básicas do Conjunto de Dados UCI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    )

st.title("Informações Básicas do Conjunto de Dados UCI")
st.divider()

"""
# Apresentação do Conjunto de Dados UCI Machine Learning Repository

O UCI Machine Learning Repository é uma fonte valiosa de conjuntos de dados para a comunidade de aprendizado de máquina, promovendo a pesquisa e o avanço na área de ciência de dados.

"""

datasets_uci_path = Path(__file__).parent.parents[1] / 'datasets' / 'uci_data'
#st.write(f"Path dos datasets: {datasets_uci_path}")

# Português
por_path = os.path.join(datasets_uci_path, 'student-por.csv')
por = pd.read_csv(por_path, sep=';')
# Matemática
mat_path = os.path.join(datasets_uci_path, 'student-mat.csv')
mat = pd.read_csv(mat_path, sep=';')

# Adicionando coluna com o conjunto de dados de origem
mat['origem'] = 'mat'
por['origem'] = 'por'

# Concatenando os dataframes

df = pd.concat([mat, por])

# Transformando valores e tipos de dados
df['traveltime'] = df['traveltime'].map({1: '<15m', 2: '15-30m', 3: '30-1h', 4: '>1h'})
df['studytime'] = df['studytime'].map({1: '<2h', 2: '2-5h', 3: '5-10h', 4: '>10h'})
df[['Medu','Fedu','famrel','goout','Dalc','Walc','health']] = \
df[['Medu','Fedu','famrel','goout','Dalc','Walc','health']].astype('object')

st.markdown("## Explorando os valores numéricos")
numeric_df = df.select_dtypes('number')


# Create visualization selection in sidebar
with st.sidebar:
    st.markdown("### Visualização dos dados numéricos")
    st.write("Selecione o tipo de visualização:")
    viz_type = st.selectbox(
        "Tipo de Visualização",
        ["Box Plot", "Histograma", "Violin Plot"]
    )

    st.markdown("---")
    st.markdown("### Informações do Conjunto de Dados")
    st.write(f"**Número de Instâncias:** {df.shape[0]}")
    st.write(f"**Número de Atributos:** {df.shape[1]}")
    st.write(f"**Número de Atributos Numéricos:** {numeric_df.shape[1]}")
    st.write(f"**Número de Atributos Categóricos:** {df.select_dtypes('object').shape[1]}")
    st.write(f"**Número de Valores Ausentes:** {df.isnull().sum().sum()}")
    st.write(f"**Número de Valores Duplicados:** {df.duplicated().sum()}")
    st.markdown("---")
    
    ### footer
    st.markdown("Mestrado em Tecnologias Educacional - UFC")

# Create visualization section
st.markdown("### :material/analytics: Visualização das distribuições dos dados numéricos")

# Get all numeric column names
numeric_columns = numeric_df.columns.tolist()

if len(numeric_columns) > 0:
    # Determine number of rows and columns for subplots
    n_cols = min(3, len(numeric_columns))
    n_rows = (len(numeric_columns) + n_cols - 1) // n_cols
    
    # Create subplots based on selection
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    if n_rows == 1:
        axes = [axes] if n_cols == 1 else axes
    else:
        axes = axes.flatten()
    
    for i, col in enumerate(numeric_columns):
        if viz_type == "Box Plot":
            axes[i].boxplot(numeric_df[col].dropna())
            axes[i].set_title(f'Distribuição de {col}')
            axes[i].set_ylabel('Valor')
        elif viz_type == "Histograma":
            axes[i].hist(numeric_df[col].dropna(), bins=30, alpha=0.7, edgecolor='black')
            axes[i].set_title(f'Distribuição de {col}')
            axes[i].set_xlabel('Valor')
            axes[i].set_ylabel('Frequência')
        elif viz_type == "Violin Plot":
            axes[i].violinplot(numeric_df[col].dropna())
            axes[i].set_title(f'Distribuição de {col}')
            axes[i].set_ylabel('Valor')
        
    # Hide empty subplots
    for i in range(len(numeric_columns), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.write("Nenhuma coluna numérica encontrada.")

"""
As distribuições dos dados numéricos mostram que a faixa etária é, na sua maioria, entre 15 e 19 anos. O valor médio de horas semanais livres é de um pouco mais de 3h. A quantidade de faltas concentra-se próximo a zero. As notas, de um modo geral, estão concentradas em valores acima da média com uma dispersão aceitável, coeficiente de variação em torno de 27%.
"""

"""
Por meio da análise descritiva dos dados numéricos e categóricos, a maioria dos estudantes são do sexo feminino, moram em cidades em família com mais de três pessoas, sustentadas pelas mães, moram com os pais.
"""

"""
### Distribuiçãoo do grau de formação dos pais em relação a nota final
"""

# Boxplot
fig, axes = plt.subplots(1, 2, figsize=(18, 5)) # Correct way to define axes

sns.boxplot(data=df, x='Fedu', y='G3', ax=axes[0])  #  Use the ax at the correct index
axes[0].set_title('Distribuição das Notas Finais por Grau de Formação do Pai')

sns.boxplot(data=df, x='Medu', y='G3', ax=axes[1])
axes[1].set_title('Distribuição das Notas Finais por Grau de Formação da Mãe')

plt.tight_layout()
st.pyplot(fig)
# plt.clf()


st.markdown('## :material/query_stats: Distribuição das notas')

import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(data=df, x='G1', bins=20, kde=True, ax=ax[0])
ax[0].set_title('Distribuição das Notas G1')
sns.histplot(data=df, x='G2', bins=20, kde=True, ax=ax[1])
ax[1].set_title('Distribuição das Notas G2')
sns.histplot(data=df, x='G3', bins=20, kde=True, ax=ax[2])
ax[2].set_title('Distribuição das Notas G3')
plt.tight_layout()
st.pyplot(fig)
plt.clf()

"""
"""

#Bloxpot

# Ocupação da mãe
fig, ax = plt.subplots(figsize=(22, 8))

sns.violinplot(data=df, x='Mjob')
fig.suptitle('Ocupação da mãe', fontsize=20)
st.pyplot(fig)

"""
A ocupação da mãe concentra a maioria das instâncias em 'outros' o que não é um bom critério para seleção.
"""


# Nível de escolaridade da mãe
fig, ax = plt.subplots(figsize=(22, 8))

sns.violinplot(data=df, x='Medu')
fig.suptitle('Nível de escolaridade da mãe', fontsize=20)
st.pyplot(fig)