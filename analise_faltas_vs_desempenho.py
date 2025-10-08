import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import os

def analisar_faltas_desempenho(df):
    """
    Analisa a relação entre faltas e desempenho acadêmico.
    
    Args:
        df: DataFrame com os dados dos estudantes
    """
    st.markdown("## Relação entre Faltas e Desempenho Acadêmico")
    
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

    # Adicionar insight sobre os resultados
    st.markdown("""
    **Insight:** Observa-se uma tendência de queda no desempenho acadêmico conforme aumenta o número de faltas.
    Estudantes com menos de 5 faltas tendem a ter notas significativamente melhores que aqueles com mais de 20 faltas.
    """)

if __name__ == "__main__":
    # Caminho para os dados UCI
    datasets_uci_path = Path.cwd() / 'datasets' / 'uci_data'
    
    try:
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
        
        # Executar a análise
        analisar_faltas_desempenho(df)
    except Exception as e:
        st.error(f"Erro ao carregar ou processar os dados: {e}")