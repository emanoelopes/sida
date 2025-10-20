#!/usr/bin/env python3
"""
Script de manutenção para arquivos pickle
Regenera os arquivos pickle quando necessário
"""

import pandas as pd
import pickle
import os
from pathlib import Path
import sys

# Adicionar o diretório webapp/src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'webapp', 'src'))

def verificar_pickles():
    """Verifica se os arquivos pickle existem e estão íntegros"""
    print("🔍 Verificando arquivos pickle...")
    
    arquivos = ['uci_dataframe.pkl', 'oulad_dataframe.pkl']
    status = {}
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            try:
                with open(arquivo, 'rb') as f:
                    df = pickle.load(f)
                if isinstance(df, pd.DataFrame):
                    status[arquivo] = {
                        'existe': True,
                        'integro': True,
                        'shape': df.shape,
                        'tamanho_mb': os.path.getsize(arquivo) / 1024 / 1024
                    }
                    print(f"✅ {arquivo}: {df.shape} ({status[arquivo]['tamanho_mb']:.2f} MB)")
                else:
                    status[arquivo] = {'existe': True, 'integro': False}
                    print(f"❌ {arquivo}: Arquivo corrompido")
            except Exception as e:
                status[arquivo] = {'existe': True, 'integro': False}
                print(f"❌ {arquivo}: Erro ao carregar - {e}")
        else:
            status[arquivo] = {'existe': False, 'integro': False}
            print(f"❌ {arquivo}: Arquivo não encontrado")
    
    return status

def regenerar_pickles():
    """Regenera os arquivos pickle"""
    print("🔄 Regenerando arquivos pickle...")
    
    try:
        from carregar_dados import carregar_dados_uci_raw, carregar_dados_oulad_raw, processar_dados_oulad
        
        # Regenerar UCI
        print("📊 Processando UCI...")
        df_uci = carregar_dados_uci_raw()
        with open('uci_dataframe.pkl', 'wb') as f:
            pickle.dump(df_uci, f)
        print(f"✅ UCI salvo: {df_uci.shape}")
        
        # Regenerar OULAD
        print("📊 Processando OULAD...")
        dataframes_oulad = carregar_dados_oulad_raw()
        df_oulad = processar_dados_oulad(dataframes_oulad)
        with open('oulad_dataframe.pkl', 'wb') as f:
            pickle.dump(df_oulad, f)
        print(f"✅ OULAD salvo: {df_oulad.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao regenerar: {e}")
        return False

def main():
    """Função principal"""
    print("🛠️ Manutenção de Arquivos Pickle")
    print("=" * 40)
    
    # Verificar status atual
    status = verificar_pickles()
    
    # Verificar se precisa regenerar
    precisa_regenerar = any(not info.get('integro', False) for info in status.values())
    
    if precisa_regenerar:
        print("\n🔄 Regeneração necessária...")
        if regenerar_pickles():
            print("\n✅ Regeneração concluída!")
            print("\n🔍 Verificação final:")
            verificar_pickles()
        else:
            print("\n❌ Falha na regeneração!")
    else:
        print("\n✅ Todos os arquivos estão íntegros!")
    
    print("\n📋 Resumo:")
    for arquivo, info in status.items():
        if info.get('existe') and info.get('integro'):
            print(f"✅ {arquivo}: OK")
        else:
            print(f"❌ {arquivo}: Problema")

if __name__ == "__main__":
    main()
