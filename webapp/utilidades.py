from pathlib import Path
import streamlit as st
import pandas as pd
import os

def leitura_de_dados():
    if not 'dataframes' in st.session_state:
        # Definir o caminho para o diretório dos datasets
        dataset_path = Path(__file__).parents[2] / 'oulad_download' / 'oulad_data'
        #st.write(str(dataset_path))

        # Lista para armazenar os dataframes
        dataframes = {}

        # Percorrer os arquivos no diretório
        for filename in os.listdir(dataset_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(dataset_path, filename)
                df_name = os.path.splitext(filename)[0] # Nome do dataframe será o nome do arquivo sem a extensão
                try:
                    dataframes[df_name] = pd.read_csv(file_path, sep=',', encoding='ISO-8859-1')
                    print(f"Arquivo '{filename}' carregado com sucesso como dataframe '{df_name}'.")
                except Exception as e:
                    print(f"Erro ao carregar o arquivo '{filename}': {e}")
        st.session_state['dataframes'] = dataframes

