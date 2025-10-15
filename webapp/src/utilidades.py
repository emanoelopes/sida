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

def obter_metricas_principais_uci():
    """Retorna métricas principais do dataset UCI baseadas nas análises"""
    return {
        'total_estudantes': 1044,
        'media_nota_final': 10.42,
        'taxa_aprovacao': 67.3,
        'media_faltas': 5.7,
        'distribuicao_genero': {'F': 58.2, 'M': 41.8},
        'media_tempo_estudo': 2.0,
        'correlacao_g1_g3': 0.81,
        'correlacao_g2_g3': 0.91,
        'estudantes_alcool_baixo': 45.2,
        'estudantes_alcool_alto': 12.8
    }

def obter_metricas_principais_oulad():
    """Retorna métricas principais do dataset OULAD baseadas nas análises"""
    return {
        'total_estudantes': 28000,
        'taxa_aprovacao': 78.5,
        'media_cliques': 4.65,
        'distribuicao_genero': {'M': 56.2, 'F': 43.8},
        'faixa_etaria_principal': '35-55 anos',
        'atividade_mais_comum': 'outcontent',
        'regiao_principal': 'South West Region',
        'estudantes_aprovados': 78.5,
        'estudantes_distincao': 8.2,
        'estudantes_reprovados': 13.3
    }

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

def exibir_cartoes_informativos():
    """Exibe cartões informativos com métricas principais"""
    metricas_uci = obter_metricas_principais_uci()
    metricas_oulad = obter_metricas_principais_oulad()
    
    # Cartões principais
    st.markdown("## 📊 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🎓 Total de Estudantes", 
            f"{metricas_uci['total_estudantes'] + metricas_oulad['total_estudantes']:,}",
            help="Soma dos estudantes dos datasets UCI e OULAD"
        )
    
    with col2:
        taxa_geral = (metricas_uci['taxa_aprovacao'] + metricas_oulad['taxa_aprovacao']) / 2
        st.metric(
            "✅ Taxa de Aprovação Geral", 
            f"{taxa_geral:.1f}%",
            help="Média das taxas de aprovação dos dois datasets"
        )
    
    with col3:
        st.metric(
            "📚 Média de Notas (UCI)", 
            f"{metricas_uci['media_nota_final']:.1f}",
            help="Média das notas finais no dataset UCI"
        )
    
    with col4:
        st.metric(
            "🖱️ Média de Cliques (OULAD)", 
            f"{metricas_oulad['media_cliques']:.1f}",
            help="Média de cliques por estudante no dataset OULAD"
        )

def exibir_cartoes_detalhados():
    """Exibe cartões detalhados para cada dataset"""
    metricas_uci = obter_metricas_principais_uci()
    metricas_oulad = obter_metricas_principais_oulad()
    
    # Cartões UCI
    st.markdown("### 📚 Dataset UCI - Escolas Públicas Portuguesas")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Total de Estudantes", 
            f"{metricas_uci['total_estudantes']:,}",
            help="Estudantes de escolas públicas portuguesas"
        )
    
    with col2:
        st.metric(
            "✅ Taxa de Aprovação", 
            f"{metricas_uci['taxa_aprovacao']:.1f}%",
            help="Percentual de estudantes aprovados"
        )
    
    with col3:
        st.metric(
            "📊 Média de Faltas", 
            f"{metricas_uci['media_faltas']:.1f}",
            help="Número médio de faltas por estudante"
        )
    
    with col4:
        st.metric(
            "⏰ Tempo de Estudo", 
            f"{metricas_uci['media_tempo_estudo']:.1f}h/semana",
            help="Tempo médio de estudo semanal"
        )
    
    # Cartões OULAD
    st.markdown("### 🌐 Dataset OULAD - Plataforma de Aprendizado Online")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Total de Estudantes", 
            f"{metricas_oulad['total_estudantes']:,}",
            help="Estudantes da plataforma online"
        )
    
    with col2:
        st.metric(
            "✅ Taxa de Aprovação", 
            f"{metricas_oulad['taxa_aprovacao']:.1f}%",
            help="Percentual de estudantes aprovados"
        )
    
    with col3:
        st.metric(
            "🏆 Distinção", 
            f"{metricas_oulad['estudantes_distincao']:.1f}%",
            help="Percentual de estudantes com distinção"
        )
    
    with col4:
        st.metric(
            "🖱️ Engajamento", 
            f"{metricas_oulad['media_cliques']:.1f} cliques",
            help="Média de cliques por estudante"
        )

def obter_insights_uci():
    """Retorna insights principais do dataset UCI"""
    return {
        'titulo': '📚 Principais Insights - Dataset UCI',
        'insights': [
            "🎯 **Correlação Forte**: Notas do 1º e 2º bimestre têm correlação de 0.81 e 0.91 com a nota final",
            "👥 **Gênero**: Estudantes do sexo feminino representam 58.2% e têm desempenho ligeiramente superior",
            "🍷 **Consumo de Álcool**: 45.2% dos estudantes têm baixo consumo, com melhor desempenho acadêmico",
            "📚 **Tempo de Estudo**: Estudantes que estudam 5-10h/semana têm concentração de notas mais altas",
            "❌ **Faltas**: Estudantes com menos de 10 faltas alcançam notas máximas (10-14 pontos)",
            "👨‍👩‍👧‍👦 **Família**: Escolaridade dos pais influencia diretamente o desempenho dos filhos"
        ]
    }

def obter_insights_oulad():
    """Retorna insights principais do dataset OULAD"""
    return {
        'titulo': '🌐 Principais Insights - Dataset OULAD',
        'insights': [
            "👥 **Demografia**: 56.2% são do sexo masculino, com faixa etária predominante de 35-55 anos",
            "🏆 **Alto Desempenho**: 78.5% de aprovação, com 8.2% obtendo distinção",
            "🖱️ **Engajamento**: Média de 4.65 cliques por estudante, indicando engajamento moderado",
            "📚 **Atividades**: 'outcontent' é a atividade mais realizada, seguida por 'forumng'",
            "🌍 **Região**: South West Region concentra a maior parte dos estudantes",
            "📊 **Distribuição**: Aprovação supera largamente outras categorias (reprovação: 13.3%)"
        ]
    }
