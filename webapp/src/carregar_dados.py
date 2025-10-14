# src/carregar_dados.py
import pandas as pd
from pathlib import Path
import pickle

def carregar_uci_dados(pickle_path: str = "datasets/uci.pkl") -> pd.DataFrame:
    p = Path(pickle_path)
    if not p.is_file():
        raise FileNotFoundError(f"Arquivo {p} não encontrado.")
    
    try:
        with p.open("rb") as f:
            df = pickle.load(f)
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo {pickle_path}: {e}")
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O conteúdo do arquivo não é um DataFrame.")
    
    return df

def carregar_oulad_dados(pickle_path: str = "datasets/oulad.pkl") -> pd.DataFrame:
    p = Path(pickle_path)
    if not p.is_file():
        raise FileNotFoundError(f"Arquivo {p} não encontrado.")
    
    try:
        with p.open("rb") as f:
            df = pickle.load(f)
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo {pickle_path}: {e}")
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O conteúdo do arquivo não é um DataFrame.")
    
    return df