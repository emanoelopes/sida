#!/usr/bin/env python3
"""
Script para gerar dataset unificado de UCI e OULAD.

Este script:
- Importa funções de unificação
- Executa processo completo de unificação
- Salva arquivos
- Exibe estatísticas e validações detalhadas
"""

import sys
from pathlib import Path

# Adicionar caminho do projeto ao sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "webapp"))

from webapp.src.unificar_datasets import unificar_datasets, salvar_dataset_unificado, validar_imputacao
import pandas as pd
import numpy as np


def exibir_estatisticas_detalhadas(df: pd.DataFrame, validacao: dict):
    """
    Exibe estatísticas detalhadas do dataset unificado.
    
    Args:
        df: DataFrame unificado
        validacao: Dicionário de validação
    """
    print("\n" + "=" * 70)
    print("📊 ESTATÍSTICAS DETALHADAS")
    print("=" * 70)
    
    # Estatísticas gerais
    print("\n📈 Estatísticas Gerais:")
    print(f"  - Total de registros: {validacao['total_registros']:,}")
    print(f"  - Total de colunas: {validacao['total_colunas']}")
    
    # Distribuição por origem
    print("\n📊 Distribuição por Origem:")
    if 'distribuicao_origem' in validacao:
        for origem, count in validacao['distribuicao_origem'].items():
            percentual = (count / validacao['total_registros']) * 100
            print(f"  - {origem}: {count:,} registros ({percentual:.2f}%)")
    
    # Estatísticas de resultado_final
    print("\n🎯 Estatísticas de resultado_final:")
    if 'estatisticas_resultado_final' in validacao and validacao['estatisticas_resultado_final']:
        stats = validacao['estatisticas_resultado_final']
        print(f"  - Mínimo: {stats.get('min', 'N/A'):.2f}")
        print(f"  - Máximo: {stats.get('max', 'N/A'):.2f}")
        print(f"  - Média: {stats.get('media', 'N/A'):.2f}")
        print(f"  - Mediana: {stats.get('mediana', 'N/A'):.2f}")
        print(f"  - Desvio padrão: {stats.get('std', 'N/A'):.2f}")
        print(f"  - NaN count: {stats.get('nan_count', 'N/A')}")
        
        if stats.get('nan_count', 0) == 0:
            print("  ✅ Nenhum NaN em resultado_final (CRÍTICO PARA ML)")
        else:
            print(f"  ⚠️ ATENÇÃO: {stats.get('nan_count', 0)} valores NaN encontrados!")
    
    # Distribuição de valores ausentes
    print("\n🔍 Valores Ausentes por Coluna:")
    if 'nan_por_coluna' in validacao and validacao['nan_por_coluna']:
        # Ordenar por percentual
        nan_sorted = sorted(
            validacao['nan_por_coluna'].items(),
            key=lambda x: x[1]['percentual'],
            reverse=True
        )
        
        print(f"  - Total de colunas com NaN: {len(validacao['nan_por_coluna'])}")
        print("\n  Top 10 colunas com mais NaN:")
        for col, info in nan_sorted[:10]:
            print(f"    - {col}: {info['count']:,} ({info['percentual']:.2f}%)")
    else:
        print("  ✅ Nenhum valor ausente encontrado!")
    
    # Tipos de dados
    print("\n🔤 Tipos de Dados:")
    tipos_contagem = {}
    for col, dtype in validacao.get('tipos_dados', {}).items():
        tipo_str = str(dtype)
        tipos_contagem[tipo_str] = tipos_contagem.get(tipo_str, 0) + 1
    
    for tipo, count in sorted(tipos_contagem.items()):
        print(f"  - {tipo}: {count} colunas")
    
    # Validações adicionais
    print("\n✅ Validações de Qualidade:")
    
    # Verificar resultado_final
    if 'resultado_final' in df.columns:
        nan_count = df['resultado_final'].isna().sum()
        if nan_count == 0:
            print("  ✅ resultado_final: Sem NaN")
        else:
            print(f"  ❌ resultado_final: {nan_count} NaN encontrados (ERRO CRÍTICO)")
        
        # Verificar range
        min_val = df['resultado_final'].min()
        max_val = df['resultado_final'].max()
        if min_val >= 0 and max_val <= 10:
            print(f"  ✅ resultado_final: Range válido ({min_val:.2f} - {max_val:.2f})")
        else:
            print(f"  ⚠️ resultado_final: Range fora do esperado ({min_val:.2f} - {max_val:.2f})")
    
    # Verificar faltas
    if 'faltas' in df.columns:
        min_faltas = df['faltas'].min()
        max_faltas = df['faltas'].max()
        if min_faltas >= 0 and max_faltas <= 50:
            print(f"  ✅ faltas: Range válido ({min_faltas:.0f} - {max_faltas:.0f})")
        else:
            print(f"  ⚠️ faltas: Range fora do esperado ({min_faltas:.0f} - {max_faltas:.0f})")
    
    # Verificar origem_dado
    if 'origem_dado' in df.columns:
        origens = df['origem_dado'].unique()
        if 'UCI' in origens and 'OULAD' in origens:
            print(f"  ✅ origem_dado: Ambas origens presentes ({', '.join(origens)})")
        else:
            print(f"  ⚠️ origem_dado: Apenas {', '.join(origens)} presente")


def exibir_informacoes_arquivos(pickle_path: Path, csv_path: Path):
    """
    Exibe informações sobre os arquivos gerados.
    
    Args:
        pickle_path: Caminho do arquivo pickle
        csv_path: Caminho do arquivo CSV
    """
    print("\n" + "=" * 70)
    print("💾 INFORMAÇÕES DOS ARQUIVOS GERADOS")
    print("=" * 70)
    
    if pickle_path.exists():
        size_mb = pickle_path.stat().st_size / (1024 * 1024)
        print(f"\n📦 Pickle: {pickle_path}")
        print(f"  - Tamanho: {size_mb:.2f} MB")
        print(f"  - Formato: Binário (protocol 4)")
    
    if csv_path.exists():
        size_mb = csv_path.stat().st_size / (1024 * 1024)
        print(f"\n📄 CSV: {csv_path}")
        print(f"  - Tamanho: {size_mb:.2f} MB")
        print(f"  - Formato: Texto (UTF-8)")
        print(f"  - Separador: Vírgula")
        print(f"  - Cabeçalho: Sim")


def main():
    """
    Função principal do script.
    """
    print("=" * 70)
    print("🚀 GERADOR DE DATASET UNIFICADO")
    print("=" * 70)
    print("\nEste script irá:")
    print("  1. Carregar dados UCI e OULAD")
    print("  2. Mapear colunas para português")
    print("  3. Agregar dados OULAD (uma linha por estudante)")
    print("  4. Unificar datasets")
    print("  5. Tratar dados ausentes")
    print("  6. Tratar outliers")
    print("  7. Validar dados")
    print("  8. Salvar arquivos (pickle e CSV)")
    
    try:
        # Executar unificação
        df_unificado = unificar_datasets()
        
        # Validar
        validacao = validar_imputacao(df_unificado)
        
        # Salvar arquivos
        pickle_path, csv_path = salvar_dataset_unificado(df_unificado)
        
        # Exibir estatísticas detalhadas
        exibir_estatisticas_detalhadas(df_unificado, validacao)
        
        # Exibir informações dos arquivos
        exibir_informacoes_arquivos(pickle_path, csv_path)
        
        # Resumo final
        print("\n" + "=" * 70)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print(f"\n📁 Arquivos gerados:")
        print(f"  - {pickle_path}")
        print(f"  - {csv_path}")
        print(f"\n📊 Dataset final:")
        print(f"  - Shape: {df_unificado.shape}")
        print(f"  - Memória: {df_unificado.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
        
        return 0
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ERRO DURANTE O PROCESSO")
        print("=" * 70)
        print(f"\nErro: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

