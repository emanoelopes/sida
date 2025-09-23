from pathlib import Path
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Informações Básicas do Dados do UCI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    )


st.title("Informações Básicas do Dados do UCI")
st.divider()
st.markdown("# Apresentação do Conjunto de Dados UCI Machine Learning Repository")
st.markdown("O conjunto de dados UCI Machine Learning Repository é um repositório amplamente utilizado para conjuntos de dados de aprendizado de máquina. Ele é mantido pela Universidade da Califórnia, Irvine (UCI) e contém uma variedade de conjuntos de dados que são frequentemente usados para pesquisa, experimentação e benchmarking em aprendizado de máquina e ciência de dados.")
st.markdown("O repositório UCI Machine Learning Repository é uma fonte valiosa para pesquisadores e profissionais que desejam testar algoritmos de aprendizado de máquina, comparar desempenho e explorar diferentes técnicas de modelagem. Ele oferece uma ampla gama de conjuntos de dados, desde problemas simples até desafios mais complexos, abrangendo diversas áreas, como classificação, regressão, clustering e muito mais.")
st.markdown("Os conjuntos de dados no repositório UCI Machine Learning Repository são frequentemente acompanhados por descrições detalhadas, informações sobre atributos, tarefas associadas e referências bibliográficas. Isso facilita a compreensão e o uso adequado dos dados para fins de pesquisa e desenvolvimento de modelos de aprendizado de máquina.")
st.markdown("Em resumo, o UCI Machine Learning Repository é uma fonte valiosa de conjuntos de dados para a comunidade de aprendizado de máquina, promovendo a pesquisa e o avanço na área de ciência de dados.")

datasets_uci_path = Path(__file__).parent.parents[1] / 'datasets' / 'uci_data'
st.write(f"Path dos datasets: {datasets_uci_path}")

# Português
por = pd.read_csv('student-por.csv', sep=';')

# Matemática
mat = pd.read_csv('student-mat.csv', sep=';')

# Adicionando coluna com o conjunto de dados de origem
mat['origem'] = 'mat'
por['origem'] = 'por'

# Concatenando os dataframes

df = pd.concat([mat, por])

st.dataframe(df)