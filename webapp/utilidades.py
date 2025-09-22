from pathlib import Path
import streamlit as st
import pandas as pd
import os

def leitura_de_dados():
    """
    Carrega todos os arquivos CSV do diretório datasets/oulad_data em dataframes.
    
    Returns:
        dict: Dicionário com os dataframes carregados, onde a chave é o nome do arquivo sem extensão
    """
    if not 'dataframes' in st.session_state:
        # Definir o caminho para o diretório dos datasets
        dataset_path = Path(__file__).parents[1] / 'datasets' / 'oulad_data'
        
        # Verificar se o diretório existe
        if not dataset_path.exists():
            st.error(f"Diretório não encontrado: {dataset_path}")
            return {}
            
        st.info(f"Carregando dados de: {dataset_path}")

        # Dicionário para armazenar os dataframes
        dataframes = {}

        # Percorrer os arquivos no diretório
        for filename in os.listdir(dataset_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(dataset_path, filename)
                df_name = os.path.splitext(filename)[0]
                try:
                    df = pd.read_csv(file_path, sep=',', encoding='ISO-8859-1')
                    if df.empty:
                        st.warning(f"Arquivo '{filename}' está vazio.")
                        continue
                    dataframes[df_name] = df
                    st.success(f"Arquivo '{filename}' carregado com sucesso.")
                except Exception as e:
                    st.error(f"Erro ao carregar '{filename}': {str(e)}")

        st.session_state['dataframes'] = dataframes
    return st.session_state['dataframes']