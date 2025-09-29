from pathlib import Path
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(
    page_title="Informações Básicas do Dados do UCI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    )


st.title("Informações Básicas do Dados do UCI")
st.divider()
st.markdown("# Apresentação do Conjunto de Dados UCI Machine Learning Repository")
st.markdown("O conjunto dEliminação da pe dados UCI Machine Learning Repository é um repositório amplamente utilizado para conjuntos de dados de aprendizado de máquina. Ele é mantido pela Universidade da Califórnia, Irvine (UCI) e contém uma variedade de conjuntos de dados que são frequentemente usados para pesquisa, experimentação e benchmarking em aprendizado de máquina e ciência de dados.")
st.markdown("O repositório UCI Machine Learning Repository é uma fonte valiosa para pesquisadores e profissionais que desejam testar algoritmos de aprendizado de máquina, comparar desempenho e explorar diferentes técnicas de modelagem. Ele oferece uma ampla gama de conjuntos de dados, desde problemas simples até desafios mais complexos, abrangendo diversas áreas, como classificação, regressão, clustering e muito mais.")
st.markdown("Os conjuntos de dados no repositório UCI Machine Learning Repository são frequentemente acompanhados por descrições detalhadas, informações sobre atributos, tarefas associadas e referências bibliográficas. Isso facilita a compreensão e o uso adequado dos dados para fins de pesquisa e desenvolvimento de modelos de aprendizado de máquina.")
st.markdown("Em resumo, o UCI Machine Learning Repository é uma fonte valiosa de conjuntos de dados para a comunidade de aprendizado de máquina, promovendo a pesquisa e o avanço na área de ciência de dados.")

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

st.markdown("Explorando os valores numéricos")
st.dataframe(df.select_dtypes('number').describe().T.round(2))

st.markdown("Explorando os valores categóricos")

st.markdown('Por meio da análise descritiva dos dados numéricos e categóricos, a maioria dos estudantes são do sexo feminino, moram em cidades em família com mais de três pessoas, sustentadas pelas mães, moram com os pais.')

st.markdown('### Distribuicao do grau de formação dos pais em relação a nota final.')

# Boxplot
fig, axes = plt.subplots(1, 2, figsize=(18, 5)) # Correct way to define axes

sns.boxplot(data=df, x='Fedu', y='G3', ax=axes[0])  #  Use the ax at the correct index
axes[0].set_title('Distribuição das Notas Finais por Grau de Formação do Pai')

sns.boxplot(data=df, x='Medu', y='G3', ax=axes[1])
axes[1].set_title('Distribuição das Notas Finais por Grau de Formação da Mãe')

plt.tight_layout()
st.pyplot(fig)
# plt.clf()


st.markdown('## Visualizando os dados')

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

#Bloxpot

# Ocupação da mãe
fig, ax = plt.subplots(figsize=(22, 8))

sns.violinplot(data=df, x='Mjob')
fig.suptitle('Ocupação da mãe', fontsize=20)
st.pyplot(fig)


# Nível de escolaridade da mãe
fig, ax = plt.subplots(figsize=(22, 8))

sns.violinplot(data=df, x='Medu')
fig.suptitle('Nível de escolaridade da mãe', fontsize=20)
st.pyplot(fig)