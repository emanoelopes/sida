from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import time
try:
    from .carregar_dados import carregar_uci_dados, carregar_oulad_dados
except ImportError:
    # Fallback para quando executado diretamente
    from carregar_dados import carregar_uci_dados, carregar_oulad_dados

def leitura_oulad_data():
    """Função para leitura dos dados OULAD - mantida para compatibilidade"""
    datasets_path = Path(__file__).parent.parents[1] / 'datasets' / 'oulad_data'
    return datasets_path

@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_dados_uci_cached():
    """Carrega dados UCI com cache"""
    return carregar_uci_dados()

@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_dados_oulad_cached():
    """Carrega dados OULAD com cache"""
    return carregar_oulad_dados()

def carregar_dados_dashboard():
    """Carrega os dados processados para o dashboard com cache"""
    try:
        # Carregar dados UCI com cache
        df_uci = carregar_dados_uci_cached()
        st.session_state['df_uci'] = df_uci
    except Exception as e:
        st.warning(f"Erro ao carregar dados UCI: {e}")
        df_uci = pd.DataFrame()
        st.session_state['df_uci'] = df_uci
    
    try:
        # Carregar dados OULAD com cache
        df_oulad = carregar_dados_oulad_cached()
        st.session_state['df_oulad'] = df_oulad
    except Exception as e:
        st.warning(f"Erro ao carregar dados OULAD: {e}")
        df_oulad = pd.DataFrame()
        st.session_state['df_oulad'] = df_oulad
    
    return df_uci, df_oulad

def obter_metricas_principais_uci():
    """Retorna métricas principais do dataset UCI calculadas dinamicamente"""
    try:
        df_uci = carregar_dados_uci_cached()
        if df_uci.empty:
            return {
                'total_estudantes': 0,
                'media_nota_final': 0,
                'taxa_aprovacao': 0,
                'media_faltas': 0,
                'distribuicao_genero': {},
                'media_tempo_estudo': 0,
                'correlacao_g1_g3': 0,
                'correlacao_g2_g3': 0,
                'estudantes_alcool_baixo': 0,
                'estudantes_alcool_alto': 0
            }
        
        # Calcular métricas reais - contar estudantes únicos baseado em características demográficas
        # Usar combinação de colunas que identificam unicamente cada estudante
        colunas_id = ['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob', 'Fjob', 'reason', 'guardian']
        total_estudantes = df_uci[colunas_id].drop_duplicates().shape[0]
        media_nota_final = df_uci['G3'].mean() if 'G3' in df_uci.columns else 0
        taxa_aprovacao = (df_uci['G3'] >= 10).mean() * 100 if 'G3' in df_uci.columns else 0
        media_faltas = df_uci['absences'].mean() if 'absences' in df_uci.columns else 0
        
        # Distribuição de gênero
        if 'sex' in df_uci.columns:
            dist_genero = df_uci['sex'].value_counts(normalize=True) * 100
            distribuicao_genero = {k: round(v, 1) for k, v in dist_genero.to_dict().items()}
        else:
            distribuicao_genero = {}
        
        # Tempo de estudo médio - converter strings para números
        if 'studytime' in df_uci.columns:
            # Mapear strings para números para calcular média
            studytime_map = {'<2h': 1, '2-5h': 2, '5-10h': 3, '>10h': 4}
            studytime_numeric = df_uci['studytime'].map(studytime_map)
            media_tempo_estudo = studytime_numeric.mean()
        else:
            media_tempo_estudo = 0
        
        # Correlações
        correlacao_g1_g3 = df_uci[['G1', 'G3']].corr().iloc[0, 1] if all(col in df_uci.columns for col in ['G1', 'G3']) else 0
        correlacao_g2_g3 = df_uci[['G2', 'G3']].corr().iloc[0, 1] if all(col in df_uci.columns for col in ['G2', 'G3']) else 0
        
        # Consumo de álcool
        if 'Dalc' in df_uci.columns:
            alcool_baixo = (df_uci['Dalc'] <= 2).mean() * 100
            alcool_alto = (df_uci['Dalc'] >= 4).mean() * 100
        else:
            alcool_baixo = 0
            alcool_alto = 0
        
        return {
            'total_estudantes': total_estudantes,
            'media_nota_final': round(media_nota_final, 2),
            'taxa_aprovacao': round(taxa_aprovacao, 1),
            'media_faltas': round(media_faltas, 1),
            'distribuicao_genero': distribuicao_genero,
            'media_tempo_estudo': round(media_tempo_estudo, 1),
            'correlacao_g1_g3': round(correlacao_g1_g3, 2),
            'correlacao_g2_g3': round(correlacao_g2_g3, 2),
            'estudantes_alcool_baixo': round(alcool_baixo, 1),
            'estudantes_alcool_alto': round(alcool_alto, 1)
        }
    except Exception as e:
        st.warning(f"Erro ao calcular métricas UCI: {e}")
        return {
            'total_estudantes': 0,
            'media_nota_final': 0,
            'taxa_aprovacao': 0,
            'media_faltas': 0,
            'distribuicao_genero': {},
            'media_tempo_estudo': 0,
            'correlacao_g1_g3': 0,
            'correlacao_g2_g3': 0,
            'estudantes_alcool_baixo': 0,
            'estudantes_alcool_alto': 0
        }

def obter_metricas_principais_oulad():
    """Retorna métricas principais do dataset OULAD calculadas dinamicamente"""
    try:
        df_oulad = carregar_dados_oulad_cached()
        if df_oulad.empty:
            return {
                'total_estudantes': 0,
                'taxa_aprovacao': 0,
                'media_cliques': 0,
                'distribuicao_genero': {},
                'faixa_etaria_principal': 'N/A',
                'atividade_mais_comum': 'N/A',
                'regiao_principal': 'N/A',
                'estudantes_aprovados': 0,
                'estudantes_distincao': 0,
                'estudantes_reprovados': 0
            }
        
        # Calcular métricas reais
        # Usar nunique() para contar estudantes únicos, não registros
        if 'id_student' in df_oulad.columns:
            total_estudantes = df_oulad['id_student'].nunique()
        else:
            total_estudantes = len(df_oulad)  # Fallback se não houver coluna id_student
        
        media_cliques = df_oulad['clicks'].mean() if 'clicks' in df_oulad.columns else 0
        
        # Taxa de aprovação
        if 'final_result' in df_oulad.columns:
            taxa_aprovacao = (df_oulad['final_result'] == 'Pass').mean() * 100
            estudantes_aprovados = taxa_aprovacao
            estudantes_distincao = (df_oulad['final_result'] == 'Distinction').mean() * 100
            estudantes_reprovados = (df_oulad['final_result'] == 'Fail').mean() * 100
        else:
            taxa_aprovacao = 0
            estudantes_aprovados = 0
            estudantes_distincao = 0
            estudantes_reprovados = 0
        
        # Distribuição de gênero
        if 'gender' in df_oulad.columns and 'id_student' in df_oulad.columns:
            dist_genero = df_oulad.groupby('gender')['id_student'].nunique()
            total_estudantes = df_oulad['id_student'].nunique()
            dist_genero_pct = (dist_genero / total_estudantes * 100)
            distribuicao_genero = {k: round(v, 1) for k, v in dist_genero_pct.to_dict().items()}
        else:
            distribuicao_genero = {}
        
        # Faixa etária principal
        if 'age_band' in df_oulad.columns and 'id_student' in df_oulad.columns:
            # Encontrar a faixa etária com mais estudantes únicos
            idade_counts = df_oulad.groupby('age_band')['id_student'].nunique()
            faixa_etaria_principal = idade_counts.idxmax() if not idade_counts.empty else 'N/A'
        else:
            faixa_etaria_principal = 'N/A'
        
        # Atividade mais comum
        if 'activity_type' in df_oulad.columns:
            atividade_mais_comum = df_oulad['activity_type'].mode().iloc[0] if not df_oulad['activity_type'].mode().empty else 'N/A'
        else:
            atividade_mais_comum = 'N/A'
        
        # Região principal
        if 'region' in df_oulad.columns and 'id_student' in df_oulad.columns:
            # Encontrar a região com mais estudantes únicos
            regiao_counts = df_oulad.groupby('region')['id_student'].nunique()
            regiao_principal = regiao_counts.idxmax() if not regiao_counts.empty else 'N/A'
        else:
            regiao_principal = 'N/A'
        
        return {
            'total_estudantes': total_estudantes,
            'taxa_aprovacao': round(taxa_aprovacao, 1),
            'media_cliques': round(media_cliques, 2),
            'distribuicao_genero': distribuicao_genero,
            'faixa_etaria_principal': faixa_etaria_principal,
            'atividade_mais_comum': atividade_mais_comum,
            'regiao_principal': regiao_principal,
            'estudantes_aprovados': round(estudantes_aprovados, 1),
            'estudantes_distincao': round(estudantes_distincao, 1),
            'estudantes_reprovados': round(estudantes_reprovados, 1)
        }
    except Exception as e:
        st.warning(f"Erro ao calcular métricas OULAD: {e}")
        return {
            'total_estudantes': 0,
            'taxa_aprovacao': 0,
            'media_cliques': 0,
            'distribuicao_genero': {},
            'faixa_etaria_principal': 'N/A',
            'atividade_mais_comum': 'N/A',
            'regiao_principal': 'N/A',
            'estudantes_aprovados': 0,
            'estudantes_distincao': 0,
            'estudantes_reprovados': 0
        }

def calcular_metricas_uci(df_uci):
    """Calcula métricas principais para o dataset UCI"""
    if df_uci.empty:
        return {}
    
    # Contar estudantes únicos baseado em características demográficas
    colunas_id = ['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob', 'Fjob', 'reason', 'guardian']
    total_estudantes_unicos = df_uci[colunas_id].drop_duplicates().shape[0]
    
    metricas = {
        'total_alunos': total_estudantes_unicos,
        'media_nota_final': df_uci['G3'].mean() if 'G3' in df_uci.columns else 0,
        'taxa_aprovacao': (df_uci['G3'] >= 10).mean() * 100 if 'G3' in df_uci.columns else 0,
        'media_faltas': df_uci['absences'].mean() if 'absences' in df_uci.columns else 0,
        'media_tempo_estudo': df_uci['studytime'].map({'<2h': 1, '2-5h': 2, '5-10h': 3, '>10h': 4}).mean() if 'studytime' in df_uci.columns else 0,
        'distribuicao_genero': df_uci['sex'].value_counts().to_dict() if 'sex' in df_uci.columns else {},
        'correlacao_notas': df_uci[['G1', 'G2', 'G3']].corr().to_dict() if all(col in df_uci.columns for col in ['G1', 'G2', 'G3']) else {}
    }
    return metricas

def calcular_metricas_oulad(df_oulad):
    """Calcula métricas principais para o dataset OULAD"""
    if df_oulad.empty:
        return {}
    
    metricas = {
        'total_estudantes': df_oulad['id_student'].nunique() if 'id_student' in df_oulad.columns else len(df_oulad),
        'media_cliques': df_oulad['clicks'].mean() if 'clicks' in df_oulad.columns else 0,
        'taxa_aprovacao': (df_oulad['final_result'] == 'Pass').mean() * 100 if 'final_result' in df_oulad.columns else 0,
        'distribuicao_genero': df_oulad.groupby('gender')['id_student'].nunique().to_dict() if 'gender' in df_oulad.columns and 'id_student' in df_oulad.columns else {},
        'distribuicao_idade': df_oulad.groupby('age_band')['id_student'].nunique().to_dict() if 'age_band' in df_oulad.columns and 'id_student' in df_oulad.columns else {},
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
        
        # Carregar métricas dinâmicas
        metricas_uci = obter_metricas_principais_uci()
        metricas_oulad = obter_metricas_principais_oulad()
        
        st.markdown("### 📚 Sobre os Datasets")
        st.markdown(f"""
        **📚 UCI Dataset:**
        - Escolas públicas portuguesas
        - {metricas_uci['total_estudantes']:,} estudantes
        - Dados demográficos e acadêmicos
        - Análise de fatores de sucesso
        """)
        
        st.markdown(f"""
        **🌐 OULAD Dataset:**
        - Plataforma de aprendizado online
        - {metricas_oulad['total_estudantes']:,} estudantes
        - Dados de engajamento digital
        - Análise de atividades online
        """)
        
        st.markdown("---")
        st.markdown("### 📈 Métricas Rápidas")
        
        # Métricas UCI
        st.metric(
            "🎓 UCI - Aprovação",
            f"{metricas_uci['taxa_aprovacao']:.1f}%",
            help="Taxa de aprovação nas escolas públicas"
        )
        
        st.metric(
            "📊 UCI - Média Notas",
            f"{metricas_uci['media_nota_final']:.1f}",
            help="Média das notas finais"
        )
        
        # Métricas OULAD
        st.metric(
            "🌐 OULAD - Aprovação",
            f"{metricas_oulad['taxa_aprovacao']:.1f}%",
            help="Taxa de aprovação na plataforma online"
        )
        
        st.metric(
            "🖱️ OULAD - Engajamento",
            f"{metricas_oulad['media_cliques']:.1f}",
            help="Média de cliques por estudante"
        )
        
        st.markdown("---")
        st.markdown("### 💡 Principais Insights")
        
        # Insights dinâmicos baseados nos dados reais
        insights_text = []
        
        if metricas_uci['correlacao_g1_g3'] > 0.7:
            insights_text.append(f"**Correlação forte** entre notas bimestrais e finais ({metricas_uci['correlacao_g1_g3']:.2f})")
        
        if metricas_uci['distribuicao_genero']:
            genero_maioria = max(metricas_uci['distribuicao_genero'], key=metricas_uci['distribuicao_genero'].get)
            insights_text.append(f"**Gênero predominante**: {genero_maioria} ({metricas_uci['distribuicao_genero'][genero_maioria]:.1f}%)")
        
        if metricas_uci['media_faltas'] > 0:
            insights_text.append(f"**Média de faltas**: {metricas_uci['media_faltas']:.1f} por estudante")
        
        if metricas_uci['media_tempo_estudo'] > 0:
            insights_text.append(f"**Tempo de estudo médio**: {metricas_uci['media_tempo_estudo']:.1f}h/semana")
        
        if metricas_oulad['atividade_mais_comum'] != 'N/A':
            insights_text.append(f"**Atividade mais comum**: {metricas_oulad['atividade_mais_comum']}")
        
        if insights_text:
            for insight in insights_text:
                st.markdown(f"- {insight}")
        else:
            st.markdown("""
            - **Correlação forte** entre notas bimestrais e finais
            - **Gênero influencia** desempenho acadêmico
            - **Faltas impactam** negativamente o desempenho
            - **Tempo de estudo** ideal: 5-10h/semana
            - **Atividades online** mais efetivas: outcontent, forumng
            """)
        
        st.markdown("---")
        st.markdown("### ℹ️ Informações")
        st.markdown("**Mestrado em Tecnologia Educacional - UFC**")
    
    return None, None  # Retorna None para manter compatibilidade

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
    """Retorna insights principais do dataset UCI baseados em dados reais"""
    metricas = obter_metricas_principais_uci()
    
    insights = []
    
    # Correlação forte
    if metricas['correlacao_g1_g3'] > 0.7 and metricas['correlacao_g2_g3'] > 0.7:
        insights.append(f"🎯 **Correlação Forte**: Notas do 1º e 2º bimestre têm correlação de {metricas['correlacao_g1_g3']:.2f} e {metricas['correlacao_g2_g3']:.2f} com a nota final")
    
    # Gênero
    if metricas['distribuicao_genero']:
        genero_maioria = max(metricas['distribuicao_genero'], key=metricas['distribuicao_genero'].get)
        genero_menor = min(metricas['distribuicao_genero'], key=metricas['distribuicao_genero'].get)
        insights.append(f"👥 **Gênero**: Estudantes do sexo {genero_maioria} representam {metricas['distribuicao_genero'][genero_maioria]:.1f}% vs {genero_menor} com {metricas['distribuicao_genero'][genero_menor]:.1f}%")
    
    # Consumo de álcool
    if metricas['estudantes_alcool_baixo'] > 0:
        insights.append(f"🍷 **Consumo de Álcool**: {metricas['estudantes_alcool_baixo']:.1f}% dos estudantes têm baixo consumo, com melhor desempenho acadêmico")
    
    # Tempo de estudo
    if metricas['media_tempo_estudo'] > 0:
        insights.append(f"📚 **Tempo de Estudo**: Média de {metricas['media_tempo_estudo']:.1f}h/semana por estudante")
    
    # Faltas
    if metricas['media_faltas'] > 0:
        insights.append(f"❌ **Faltas**: Média de {metricas['media_faltas']:.1f} faltas por estudante")
    
    # Taxa de aprovação
    if metricas['taxa_aprovacao'] > 0:
        insights.append(f"✅ **Aprovação**: Taxa de aprovação de {metricas['taxa_aprovacao']:.1f}%")
    
    # Média de notas
    if metricas['media_nota_final'] > 0:
        insights.append(f"📊 **Desempenho**: Média de notas finais de {metricas['media_nota_final']:.1f}")
    
    return {
        'titulo': '📚 Principais Insights - Dataset UCI',
        'insights': insights if insights else [
            "🎯 **Correlação Forte**: Notas do 1º e 2º bimestre têm correlação forte com a nota final",
            "👥 **Gênero**: Distribuição equilibrada entre gêneros",
            "📚 **Tempo de Estudo**: Fator importante para o desempenho acadêmico",
            "❌ **Faltas**: Impactam negativamente o desempenho",
            "👨‍👩‍👧‍👦 **Família**: Escolaridade dos pais influencia o desempenho dos filhos"
        ]
    }

def obter_insights_oulad():
    """Retorna insights principais do dataset OULAD baseados em dados reais"""
    metricas = obter_metricas_principais_oulad()
    
    insights = []
    
    # Demografia
    if metricas['distribuicao_genero']:
        genero_maioria = max(metricas['distribuicao_genero'], key=metricas['distribuicao_genero'].get)
        insights.append(f"👥 **Demografia**: {metricas['distribuicao_genero'][genero_maioria]:.1f}% são do sexo {genero_maioria}")
    
    if metricas['faixa_etaria_principal'] != 'N/A':
        insights.append(f"👥 **Faixa Etária**: Faixa etária predominante de {metricas['faixa_etaria_principal']}")
    
    # Desempenho
    if metricas['taxa_aprovacao'] > 0:
        insights.append(f"🏆 **Alto Desempenho**: {metricas['taxa_aprovacao']:.1f}% de aprovação")
    
    if metricas['estudantes_distincao'] > 0:
        insights.append(f"🏆 **Distinção**: {metricas['estudantes_distincao']:.1f}% obtendo distinção")
    
    # Engajamento
    if metricas['media_cliques'] > 0:
        insights.append(f"🖱️ **Engajamento**: Média de {metricas['media_cliques']:.1f} cliques por estudante, indicando engajamento moderado")
    
    # Atividades
    if metricas['atividade_mais_comum'] != 'N/A':
        insights.append(f"📚 **Atividades**: '{metricas['atividade_mais_comum']}' é a atividade mais realizada")
    
    # Região
    if metricas['regiao_principal'] != 'N/A':
        insights.append(f"🌍 **Região**: {metricas['regiao_principal']} concentra a maior parte dos estudantes")
    
    # Distribuição de resultados
    if metricas['estudantes_reprovados'] > 0:
        insights.append(f"📊 **Distribuição**: Aprovação supera largamente outras categorias (reprovação: {metricas['estudantes_reprovados']:.1f}%)")
    
    # Total de estudantes
    if metricas['total_estudantes'] > 0:
        insights.append(f"👥 **Total**: {metricas['total_estudantes']:,} estudantes analisados")
    
    return {
        'titulo': '🌐 Principais Insights - Dataset OULAD',
        'insights': insights if insights else [
            "👥 **Demografia**: Distribuição equilibrada entre gêneros",
            "🏆 **Alto Desempenho**: Boa taxa de aprovação geral",
            "🖱️ **Engajamento**: Nível moderado de engajamento na plataforma",
            "📚 **Atividades**: Diversas atividades disponíveis",
            "🌍 **Região**: Distribuição geográfica variada",
            "📊 **Distribuição**: Resultados positivos predominam"
        ]
    }

# =============================================================================
# FUNÇÕES DE TREINAMENTO SOB DEMANDA
# =============================================================================

def treinar_modelo_uci_on_demand():
    """Treina modelo UCI sob demanda com progresso e salvamento automático"""
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.model_selection import train_test_split
        import pickle
        
        # Indicador de progresso (compatível com e sem Streamlit)
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            use_streamlit = True
        except:
            progress_bar = None
            status_text = None
            use_streamlit = False
            print("🔄 Carregando dados UCI...")
        
        if use_streamlit:
            status_text.text("🔄 Carregando dados UCI...")
            progress_bar.progress(20)
        else:
            print("🔄 Carregando dados UCI...")
        
        # Carregar dados UCI
        df_uci = carregar_uci_dados()
        
        if use_streamlit:
            status_text.text("🔄 Preparando dados...")
            progress_bar.progress(40)
        else:
            print("🔄 Preparando dados...")
        
        # Preparar dados como na página 1_uci.py
        Y = df_uci['G3']
        X = df_uci.drop('G3', axis=1)
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        
        if use_streamlit:
            status_text.text("🔄 Treinando modelo RandomForest...")
            progress_bar.progress(60)
        else:
            print("🔄 Treinando modelo RandomForest...")
        
        # Identificar colunas categóricas
        categorical_features = X_train.select_dtypes(include=['object']).columns
        
        # Criar preprocessor
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ],
            remainder='passthrough'
        )
        
        # Criar pipeline
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])
        
        # Treinar modelo
        y_train_encoded = y_train.astype(float)
        model.fit(X_train, y_train_encoded)
        
        if use_streamlit:
            status_text.text("🔄 Salvando modelo...")
            progress_bar.progress(80)
        else:
            print("🔄 Salvando modelo...")
        
        # Salvar modelo
        with open('uci.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        if use_streamlit:
            status_text.text("✅ Modelo UCI treinado e salvo!")
            progress_bar.progress(100)
            
            # Limpar indicadores
            progress_bar.empty()
            status_text.empty()
        else:
            print("✅ Modelo UCI treinado e salvo!")
        
        return model
        
    except Exception as e:
        try:
            st.error(f"Erro ao treinar modelo UCI: {e}")
        except:
            print(f"❌ Erro ao treinar modelo UCI: {e}")
        return None

def treinar_modelo_oulad_on_demand():
    """Treina modelo OULAD sob demanda com progresso e salvamento automático"""
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import OneHotEncoder, LabelEncoder
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.model_selection import train_test_split
        from sklearn.impute import SimpleImputer
        import pickle
        import numpy as np
        
        # Indicador de progresso (compatível com e sem Streamlit)
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            use_streamlit = True
        except:
            progress_bar = None
            status_text = None
            use_streamlit = False
            print("🔄 Carregando dados OULAD...")
        
        if use_streamlit:
            status_text.text("🔄 Carregando dados OULAD...")
            progress_bar.progress(10)
        else:
            print("🔄 Carregando dados OULAD...")
        
        # Carregar dados OULAD
        df_oulad = carregar_oulad_dados()
        
        # Usar amostra para treinamento mais rápido
        if len(df_oulad) > 50000:
            df_oulad = df_oulad.sample(n=50000, random_state=42)
            if use_streamlit:
                st.info("📊 Usando amostra de 50k registros para treinamento mais rápido")
            else:
                print("📊 Usando amostra de 50k registros para treinamento mais rápido")
        
        if use_streamlit:
            status_text.text("🔄 Preparando dados...")
            progress_bar.progress(30)
        else:
            print("🔄 Preparando dados...")
        
        # Preparar dados como na página 2_oulad.py
        Y = df_oulad['final_result']
        X = df_oulad.loc[:, df_oulad.columns != 'final_result']
        
        # Remover colunas irrelevantes
        X = X.drop(['id_student', 'id_site', 'id_assessment', 'code_module', 'code_presentation', 'code_module_y', 'code_module_x'], axis=1, errors='ignore')
        
        if use_streamlit:
            status_text.text("🔄 Dividindo dados...")
            progress_bar.progress(50)
        else:
            print("🔄 Dividindo dados...")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        
        if use_streamlit:
            status_text.text("🔄 Limpando dados de treino...")
            progress_bar.progress(60)
        else:
            print("🔄 Limpando dados de treino...")
        
        # Limpar dados de treino
        nan_rows_train = y_train.isnull()
        X_train_cleaned = X_train[~nan_rows_train].copy()
        y_train_cleaned = y_train[~nan_rows_train].copy()
        
        
        if use_streamlit:
            status_text.text("🔄 Treinando modelo RandomForest...")
            progress_bar.progress(70)
        else:
            print("🔄 Treinando modelo RandomForest...")
        
        # Identificar colunas categóricas e numéricas
        categorical_cols = X_train_cleaned.select_dtypes(include='object').columns
        numerical_cols = X_train_cleaned.select_dtypes(include=[np.number]).columns
        
        # Verificar se há colunas que não são nem categóricas nem numéricas
        all_cols = set(X_train_cleaned.columns)
        processed_cols = set(categorical_cols) | set(numerical_cols)
        remaining_cols = all_cols - processed_cols
        
        if len(remaining_cols) > 0:
            # Adicionar colunas restantes como categóricas
            categorical_cols = list(categorical_cols) + list(remaining_cols)
        
        # Criar preprocessor
        transformers = []
        
        # Adicionar transformador numérico apenas se houver colunas numéricas
        if len(numerical_cols) > 0:
            transformers.append(('num', SimpleImputer(strategy='mean'), numerical_cols))
        
        # Adicionar transformador categórico apenas se houver colunas categóricas
        if len(categorical_cols) > 0:
            transformers.append(('cat', Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))]), categorical_cols))
        
        preprocessor = ColumnTransformer(
            transformers=transformers,
            remainder='passthrough'
        )
        
        # Criar pipeline
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=50, n_jobs=2, max_depth=4, random_state=42))
        ])
        
        # Treinar modelo
        model.fit(X_train_cleaned, y_train_cleaned)
        
        if use_streamlit:
            status_text.text("🔄 Salvando modelo...")
            progress_bar.progress(90)
        else:
            print("🔄 Salvando modelo...")
        
        # Salvar modelo
        with open('oulad.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        if use_streamlit:
            status_text.text("✅ Modelo OULAD treinado e salvo!")
            progress_bar.progress(100)
            
            # Limpar indicadores
            progress_bar.empty()
            status_text.empty()
        else:
            print("✅ Modelo OULAD treinado e salvo!")
        
        return model
        
    except Exception as e:
        try:
            st.error(f"Erro ao treinar modelo OULAD: {e}")
            import traceback
            st.error(f"Traceback: {traceback.format_exc()}")
        except:
            print(f"❌ Erro ao treinar modelo OULAD: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
        return None

@st.cache_resource(ttl=7200)  # Cache por 2 horas
def carregar_modelo_uci():
    """Carrega o modelo UCI com cache ou treina sob demanda"""
    try:
        # Tentar diferentes caminhos para o arquivo pickle
        possible_paths = [
            '../uci.pkl',
            '../../uci.pkl',
            Path(__file__).parent.parents[1] / "uci.pkl",
            'uci.pkl'
        ]
        
        model = None
        for path in possible_paths:
            p = Path(path)
            if p.is_file():
                try:
                    with p.open("rb") as f:
                        model = pickle.load(f)
                    break
                except Exception as e:
                    continue
        
        if model is None:
            st.info("📦 Modelo UCI não encontrado. Treinando modelo automaticamente...")
            return treinar_modelo_uci_on_demand()
        
        return model
    except Exception as e:
        st.warning(f"Erro ao carregar modelo UCI: {e}")
        return None

@st.cache_resource(ttl=7200)  # Cache por 2 horas
def carregar_modelo_oulad():
    """Carrega o modelo OULAD com cache ou treina sob demanda"""
    try:
        # Tentar diferentes caminhos para o arquivo pickle
        possible_paths = [
            '../oulad.pkl',
            '../../oulad.pkl',
            Path(__file__).parent.parents[1] / "oulad.pkl",
            'oulad.pkl'
        ]
        
        model = None
        for path in possible_paths:
            p = Path(path)
            if p.is_file():
                try:
                    with p.open("rb") as f:
                        model = pickle.load(f)
                    break
                except Exception as e:
                    continue
        
        if model is None:
            st.info("📦 Modelo OULAD não encontrado. Treinando modelo automaticamente (pode levar alguns minutos)...")
            return treinar_modelo_oulad_on_demand()
        
        return model
    except Exception as e:
        st.warning(f"Erro ao carregar modelo OULAD: {e}")
        return None

@st.cache_data(ttl=3600)  # Cache por 1 hora (UCI é menor)
def calcular_feature_importance_uci():
    """Calcula feature importance real para UCI com otimizações"""
    try:
        from sklearn.inspection import permutation_importance
        from sklearn.model_selection import train_test_split
        
        # Indicador de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔄 Carregando dados UCI...")
        progress_bar.progress(20)
        
        # Carregar dados UCI
        df_uci = carregar_uci_dados()
        
        status_text.text("🔄 Preparando dados...")
        progress_bar.progress(40)
        
        # Preparar dados como nas páginas individuais
        Y = df_uci['G3']
        X = df_uci.drop('G3', axis=1)
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        
        status_text.text("🔄 Carregando modelo...")
        progress_bar.progress(60)
        
        # Carregar modelo treinado
        model = carregar_modelo_uci()
        if model is None:
            progress_bar.empty()
            status_text.empty()
            return pd.DataFrame()
        
        status_text.text("🔄 Calculando feature importance...")
        progress_bar.progress(80)
        
        # OTIMIZAÇÃO: Usar todos os cores disponíveis
        result = permutation_importance(
            model, X_test, y_test, 
            n_repeats=10,  # Manter 10 para UCI (é pequeno)
            random_state=42, 
            n_jobs=-1  # Usar todos os cores disponíveis
        )
        sorted_idx = result.importances_mean.argsort()
        
        status_text.text("✅ Finalizando...")
        progress_bar.progress(95)
        
        # Criar DataFrame com resultados reais
        features = X_test.columns[sorted_idx]
        importance = result.importances_mean[sorted_idx]
        
        df_result = pd.DataFrame({
            'feature': features,
            'importance': importance
        }).sort_values('importance', ascending=True)
        
        # Limpar indicadores
        progress_bar.empty()
        status_text.empty()
        
        return df_result
        
    except Exception as e:
        st.warning(f"Erro ao calcular feature importance UCI: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=7200)  # Cache por 2 horas (OULAD é pesado)
def calcular_feature_importance_oulad():
    """Calcula feature importance real para OULAD com otimizações"""
    try:
        from sklearn.inspection import permutation_importance
        from sklearn.model_selection import train_test_split
        
        # Indicador de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔄 Carregando dados OULAD...")
        progress_bar.progress(10)
        
        # Carregar dados OULAD
        df_oulad = carregar_oulad_dados()
        
        # AMOSTRAGEM: Usar apenas 50k registros para OULAD (muito mais rápido)
        if len(df_oulad) > 50000:
            df_oulad = df_oulad.sample(n=50000, random_state=42)
            st.info("📊 Usando amostra de 50k registros para análise mais rápida")
        
        status_text.text("🔄 Preparando dados...")
        progress_bar.progress(30)
        
        # Preparar dados como nas páginas individuais
        Y = df_oulad['final_result']
        X = df_oulad.loc[:, df_oulad.columns != 'final_result']
        
        # Remover colunas irrelevantes
        X = X.drop(['id_student', 'id_site', 'id_assessment', 'code_module', 'code_presentation', 'code_module_y', 'code_module_x'], axis=1, errors='ignore')
        
        status_text.text("🔄 Dividindo dados...")
        progress_bar.progress(50)
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        
        # Carregar modelo treinado
        model = carregar_modelo_oulad()
        if model is None:
            progress_bar.empty()
            status_text.empty()
            return pd.DataFrame()
        
        status_text.text("🔄 Limpando dados de teste...")
        progress_bar.progress(70)
        
        # Limpar dados de teste
        nan_rows_test = y_test.isnull()
        X_test_cleaned = X_test[~nan_rows_test].copy()
        y_test_cleaned = y_test[~nan_rows_test].copy()
        
        status_text.text("🔄 Calculando feature importance...")
        progress_bar.progress(85)
        
        # OTIMIZAÇÃO: Menos repetições e mais jobs
        result = permutation_importance(
            model, X_test_cleaned, y_test_cleaned, 
            n_repeats=5,  # Reduzido de 10 para 5
            random_state=42, 
            n_jobs=-1  # Usar todos os cores disponíveis
        )
        sorted_idx = result.importances_mean.argsort()
        
        status_text.text("✅ Finalizando...")
        progress_bar.progress(95)
        
        # Criar DataFrame com resultados reais
        features = X_test_cleaned.columns[sorted_idx]
        importance = result.importances_mean[sorted_idx]
        
        df_result = pd.DataFrame({
            'feature': features,
            'importance': importance
        }).sort_values('importance', ascending=True)
        
        # Limpar indicadores
        progress_bar.empty()
        status_text.empty()
        
        return df_result
        
    except Exception as e:
        st.warning(f"Erro ao calcular feature importance OULAD: {e}")
        return pd.DataFrame()

def criar_grafico_feature_importance_uci():
    """Cria gráfico de feature importance para UCI"""
    df_importance = calcular_feature_importance_uci()
    if df_importance.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(df_importance['feature'], df_importance['importance'], color='skyblue')
    ax.set_title('Importância das Features - Dataset UCI', fontsize=14, fontweight='bold')
    ax.set_xlabel('Importância')
    ax.set_ylabel('Features')
    
    # Adicionar valores nas barras
    for i, (bar, importance) in enumerate(zip(bars, df_importance['importance'])):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{importance:.3f}', va='center', fontsize=10)
    
    plt.tight_layout()
    return fig

def criar_grafico_feature_importance_oulad():
    """Cria gráfico de feature importance para OULAD"""
    df_importance = calcular_feature_importance_oulad()
    if df_importance.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(df_importance['feature'], df_importance['importance'], color='lightcoral')
    ax.set_title('Importância das Features - Dataset OULAD', fontsize=14, fontweight='bold')
    ax.set_xlabel('Importância')
    ax.set_ylabel('Features')
    
    # Adicionar valores nas barras
    for i, (bar, importance) in enumerate(zip(bars, df_importance['importance'])):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{importance:.3f}', va='center', fontsize=10)
    
    plt.tight_layout()
    return fig

def criar_secao_pygwalker():
    """Cria seção opcional para PyGWalker com seleção de dataset"""
    st.markdown("---")
    st.markdown("### 🔍 Análise Interativa com PyGWalker")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        dataset_selecionado = st.selectbox(
            "Selecione o dataset para análise:",
            ["UCI", "OULAD"],
            help="Escolha qual dataset analisar interativamente"
        )
    
    with col2:
        usar_pygwalker_uci = st.checkbox(
            "Ativar PyGWalker UCI", 
            value=False,
            help="Permite análise interativa dos dados UCI"
        )

        usar_pygwalker_oulad = st.checkbox(
            "Ativar PyGWalker OULAD", 
            value=False,
            help="Permite análise interativa dos dados OULAD"
        )
    if usar_pygwalker_uci:
        try:
            import pygwalker as pyg
            from pygwalker.api.streamlit import StreamlitRenderer
            
            # Carregar dados baseado na seleção
            if dataset_selecionado == "UCI":
                if 'df_uci' in st.session_state and not st.session_state['df_uci'].empty:
                    st.info("📊 Carregando PyGWalker com dados UCI...")
                    df = st.session_state['df_uci']
                else:
                    st.info("📊 Carregando dados UCI do arquivo...")
                    df = carregar_uci_dados()
            else:  # OULAD
                if 'df_oulad' in st.session_state and not st.session_state['df_oulad'].empty:
                    st.info("📊 Carregando PyGWalker com dados OULAD...")
                    df = st.session_state['df_oulad']
                else:
                    st.info("📊 Carregando dados OULAD do arquivo...")
                    df = carregar_oulad_dados()
            
            # Verificar se os dados foram carregados
            if df is not None and not df.empty:
                # Criar renderer do PyGWalker
                renderer = StreamlitRenderer(df, spec="./gw0.json", debug=False)
                renderer.render_explore()
            else:
                st.warning(f"⚠️ Nenhum dado disponível para {dataset_selecionado}. Verifique se os arquivos de dados existem.")
                
        except ImportError:
            st.error("❌ PyGWalker não está instalado. Execute: `pip install pygwalker`")
        except Exception as e:
            st.error(f"❌ Erro ao carregar PyGWalker: {e}")
    else:
        st.info(f"💡 Marque a opção acima para ativar a análise interativa com PyGWalker para o dataset {dataset_selecionado}")

    if usar_pygwalker_oulad:
        try:
            import pygwalker as pyg
            from pygwalker.api.streamlit import StreamlitRenderer
            
            # Verificar se há dados disponíveis
            if 'df_oulad' in st.session_state and not st.session_state['df_oulad'].empty:
                st.info("📊 Carregando PyGWalker com dados OULAD...")
                df = st.session_state['df_oulad']
                
                # Criar renderer do PyGWalker
                renderer = StreamlitRenderer(df, spec="./gw0.json", debug=False)
                renderer.render_explore()
                
            else:
                st.warning("⚠️ Nenhum dado disponível para análise interativa. Navegue para as páginas de análise primeiro.")
            
        except ImportError:
            st.error("❌ PyGWalker não está instalado. Execute: `pip install pygwalker`")
        except Exception as e:
            st.error(f"❌ Erro ao carregar PyGWalker: {e}")
        else:
            st.info("💡 Marque a opção acima para ativar a análise interativa com PyGWalker")

# =============================================================================
# FUNÇÕES PARA TEMPLATE DE FEATURE IMPORTANCE
# =============================================================================

def traduzir_nome_feature(feature: str, dataset_origem: str) -> str:
    """Traduz nomes de features para português brasileiro"""
    # Mapeamento de traduções para features comuns
    traducoes = {
        # UCI features
        'failures': 'reprovacoes',
        'absences': 'faltas',
        'G1': 'nota_1bim',
        'G2': 'nota_2bim',
        'G3': 'nota_final',
        'studytime': 'tempo_estudo',
        'goout': 'saidas',
        'Dalc': 'alcool_dia',
        'Walc': 'alcool_fds',
        'freetime': 'tempo_livre',
        'health': 'saude',
        'age': 'idade',
        'sex': 'sexo',
        'school': 'escola',
        'address': 'endereco',
        'famsize': 'tamanho_familia',
        'Pstatus': 'status_pais',
        'Medu': 'educacao_mae',
        'Fedu': 'educacao_pai',
        'Mjob': 'trabalho_mae',
        'Fjob': 'trabalho_pai',
        'reason': 'motivo_escola',
        'guardian': 'responsavel',
        'traveltime': 'tempo_viagem',
        
        # OULAD features
        'sum_click': 'cliques',
        'score': 'pontuacao',
        'studied_credits': 'creditos_estudados',
        'num_of_prev_attempts': 'tentativas_anteriores',
        'date': 'data',
        'date_submitted': 'data_submissao',
        'clicks': 'cliques',
        'final_result': 'resultado_final',
        'gender': 'genero',
        'region': 'regiao',
        'highest_education': 'educacao_superior',
        'imd_band': 'banda_imd',
        'age_band': 'faixa_etaria',
        'disability': 'deficiencia',
        'activity_type': 'tipo_atividade',
        'assessment_type': 'tipo_avaliacao',
        'weight': 'peso',
        'module_presentation_length': 'duracao_modulo',
    }
    
    # Tentar traduzir, se não existir mapeamento, retornar o original em lowercase
    return traducoes.get(feature, feature.lower().replace('_', '_'))

def gerar_template_unificado() -> pd.DataFrame:
    """Gera template unificado com top 3 features de UCI e OULAD"""
    try:
        # Get top 3 features from UCI
        df_importance_uci = calcular_feature_importance_uci()
        top_features_uci = df_importance_uci.nlargest(3, 'importance')['feature'].tolist() if not df_importance_uci.empty else []
        
        # Get top 3 features from OULAD
        df_importance_oulad = calcular_feature_importance_oulad()
        top_features_oulad = df_importance_oulad.nlargest(3, 'importance')['feature'].tolist() if not df_importance_oulad.empty else []
        
        # Build template with name field first
        template_data = {'nome_aluno': [''] * 10}
        
        # Store mapping for validation later
        feature_mapping = {}
        
        # Add UCI features translated to Portuguese, without prefix
        for feature in top_features_uci:
            translated = traduzir_nome_feature(feature, 'uci')
            # If translation conflicts, add _uci suffix
            if translated in template_data or translated in feature_mapping:
                translated = f"{translated}_uci"
            template_data[translated] = [np.nan] * 10
            feature_mapping[translated] = ('uci', feature)
        
        # Add OULAD features translated to Portuguese, without prefix
        for feature in top_features_oulad:
            translated = traduzir_nome_feature(feature, 'oulad')
            # If translation conflicts, add _oulad suffix
            if translated in template_data or translated in feature_mapping:
                translated = f"{translated}_oulad"
            template_data[translated] = [np.nan] * 10
            feature_mapping[translated] = ('oulad', feature)
        
        # Add result column
        template_data['resultado_final'] = [np.nan] * 10
        
        df_template = pd.DataFrame(template_data)
        
        # Add example row with placeholder values
        df_template.loc[0, 'nome_aluno'] = 'João Silva'
        
        # Add example values based on typical feature ranges
        for col in df_template.columns:
            if col == 'nome_aluno':
                continue
            elif col == 'resultado_final':
                df_template.loc[0, col] = 'Pass'
            elif 'reprovacoes' in col or 'faltas' in col or 'tentativas' in col:
                df_template.loc[0, col] = 0
            elif 'nota' in col or 'pontuacao' in col:
                df_template.loc[0, col] = 10.0
            elif 'cliques' in col or 'creditos' in col:
                df_template.loc[0, col] = 50
            elif 'tempo' in col:
                df_template.loc[0, col] = 2
            else:
                df_template.loc[0, col] = 'Exemplo'
        
        # Store mapping as metadata (could be saved separately if needed)
        df_template.attrs['feature_mapping'] = feature_mapping
        
        return df_template
        
    except Exception as e:
        st.error(f"Erro ao gerar template unificado: {e}")
        return pd.DataFrame()

def gerar_template_features(dataset_tipo: str) -> pd.DataFrame:
    """Gera template com as 2 features mais importantes do dataset selecionado"""
    try:
        # Obter feature importance baseado no dataset
        if dataset_tipo.lower() == 'uci':
            df_importance = calcular_feature_importance_uci()
        elif dataset_tipo.lower() == 'oulad':
            df_importance = calcular_feature_importance_oulad()
        else:
            raise ValueError(f"Dataset tipo '{dataset_tipo}' não reconhecido. Use 'uci' ou 'oulad'")
        
        if df_importance.empty:
            st.warning(f"Não foi possível obter feature importance para {dataset_tipo}")
            return pd.DataFrame()
        
        # Pegar as 2 features mais importantes (maior importance)
        top_features = df_importance.nlargest(2, 'importance')['feature'].tolist()
        
        # Criar template DataFrame
        template_data = {
            feature: [np.nan] * 10 for feature in top_features
        }
        template_data['resultado_final'] = [np.nan] * 10
        
        df_template = pd.DataFrame(template_data)
        
        # Adicionar algumas linhas de exemplo com valores placeholder
        if dataset_tipo.lower() == 'uci':
            # Exemplos baseados no dataset UCI
            if len(top_features) >= 1:
                df_template.loc[0, top_features[0]] = 1.0  # Exemplo de valor numérico
            if len(top_features) >= 2:
                df_template.loc[0, top_features[1]] = 2.0
            df_template.loc[0, 'resultado_final'] = 10.0  # Exemplo de nota
        else:  # OULAD
            # Exemplos baseados no dataset OULAD
            if len(top_features) >= 1:
                df_template.loc[0, top_features[0]] = 'Pass'  # Exemplo de categoria
            if len(top_features) >= 2:
                df_template.loc[0, top_features[1]] = 1.0
            df_template.loc[0, 'resultado_final'] = 'Pass'
        
        return df_template
        
    except Exception as e:
        st.error(f"Erro ao gerar template: {e}")
        return pd.DataFrame()

def converter_template_para_excel(df_template: pd.DataFrame) -> bytes:
    """Converte DataFrame template para formato Excel (bytes)"""
    try:
        import io
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_template.to_excel(writer, sheet_name='Template', index=False)
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Erro ao converter template para Excel: {e}")
        return b''

def validar_template_usuario(df_usuario: pd.DataFrame, df_template: pd.DataFrame = None) -> tuple[bool, str]:
    """Valida se o template preenchido pelo usuário está correto"""
    try:
        # Verificar se tem a coluna resultado_final
        if 'resultado_final' not in df_usuario.columns:
            return False, "Coluna 'resultado_final' não encontrada no arquivo"
        
        # Verificar se tem a coluna nome_aluno (para template unificado)
        if 'nome_aluno' not in df_usuario.columns:
            return False, "Coluna 'nome_aluno' não encontrada no arquivo"
        
        # Se df_template foi fornecido, verificar features específicas
        if df_template is not None:
            expected_features = [col for col in df_template.columns if col not in ['resultado_final', 'nome_aluno']]
            missing_features = [col for col in expected_features if col not in df_usuario.columns]
            
            if missing_features:
                return False, f"Colunas de features esperadas não encontradas: {missing_features}"
        
        # Verificar se tem dados (não está vazio)
        if df_usuario.empty:
            return False, "Arquivo está vazio"
        
        # Verificar se tem pelo menos algumas linhas com dados válidos
        non_empty_rows = df_usuario.dropna(how='all').shape[0]
        if non_empty_rows < 3:
            return False, "Arquivo deve ter pelo menos 3 linhas com dados válidos"
        
        # Verificar se tem pelo menos algumas features além de nome e resultado
        feature_cols = [col for col in df_usuario.columns if col not in ['nome_aluno', 'resultado_final']]
        if len(feature_cols) < 2:
            return False, "Template deve ter pelo menos 2 features além de nome_aluno e resultado_final"
        
        return True, "Template válido"
        
    except Exception as e:
        return False, f"Erro na validação: {e}"

def realizar_eda_automatica(df_usuario: pd.DataFrame) -> dict:
    """Realiza EDA automática no dataset do usuário"""
    try:
        from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
        from sklearn.preprocessing import OneHotEncoder, LabelEncoder
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, classification_report
        from sklearn.inspection import permutation_importance
        import numpy as np
        
        # Preparar dados - remover nome_aluno se existir
        target_col = 'resultado_final'
        y = df_usuario[target_col]
        X = df_usuario.drop([target_col, 'nome_aluno'], axis=1, errors='ignore')
        
        # Detectar tipo de problema (regressão vs classificação)
        is_regression = pd.api.types.is_numeric_dtype(y) and y.nunique() > 10
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Preparar preprocessamento
        categorical_features = X_train.select_dtypes(include=['object']).columns
        numerical_features = X_train.select_dtypes(include=[np.number]).columns
        
        # Criar preprocessor
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', 'passthrough', numerical_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ]
        )
        
        # Treinar modelo apropriado
        if is_regression:
            model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
            ])
            y_train_encoded = y_train.astype(float)
            y_test_encoded = y_test.astype(float)
        else:
            model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
            ])
            # Para classificação, usar LabelEncoder se necessário
            if not pd.api.types.is_numeric_dtype(y_train):
                le = LabelEncoder()
                y_train_encoded = le.fit_transform(y_train)
                y_test_encoded = le.transform(y_test)
            else:
                y_train_encoded = y_train
                y_test_encoded = y_test
        
        # Treinar modelo
        model.fit(X_train, y_train_encoded)
        
        # Fazer predições
        predictions = model.predict(X_test)
        
        # Calcular métricas
        if is_regression:
            mae = mean_absolute_error(y_test_encoded, predictions)
            rmse = np.sqrt(mean_squared_error(y_test_encoded, predictions))
            r2 = r2_score(y_test_encoded, predictions)
            metrics = {
                'mae': mae,
                'rmse': rmse,
                'r2': r2,
                'type': 'regression'
            }
        else:
            accuracy = accuracy_score(y_test_encoded, predictions)
            metrics = {
                'accuracy': accuracy,
                'type': 'classification',
                'classification_report': classification_report(y_test_encoded, predictions, output_dict=True)
            }
        
        # Calcular feature importance
        try:
            # Usar permutation importance
            result = permutation_importance(
                model, X_test, y_test_encoded, 
                n_repeats=5, random_state=42, n_jobs=-1
            )
            
            feature_importance = pd.DataFrame({
                'feature': X_test.columns,
                'importance': result.importances_mean
            }).sort_values('importance', ascending=False)
        except:
            # Fallback para feature_importances_ do modelo
            if hasattr(model.named_steps[list(model.named_steps.keys())[-1]], 'feature_importances_'):
                feature_importance = pd.DataFrame({
                    'feature': X_test.columns,
                    'importance': model.named_steps[list(model.named_steps.keys())[-1]].feature_importances_
                }).sort_values('importance', ascending=False)
            else:
                feature_importance = pd.DataFrame()
        
        # Estatísticas descritivas
        stats = {
            'shape': df_usuario.shape,
            'missing_values': df_usuario.isnull().sum().to_dict(),
            'dtypes': df_usuario.dtypes.to_dict(),
            'numeric_summary': df_usuario.select_dtypes(include=[np.number]).describe().to_dict() if not df_usuario.select_dtypes(include=[np.number]).empty else {},
            'categorical_summary': df_usuario.select_dtypes(include=['object']).describe().to_dict() if not df_usuario.select_dtypes(include=['object']).empty else {}
        }
        
        return {
            'model': model,
            'metrics': metrics,
            'feature_importance': feature_importance,
            'predictions': predictions,
            'y_test': y_test_encoded,
            'stats': stats,
            'is_regression': is_regression
        }
        
    except Exception as e:
        st.error(f"Erro na EDA automática: {e}")
        return {}
