from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import time
from .carregar_dados import carregar_uci_dados, carregar_oulad_dados

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
        
        st.markdown("### 📚 Sobre os Datasets")
        st.markdown("""
        **📚 UCI Dataset:**
        - Escolas públicas portuguesas
        - 1,044 estudantes
        - Dados demográficos e acadêmicos
        - Análise de fatores de sucesso
        """)
        
        st.markdown("""
        **🌐 OULAD Dataset:**
        - Plataforma de aprendizado online
        - 28,000 estudantes
        - Dados de engajamento digital
        - Análise de atividades online
        """)
        
        st.markdown("---")
        st.markdown("### 📈 Métricas Rápidas")
        
        # Métricas UCI
        st.metric(
            "🎓 UCI - Aprovação",
            "67.3%",
            help="Taxa de aprovação nas escolas públicas"
        )
        
        st.metric(
            "📊 UCI - Média Notas",
            "10.4",
            help="Média das notas finais"
        )
        
        # Métricas OULAD
        st.metric(
            "🌐 OULAD - Aprovação",
            "78.5%",
            help="Taxa de aprovação na plataforma online"
        )
        
        st.metric(
            "🖱️ OULAD - Engajamento",
            "4.65",
            help="Média de cliques por estudante"
        )
        
        st.markdown("---")
        st.markdown("### 💡 Principais Insights")
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

@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_modelo_uci():
    """Carrega o modelo UCI com cache"""
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
            raise FileNotFoundError(f"Arquivo uci.pkl não encontrado em nenhum dos caminhos: {possible_paths}")
        
        return model
    except Exception as e:
        st.warning(f"Erro ao carregar modelo UCI: {e}")
        return None

@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_modelo_oulad():
    """Carrega o modelo OULAD com cache"""
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
            raise FileNotFoundError(f"Arquivo oulad.pkl não encontrado em nenhum dos caminhos: {possible_paths}")
        
        return model
    except Exception as e:
        st.warning(f"Erro ao carregar modelo OULAD: {e}")
        return None

@st.cache_data(ttl=1800)  # Cache por 30 minutos
def calcular_feature_importance_uci():
    """Calcula feature importance real para UCI usando permutation_importance"""
    try:
        from sklearn.inspection import permutation_importance
        from sklearn.model_selection import train_test_split
        
        # Carregar dados UCI
        df_uci = carregar_uci_dados()
        
        # Preparar dados como nas páginas individuais
        Y = df_uci['G3']
        X = df_uci.drop('G3', axis=1)
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        
        # Carregar modelo treinado
        model = carregar_modelo_uci()
        if model is None:
            return pd.DataFrame()
        
        # Calcular permutation importance
        result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2)
        sorted_idx = result.importances_mean.argsort()
        
        # Criar DataFrame com resultados reais
        features = X_test.columns[sorted_idx]
        importance = result.importances_mean[sorted_idx]
        
        return pd.DataFrame({
            'feature': features,
            'importance': importance
        }).sort_values('importance', ascending=True)
        
    except Exception as e:
        st.warning(f"Erro ao calcular feature importance UCI: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=1800)  # Cache por 30 minutos
def calcular_feature_importance_oulad():
    """Calcula feature importance real para OULAD usando permutation_importance"""
    try:
        from sklearn.inspection import permutation_importance
        from sklearn.model_selection import train_test_split
        
        # Carregar dados OULAD
        df_oulad = carregar_oulad_dados()
        
        # Preparar dados como nas páginas individuais
        Y = df_oulad['final_result']
        X = df_oulad.loc[:, df_oulad.columns != 'final_result']
        
        # Remover colunas irrelevantes
        X = X.drop(['id_student', 'id_site', 'id_assessment', 'code_module', 'code_presentation', 'code_module_y', 'code_module_x'], axis=1, errors='ignore')
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        
        # Carregar modelo treinado
        model = carregar_modelo_oulad()
        if model is None:
            return pd.DataFrame()
        
        # Limpar dados de teste
        nan_rows_test = y_test.isnull()
        X_test_cleaned = X_test[~nan_rows_test].copy()
        y_test_cleaned = y_test[~nan_rows_test].copy()
        
        # Calcular permutation importance
        result = permutation_importance(model, X_test_cleaned, y_test_cleaned, n_repeats=10, random_state=42, n_jobs=2)
        sorted_idx = result.importances_mean.argsort()
        
        # Criar DataFrame com resultados reais
        features = X_test_cleaned.columns[sorted_idx]
        importance = result.importances_mean[sorted_idx]
        
        return pd.DataFrame({
            'feature': features,
            'importance': importance
        }).sort_values('importance', ascending=True)
        
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
        usar_pygwalker = st.checkbox(
            "Ativar PyGWalker", 
            value=False,
            help="Permite análise interativa dos dados"
        )
    
    if usar_pygwalker:
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
