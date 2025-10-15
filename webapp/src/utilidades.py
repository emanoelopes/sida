from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .carregar_dados import carregar_uci_dados, carregar_oulad_dados

def leitura_oulad_data():
    """Função para leitura dos dados OULAD - mantida para compatibilidade"""
    datasets_path = Path(__file__).parent.parents[1] / 'datasets' / 'oulad_data'
    return datasets_path

def carregar_dados_dashboard():
    """Carrega os dados processados para o dashboard"""
    try:
        # Carregar dados UCI
        df_uci = carregar_uci_dados()
        st.session_state['df_uci'] = df_uci
    except Exception as e:
        st.warning(f"Erro ao carregar dados UCI: {e}")
        df_uci = pd.DataFrame()
        st.session_state['df_uci'] = df_uci
    
    try:
        # Carregar dados OULAD
        df_oulad = carregar_oulad_dados()
        st.session_state['df_oulad'] = df_oulad
    except Exception as e:
        st.warning(f"Erro ao carregar dados OULAD: {e}")
        df_oulad = pd.DataFrame()
        st.session_state['df_oulad'] = df_oulad
    
    return df_uci, df_oulad

def calcular_metricas_uci(df_uci):
    """Calcula métricas principais para o dataset UCI"""
    if df_uci.empty:
        return {}
    
    metricas = {
        'total_alunos': len(df_uci),
        'media_nota_final': df_uci['G3'].mean() if 'G3' in df_uci.columns else 0,
        'taxa_aprovacao': (df_uci['G3'] >= 10).mean() * 100 if 'G3' in df_uci.columns else 0,
        'media_faltas': df_uci['absences'].mean() if 'absences' in df_uci.columns else 0,
        'media_tempo_estudo': df_uci['studytime'].mean() if 'studytime' in df_uci.columns else 0,
        'distribuicao_genero': df_uci['sex'].value_counts().to_dict() if 'sex' in df_uci.columns else {},
        'correlacao_notas': df_uci[['G1', 'G2', 'G3']].corr().to_dict() if all(col in df_uci.columns for col in ['G1', 'G2', 'G3']) else {}
    }
    return metricas

def calcular_metricas_oulad(df_oulad):
    """Calcula métricas principais para o dataset OULAD"""
    if df_oulad.empty:
        return {}
    
    metricas = {
        'total_estudantes': len(df_oulad),
        'media_cliques': df_oulad['clicks'].mean() if 'clicks' in df_oulad.columns else 0,
        'taxa_aprovacao': (df_oulad['final_result'] == 'Pass').mean() * 100 if 'final_result' in df_oulad.columns else 0,
        'distribuicao_genero': df_oulad['gender'].value_counts().to_dict() if 'gender' in df_oulad.columns else {},
        'distribuicao_idade': df_oulad['age_band'].value_counts().to_dict() if 'age_band' in df_oulad.columns else {},
        'atividade_mais_comum': df_oulad['activity_type'].mode().iloc[0] if 'activity_type' in df_oulad.columns else 'N/A',
        'regiao_mais_comum': df_oulad['region'].mode().iloc[0] if 'region' in df_oulad.columns else 'N/A'
    }
    return metricas

def gerar_metricas_consolidadas(df_uci, df_oulad):
    """Gera métricas consolidadas para o dashboard"""
    metricas_uci = calcular_metricas_uci(df_uci)
    metricas_oulad = calcular_metricas_oulad(df_oulad)
    
    # Métricas consolidadas
    total_estudantes = metricas_uci.get('total_alunos', 0) + metricas_oulad.get('total_estudantes', 0)
    taxa_aprovacao_geral = np.mean([
        metricas_uci.get('taxa_aprovacao', 0),
        metricas_oulad.get('taxa_aprovacao', 0)
    ])
    
    return {
        'total_estudantes_geral': total_estudantes,
        'taxa_aprovacao_geral': taxa_aprovacao_geral,
        'metricas_uci': metricas_uci,
        'metricas_oulad': metricas_oulad
    }

def criar_sidebar_dashboard():
    """Cria a barra lateral do dashboard"""
    with st.sidebar:
        st.markdown("### 📊 Dashboard Educacional")
        st.markdown("---")
        
        st.markdown("### 📈 Filtros")
        periodo = st.selectbox("Período", ["2021", "2022", "2023", "Todos"])
        genero = st.multiselect("Gênero", ["Masculino", "Feminino", "Outro"])
        
        st.markdown("---")
        st.markdown("### 📚 Datasets")
        st.markdown("- **UCI**: Dados de escolas públicas")
        st.markdown("- **OULAD**: Plataforma de aprendizado online")
        
        st.markdown("---")
        st.markdown("### ℹ️ Informações")
        st.markdown("**Mestrado em Tecnologia Educacional - UFC**")
        
        return periodo, genero

def exibir_metricas_principais(metricas_consolidadas):
    """Exibe as métricas principais do dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Estudantes", 
            f"{metricas_consolidadas['total_estudantes_geral']:,}",
            help="Soma dos estudantes dos datasets UCI e OULAD"
        )
    
    with col2:
        st.metric(
            "Taxa de Aprovação Geral", 
            f"{metricas_consolidadas['taxa_aprovacao_geral']:.1f}%",
            help="Média das taxas de aprovação dos dois datasets"
        )
    
    with col3:
        uci_aprov = metricas_consolidadas['metricas_uci'].get('taxa_aprovacao', 0)
        st.metric(
            "Aprovação UCI", 
            f"{uci_aprov:.1f}%",
            help="Taxa de aprovação no dataset UCI"
        )
    
    with col4:
        oulad_aprov = metricas_consolidadas['metricas_oulad'].get('taxa_aprovacao', 0)
        st.metric(
            "Aprovação OULAD", 
            f"{oulad_aprov:.1f}%",
            help="Taxa de aprovação no dataset OULAD"
        )
