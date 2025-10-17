#!/usr/bin/env python3
"""
Script para gerar pickle otimizado dos dados OULAD
Execute este script para criar o arquivo oulad_data.pkl otimizado
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'webapp', 'src'))

from carregar_dados import carregar_dados_oulad_raw, processar_dados_oulad
import pickle

def main():
    print("🚀 Iniciando geração do pickle otimizado OULAD...")
    print("=" * 50)
    
    try:
        # Carregar dados brutos
        print("📂 Carregando dados brutos...")
        dataframes_oulad = carregar_dados_oulad_raw()
        
        # Processar dados
        print("⚙️ Processando dados...")
        df_oulad = processar_dados_oulad(dataframes_oulad)
        
        # Salvar pickle otimizado
        print("💾 Salvando pickle otimizado...")
        pickle_path = Path("oulad_data.pkl")
        
        with open(pickle_path, 'wb') as f:
            pickle.dump(df_oulad, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        # Verificar tamanho do arquivo
        file_size = pickle_path.stat().st_size / (1024 * 1024)  # MB
        print(f"✅ Pickle salvo: {pickle_path}")
        print(f"📊 Tamanho do arquivo: {file_size:.2f} MB")
        print(f"📊 Shape do dataset: {df_oulad.shape}")
        print(f"💾 Uso de memória: {df_oulad.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print("=" * 50)
        print("🎉 Processo concluído com sucesso!")
        print("💡 O arquivo oulad_data.pkl foi criado e pode ser usado pelo aplicativo.")
        
    except Exception as e:
        print(f"❌ Erro durante o processamento: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
