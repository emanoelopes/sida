# tests/test_carregar_dados.py
import pytest
from src.carregar_dados import carregar_uci_dados, carregar_oulad_dados

def test_carregar_uci_dados():
    df = carregar_uci_dados()
    assert isinstance(df, pd.DataFrame), "O retorno não é um DataFrame"
    # Adicione mais asserções conforme necessário para validar o conteúdo do DataFrame

def test_carregar_oulad_dados():
    df = carregar_oulad_dados()
    assert isinstance(df, pd.DataFrame), "O retorno não é um DataFrame"
    # Adicione mais asserções conforme necessário para validar o conteúdo do DataFrame