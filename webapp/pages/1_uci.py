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

@st.cache_data
def concat():
    df = pd.concat([mat, por])
    return df

df = concat()

st.session_state['df_uci'] = df
# Transformando valores e tipos de dados
df['traveltime'] = df['traveltime'].map({1: '<15m', 2: '15-30m', 3: '30-1h', 4: '>1h'})
df['studytime'] = df['studytime'].map({1: '<2h', 2: '2-5h', 3: '5-10h', 4: '>10h'})
df[['Medu','Fedu','famrel','goout','Dalc','Walc','health']] = \
df[['Medu','Fedu','famrel','goout','Dalc','Walc','health']].astype('object')

st.markdown('## Distribuição das notas')

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

'''
## Avaliando a normalidade da classe G3
'''

import numpy as np
from scipy.stats import norm

media = df['G3'].mean()
desvio_padrao = df['G3'].std()
v_min = df['G3'].min()
v_max = df['G3'].max()

xs = np.linspace(v_min, v_max, 10_000)
ys = norm.pdf(xs, loc=media, scale=desvio_padrao)

fig, ax = plt.subplots(figsize=(18, 8))

sns.histplot(data=df, ax=ax, x='G3', binwidth=1.0, kde=True, stat='density')
ax.plot(xs, ys, color='red')

fig.suptitle('Notas finais')
st.pyplot(fig)


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
    st.markdown("## Informações")
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
st.markdown("### Visualização das distribuições dos dados numéricos ")

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
As distribuições dos dados numéricos mostram que a faixa etária é, na sua maioria, entre 15 e 19 anos. O valor médio de horas semanais livres é um pouco maior 3h. A quantidade de faltas concentra-se próximo a zero. As notas, de um modo geral, estão concentradas em valores acima da mediana com uma dispersão aceitável, coeficiente de variação em torno de 27%.
"""
"""
## Explorando os valores categóricos
"""

st.session_state['cat_columns'] = df.select_dtypes('object').describe().T

st.dataframe(st.session_state['cat_columns'], width='content')


"""
Por meio da análise descritiva dos dados numéricos e categóricos, a maioria dos estudantes é do sexo feminino, mora em cidades em família com mais de três pessoas, mora com os pais, com a mãe sendo a guardiã dos filhos.
"""
"""
### Distribuição do grau de formação dos pais em relação a nota final
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
'''
O gráfico apresenta uma relação direta do grau de formação do pai com a nota final, no entando há registros de estudante que alcançou nota final 15 com mãe sem educação formal, apesar das maiores notas serem alcançadas por filhos de mães com nível superior.
'''

# Nível de escolaridade da mãe
fig, ax = plt.subplots(figsize=(22, 8))

sns.violinplot(data=df, x='Medu')
fig.suptitle('Nível de escolaridade da mãe', fontsize=20)
st.pyplot(fig)

'''
Há uma concentração mais acentuada de mães com Nível Superior e com Ensino Fundamental II (6º ao 9º ano). 
'''

# 1. Análise de correlação entre variáveis numéricas
st.markdown("## Matriz de Correlação")
st.write("Esta visualização mostra como as variáveis numéricas se relacionam entre si.")

# Calcular a matriz de correlação
corr = numeric_df.corr()

# Plotar o mapa de calor
fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
            square=True, linewidths=.5, annot=True, fmt=".2f", ax=ax)
plt.title('Matriz de Correlação entre Variáveis Numéricas', fontsize=15)
st.pyplot(fig)
plt.clf()

'''
A idade é diretamente proporcionais às quantidade de faltas e falhas (notas baixas) e estas, por sua vez, possuem relação direta com tempo livre e faltas. As notas finais, possuem uma forte correlação com as notas do primeiro bimestre e, mais ainda, com as do segundo bimestre, 0.81 e 0.91, respectivamente.
'''

# 2. Análise da relação entre consumo de álcool e desempenho acadêmico
st.markdown("## Relação entre Consumo de Álcool e Desempenho Acadêmico")

fig, axes = plt.subplots(1, 2, figsize=(18, 6))
sns.boxplot(x='Dalc', y='G3', data=df, ax=axes[0])
axes[0].set_title('Consumo de Álcool Durante a Semana vs Nota Final')
axes[0].set_xlabel('Nível de Consumo de Álcool Durante a Semana')
axes[0].set_ylabel('Nota Final')

sns.boxplot(x='Walc', y='G3', data=df, ax=axes[1])
axes[1].set_title('Consumo de Álcool no Final de Semana vs Nota Final')
axes[1].set_xlabel('Nível de Consumo de Álcool no Final de Semana')
axes[1].set_ylabel('Nota Final')

plt.tight_layout()
st.pyplot(fig)
plt.clf()

'''
Estudantes com zero ou baixo consumo de álcool, durante a semana, alcançam nota máxima, com média de 12,5 e com registros de nota cinco. Os alunos com alto consumo de álcool, durante a semana, alcaçam notas um pouco acima de 15, mas apresentam média semelhante. Em relação ao consumo apenas no final de semana, os resultados são mais equivalentes quando a escala alcança o valor 3, ou seja, com moderação do consumo.
'''

# 3. Análise do impacto do tempo de estudo no desempenho
st.markdown("## Impacto do Tempo de Estudo no Desempenho Acadêmico")

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='studytime', y='G3', data=df, ax=ax)
ax.set_title('Tempo de Estudo vs Nota Final')
ax.set_xlabel('Tempo de Estudo Semanal')
ax.set_ylabel('Nota Final')
st.pyplot(fig)
plt.clf()

'''
A correlação entre o número de horas de estudo e a pontuação final indica que 75% dos alunos que dedicam menos de 2 horas por semana, obtêm uma pontuação inferior a 13. Aqueles que estudam de 5 a 10h têm uma concentração de notas mais altas, até mesmo em comparação com aqueles que estudam mais de 10h; estes foram os que obtiveram as maiores notas.
'''

# 4. Análise de desempenho por gênero
st.markdown("## Comparação de Desempenho por Gênero")

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='sex', y='G3', data=df, ax=ax)
ax.set_title('Notas Finais por Gênero')
ax.set_xlabel('Gênero')
ax.set_ylabel('Nota Final')

st.pyplot(fig)
plt.clf()

'''
Uma análise das notas finais de ambos os gêneros revela que, apesar da distribuição e da variabilidade das notas serem bastante parecidas, a mediana das notas femininas é um pouco mais alta que a dos homens.'''

# 5. Análise de faltas vs desempenho
st.markdown("## Relação entre faltas e nota final")

# Criar categorias de faltas
# Criar um DataFrame temporário para evitar problemas de índice duplicado
temp_df = df.reset_index(drop=True).copy()

# Criar categorias de faltas
temp_df['absences_cat'] = pd.cut(temp_df['absences'], 
                           bins=[0, 5, 10, 15, 20, 100], 
                           labels=['0-5', '6-10', '11-15', '16-20', '21+'])

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='absences_cat', y='G3', data=temp_df, ax=ax)
ax.set_title('Faltas vs Nota Final')
ax.set_xlabel('Número de Faltas')
ax.set_ylabel('Nota Final')

st.pyplot(fig)
plt.clf()

'''
O gráfico indica uma ligeira tendência de queda na nota final conforme o número de faltas aumenta, especialmente a partir da faixa de 11-15 faltas. Estudantes que apresentam menos de 10 faltas alcançam notas máximas e concentram-se entre 10 e 14 pontos. As notas medianas e máximas observadas demonstram uma redução significativa quando superior a 16 faltas.
'''

st.markdown("## Entendendo as relações das classes utilizando Aprendizado de Máquina")

st.markdown("Preparação dos dados para modelos de ML...")
Y = df['G3']
X = df.drop('G3', axis=1)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

"""
Treinando o modelo...
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Identify categorical columns
categorical_features = X.select_dtypes(include=['object']).columns

# Create a column transformer to apply one-hot encoding
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough' # Keep other columns (numerical)
)

# Create a pipeline with the preprocessor and the model
model = Pipeline(steps=[('preprocessor', preprocessor),
                      ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

# Convert the target variable to integers (although for regression this might not be strictly necessary depending on the model, it doesn't hurt)
y_train = y_train.astype(float) # Convert to float for regression

model.fit(X_train, y_train)

"""
## Avaliação do modelo
"""

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import confusion_matrix, classification_report

import numpy as np

# Make predictions on the test data
predictions = model.predict(X_test)

# Evaluate the model using regression metrics
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

st.markdown(f"Mean Absolute Error (MAE): {mae:.2f}")
st.markdown(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
st.markdown(f"R-squared (R2): {r2:.2f}")


"""
## Importância das classes em relação ao resultado final\
"""

from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2)
sorted_idx = result.importances_mean.argsort()

fig, ax = plt.subplots(figsize=(12, 10))
ax.boxplot(result.importances[sorted_idx].T,
           vert=False, labels=X_test.columns[sorted_idx])
ax.set_title("Importância das classes")
fig.tight_layout()
st.pyplot(fig)


st.markdown("## Conclusão")

"""
Foi possível observar que a notal final (G3) é fortemente influenciada, em termos absolutos, pelas notas anteriores e a quantidade de faltas.
"""

# Salvando os resultados no formato pickle

import pickle
from pathlib import Path

with open('uci.pkl', 'wb') as f:
    pickle.dump(model, f)
    f.close()
