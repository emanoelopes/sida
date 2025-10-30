"""
Módulo para unificar datasets UCI e OULAD.

Este módulo contém funções para:
- Carregar e processar dados UCI e OULAD
- Mapear colunas para nomes em português
- Agregar dados OULAD (múltiplas linhas por estudante)
- Normalizar variável target (resultado_final)
- Tratar dados ausentes com estratégias específicas
- Validar e salvar dataset unificado
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import warnings

warnings.filterwarnings('ignore')

# Importar funções de carregamento existentes
from .carregar_dados import carregar_dados_uci_raw, carregar_dados_oulad_raw


# ============================================================================
# Funções de Normalização de Target
# ============================================================================

def normalizar_target_uci(valor_g3: float) -> float:
    """
    Converte G3 (0-20) para escala 0-10.
    
    Args:
        valor_g3: Nota G3 original (escala 0-20)
    
    Returns:
        Nota normalizada (escala 0-10)
    """
    if pd.isna(valor_g3):
        return np.nan
    return valor_g3 / 2.0


def normalizar_target_oulad(final_result: str) -> float:
    """
    Converte resultado categórico OULAD para escala numérica 0-10.
    
    Args:
        final_result: Resultado categórico ('Distinction', 'Pass', 'Fail', 'Withdrawn')
    
    Returns:
        Nota normalizada (escala 0-10)
    """
    mapeamento = {
        'Distinction': 9.0,
        'Pass': 7.0,
        'Fail': 3.0,
        'Withdrawn': 0.0
    }
    return mapeamento.get(str(final_result), np.nan)


# ============================================================================
# Funções de Mapeamento de Colunas
# ============================================================================

def mapear_colunas_uci(df_uci: pd.DataFrame) -> pd.DataFrame:
    """
    Renomeia e transforma colunas UCI para português.
    
    Args:
        df_uci: DataFrame com dados UCI brutos
    
    Returns:
        DataFrame com colunas renomeadas e transformadas
    """
    df = df_uci.copy()
    
    # Mapeamento de colunas comuns (harmonizadas)
    mapeamento_comum = {
        'sex': 'genero',
        'age': 'idade',
        'address': 'regiao',
        'absences': 'faltas',
        'failures': 'tentativas_anteriores'
    }
    
    # Renomear colunas comuns
    df = df.rename(columns=mapeamento_comum)
    
    # Normalizar target (G3 -> resultado_final)
    if 'G3' in df.columns:
        df['resultado_final'] = df['G3'].apply(normalizar_target_uci)
    
    # Transformar gênero
    if 'genero' in df.columns:
        df['genero'] = df['genero'].map({'M': 'Masculino', 'F': 'Feminino'})
    
    # Transformar região (U/R -> mais descritivo)
    if 'regiao' in df.columns:
        df['regiao'] = df['regiao'].map({'U': 'Urbana', 'R': 'Rural'})
    
    # Renomear colunas UCI específicas (com prefixo uci_)
    mapeamento_uci = {
        'Medu': 'uci_educacao_mae',
        'Fedu': 'uci_educacao_pai',
        'Mjob': 'uci_trabalho_mae',
        'Fjob': 'uci_trabalho_pai',
        'Dalc': 'uci_alcool_semana',
        'Walc': 'uci_alcool_fds',
        'studytime': 'uci_tempo_estudo',
        'G1': 'uci_nota_periodo1',
        'G2': 'uci_nota_periodo2',
        'schoolsup': 'uci_suporte_escolar',
        'famsup': 'uci_suporte_familiar',
        'health': 'uci_saude',
        'freetime': 'uci_tempo_livre',
        'romantic': 'uci_relacionamento',
        'activities': 'uci_atividades',
        'nursery': 'uci_creche',
        'higher': 'uci_educacao_superior',
        'internet': 'uci_internet',
        'famrel': 'uci_relacao_familiar',
        'goout': 'uci_saidas',
        'traveltime': 'uci_tempo_viagem',
        'school': 'uci_escola',
        'reason': 'uci_motivo_escola',
        'guardian': 'uci_responsavel',
        'famsize': 'uci_tamanho_familia',
        'Pstatus': 'uci_status_pais',
        'paid': 'uci_aulas_pagas'
    }
    
    # Renomear colunas UCI específicas
    for col_old, col_new in mapeamento_uci.items():
        if col_old in df.columns:
            df[col_new] = df[col_old]
            if col_old != col_new:
                df = df.drop(columns=[col_old])
    
    return df


def agregar_oulad_por_estudante(dataframes_oulad: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Agrega dados OULAD em uma linha por estudante.
    
    Args:
        dataframes_oulad: Dicionário com dataframes OULAD brutos
    
    Returns:
        DataFrame agregado com uma linha por estudante
    """
    # Verificar dataframes essenciais
    if 'studentInfo' not in dataframes_oulad:
        raise ValueError("studentInfo não encontrado nos dataframes OULAD")
    
    df_studentinfo = dataframes_oulad['studentInfo'].copy()
    
    # Manter primeira ocorrência de cada estudante do studentInfo (dados demográficos)
    df_studentinfo_first = df_studentinfo.groupby('id_student').first().reset_index()
    
    # Merge com courses se disponível
    if 'courses' in dataframes_oulad:
        df_courses = dataframes_oulad['courses'].copy()
        df_studentinfo_first = pd.merge(
            df_studentinfo_first, 
            df_courses, 
            on=['code_module', 'code_presentation'], 
            how='left'
        )
    
    # Agregar cliques por estudante (se disponível)
    if 'studentVle' in dataframes_oulad and not dataframes_oulad['studentVle'].empty:
        df_studentvle = dataframes_oulad['studentVle'].copy()
        cliques_agg = df_studentvle.groupby('id_student').agg({
            'sum_click': 'sum',
            'date': ['count', 'min', 'max']
        }).reset_index()
        cliques_agg.columns = ['id_student', 'oulad_total_cliques', 'oulad_dias_atividade', 'oulad_primeira_atividade', 'oulad_ultima_atividade']
        
        # Calcular média de cliques por dia
        cliques_agg['oulad_media_cliques_dia'] = (
            cliques_agg['oulad_total_cliques'] / cliques_agg['oulad_dias_atividade'].replace(0, np.nan)
        )
    else:
        # Criar DataFrame vazio com as colunas esperadas
        cliques_agg = pd.DataFrame(columns=['id_student', 'oulad_total_cliques', 'oulad_dias_atividade', 
                                            'oulad_primeira_atividade', 'oulad_ultima_atividade', 'oulad_media_cliques_dia'])
    
    # Agregar avaliações por estudante (se disponível)
    if 'studentAssessment' in dataframes_oulad and not dataframes_oulad['studentAssessment'].empty:
        df_studentassessment = dataframes_oulad['studentAssessment'].copy()
        assessments_agg = df_studentassessment.groupby('id_student').agg({
            'score': ['mean', 'count'],
            'date_submitted': 'min'
        }).reset_index()
        assessments_agg.columns = ['id_student', 'oulad_media_score', 'oulad_num_avaliacoes', 'oulad_primeira_submissao']
    else:
        assessments_agg = pd.DataFrame(columns=['id_student', 'oulad_media_score', 'oulad_num_avaliacoes', 'oulad_primeira_submissao'])
    
    # Processar registros de estudante (se disponível)
    if 'studentRegistration' in dataframes_oulad and not dataframes_oulad['studentRegistration'].empty:
        df_studentregistration = dataframes_oulad['studentRegistration'].copy()
        registration_agg = df_studentregistration.groupby('id_student').agg({
            'date_registration': 'min',
            'date_unregistration': 'max'
        }).reset_index()
        registration_agg.columns = ['id_student', 'oulad_data_registro', 'oulad_data_cancelamento']
    else:
        registration_agg = pd.DataFrame(columns=['id_student', 'oulad_data_registro', 'oulad_data_cancelamento'])
    
    # Juntar todas as agregações
    df_agregado = df_studentinfo_first.copy()
    
    # Merge com cliques (left join para manter todos os estudantes)
    if not cliques_agg.empty:
        df_agregado = pd.merge(df_agregado, cliques_agg, on='id_student', how='left')
    
    # Merge com avaliações
    if not assessments_agg.empty:
        df_agregado = pd.merge(df_agregado, assessments_agg, on='id_student', how='left')
    
    # Merge com registros
    if not registration_agg.empty:
        df_agregado = pd.merge(df_agregado, registration_agg, on='id_student', how='left')
    
    return df_agregado


def mapear_colunas_oulad(df_oulad_agregado: pd.DataFrame) -> pd.DataFrame:
    """
    Renomeia e transforma colunas OULAD agregadas para português.
    
    Args:
        df_oulad_agregado: DataFrame OULAD agregado
    
    Returns:
        DataFrame com colunas renomeadas e transformadas
    """
    df = df_oulad_agregado.copy()
    
    # Mapeamento de colunas comuns (harmonizadas)
    mapeamento_comum = {
        'gender': 'genero',
        'region': 'regiao',
        'age_band': 'idade',
        'num_of_prev_attempts': 'tentativas_anteriores'
    }
    
    # Renomear colunas comuns
    df = df.rename(columns=mapeamento_comum)
    
    # Normalizar target (final_result -> resultado_final)
    if 'final_result' in df.columns:
        df['resultado_final'] = df['final_result'].apply(normalizar_target_oulad)
    
    # Transformar gênero
    if 'genero' in df.columns:
        df['genero'] = df['genero'].map({'M': 'Masculino', 'F': 'Feminino'})
    
    # Renomear colunas OULAD específicas (com prefixo oulad_)
    mapeamento_oulad = {
        'highest_education': 'nivel_educacao',
        'disability': 'oulad_deficiencia',
        'imd_band': 'oulad_imd_band',
        'studied_credits': 'oulad_creditos_estudados',
        'code_module': 'oulad_modulo',
        'code_presentation': 'oulad_apresentacao',
        'module_presentation_length': 'oulad_duracao_curso'
    }
    
    # Renomear colunas OULAD específicas (já podem estar com prefixo oulad_)
    for col_old, col_new in mapeamento_oulad.items():
        if col_old in df.columns:
            if not col_new.startswith('oulad_'):
                col_new = 'oulad_' + col_new
            df[col_new] = df[col_old]
            if col_old != col_new:
                df = df.drop(columns=[col_old])
    
    # As colunas agregadas já começam com oulad_, então não precisam renomear
    
    return df


def adicionar_coluna_origem(df: pd.DataFrame, origem: str) -> pd.DataFrame:
    """
    Adiciona coluna `origem_dado` ao DataFrame.
    
    Args:
        df: DataFrame
        origem: Valor da origem ('UCI' ou 'OULAD')
    
    Returns:
        DataFrame com coluna origem_dado adicionada
    """
    df = df.copy()
    df['origem_dado'] = origem
    return df


# ============================================================================
# Funções de Tratamento de Dados Ausentes
# ============================================================================

def imputar_numerica_por_grupo(df: pd.DataFrame, coluna: str, grupo_cols: List[str] = None) -> pd.Series:
    """
    Imputa coluna numérica usando mediana por grupo.
    
    Args:
        df: DataFrame
        coluna: Nome da coluna numérica a imputar
        grupo_cols: Lista de colunas para agrupar (padrão: ['origem_dado', 'regiao', 'genero'])
    
    Returns:
        Série com valores imputados
    """
    if grupo_cols is None:
        grupo_cols = ['origem_dado', 'regiao', 'genero']
    
    # Filtrar apenas colunas que existem no DataFrame
    grupo_cols = [c for c in grupo_cols if c in df.columns]
    
    serie = df[coluna].copy()
    
    if serie.isna().sum() == 0:
        return serie
    
    # Tentar imputar por grupo
    if len(grupo_cols) > 0:
        # Calcular mediana por grupo
        medianas_grupo = df.groupby(grupo_cols)[coluna].transform('median')
        # Preencher apenas onde há NaN
        mask_nan = serie.isna()
        serie.loc[mask_nan] = medianas_grupo.loc[mask_nan]
    
    # Se ainda houver NaN, usar mediana global
    if serie.isna().sum() > 0:
        mediana_global = df[coluna].median()
        if not pd.isna(mediana_global):
            serie = serie.fillna(mediana_global)
        else:
            # Se mediana também for NaN, usar zero (para contadores)
            serie = serie.fillna(0)
    
    return serie


def imputar_categorica_por_grupo(df: pd.DataFrame, coluna: str, grupo_cols: List[str] = None) -> pd.Series:
    """
    Imputa coluna categórica usando moda por grupo.
    
    Args:
        df: DataFrame
        coluna: Nome da coluna categórica a imputar
        grupo_cols: Lista de colunas para agrupar (padrão: ['origem_dado', 'regiao'])
    
    Returns:
        Série com valores imputados
    """
    if grupo_cols is None:
        grupo_cols = ['origem_dado', 'regiao']
    
    # Filtrar apenas colunas que existem no DataFrame
    grupo_cols = [c for c in grupo_cols if c in df.columns]
    
    serie = df[coluna].copy()
    
    if serie.isna().sum() == 0:
        return serie
    
    # Tentar imputar por grupo
    if len(grupo_cols) > 0:
        def get_mode(x):
            mode_vals = x.mode()
            return mode_vals.iloc[0] if len(mode_vals) > 0 else None
        
        modas_grupo = df.groupby(grupo_cols)[coluna].transform(get_mode)
        # Preencher apenas onde há NaN
        mask_nan = serie.isna()
        serie.loc[mask_nan] = modas_grupo.loc[mask_nan]
    
    # Se ainda houver NaN, usar moda global
    if serie.isna().sum() > 0:
        moda_global = serie.mode()
        if len(moda_global) > 0:
            serie = serie.fillna(moda_global.iloc[0])
        else:
            # Se não houver moda, usar "Não informado"
            serie = serie.fillna("Não informado")
    
    return serie


def imputar_numerica_uci(df: pd.DataFrame, coluna: str) -> pd.Series:
    """
    Imputa coluna numérica específica UCI.
    
    Args:
        df: DataFrame
        coluna: Nome da coluna UCI
    
    Returns:
        Série com valores imputados
    """
    serie = df[coluna].copy()
    
    if serie.isna().sum() == 0:
        return serie
    
    # Estratégias específicas por coluna
    if 'faltas' in coluna:
        # Faltas: zero se NaN
        serie = serie.fillna(0)
    elif 'nota' in coluna.lower():
        # Notas: mediana por grupo ou zero
        serie = imputar_numerica_por_grupo(df, coluna)
        if serie.isna().sum() > 0:
            serie = serie.fillna(0)
    else:
        # Outras numéricas: mediana por grupo
        serie = imputar_numerica_por_grupo(df, coluna)
    
    return serie


def imputar_numerica_oulad(df: pd.DataFrame, coluna: str) -> pd.Series:
    """
    Imputa coluna numérica específica OULAD.
    
    Args:
        df: DataFrame
        coluna: Nome da coluna OULAD
    
    Returns:
        Série com valores imputados
    """
    serie = df[coluna].copy()
    
    if serie.isna().sum() == 0:
        return serie
    
    # Estratégias específicas por coluna
    if 'cliques' in coluna.lower():
        # Cliques: zero se NaN (sem atividade)
        serie = serie.fillna(0)
    elif 'score' in coluna.lower() or 'media' in coluna.lower():
        # Scores: mediana por grupo
        serie = imputar_numerica_por_grupo(df, coluna)
    else:
        # Outras numéricas: mediana por grupo
        serie = imputar_numerica_por_grupo(df, coluna)
    
    return serie


def imputar_resultado_final(row: pd.Series) -> float:
    """
    Imputa target usando informações auxiliares.
    
    Args:
        row: Linha do DataFrame (Series)
    
    Returns:
        Valor imputado para resultado_final
    """
    resultado = row.get('resultado_final', np.nan)
    
    if not pd.isna(resultado):
        return resultado
    
    origem = row.get('origem_dado', '')
    
    # Estratégia para UCI
    if origem == 'UCI':
        # Usar G1 e G2 para estimar G3 ausente
        g1 = row.get('uci_nota_periodo1', np.nan)
        g2 = row.get('uci_nota_periodo2', np.nan)
        
        if not pd.isna(g1) and not pd.isna(g2):
            # Média de G1 e G2, depois normalizar
            g3_estimado = (g1 + g2) / 2.0
            return normalizar_target_uci(g3_estimado)
        elif not pd.isna(g1):
            # Se só tiver G1, usar G1 como estimativa
            return normalizar_target_uci(g1)
        elif not pd.isna(g2):
            # Se só tiver G2, usar G2 como estimativa
            return normalizar_target_uci(g2)
    
    # Estratégia para OULAD
    elif origem == 'OULAD':
        # Usar média de scores para estimar resultado
        media_score = row.get('oulad_media_score', np.nan)
        
        if not pd.isna(media_score):
            # Converter score (0-100) para escala 0-10
            # Assumindo que score > 70 = Pass, > 85 = Distinction, < 50 = Fail
            if media_score >= 85:
                return 9.0  # Distinction
            elif media_score >= 70:
                return 7.0  # Pass
            elif media_score >= 50:
                return 3.0  # Fail
            else:
                return 0.0  # Withdrawn
    
    # Fallback: valor médio global (5.0)
    return 5.0


def tratar_dados_ausentes(df_unificado: pd.DataFrame) -> pd.DataFrame:
    """
    Função principal de imputação de dados ausentes.
    
    Args:
        df_unificado: DataFrame unificado com dados UCI e OULAD
    
    Returns:
        DataFrame com dados imputados
    """
    df = df_unificado.copy()
    
    print("🔄 Tratando dados ausentes...")
    
    # Separar colunas por tipo e origem
    colunas_uci = [c for c in df.columns if c.startswith('uci_')]
    colunas_oulad = [c for c in df.columns if c.startswith('oulad_')]
    colunas_comuns = [c for c in df.columns if c not in colunas_uci + colunas_oulad + ['origem_dado']]
    
    # Tratar coluna target primeiro (CRÍTICO)
    if 'resultado_final' in df.columns:
        print("  ⚠️ Imputando resultado_final (crítico)...")
        df['resultado_final'] = df.apply(imputar_resultado_final, axis=1)
    
    # Tratar colunas numéricas comuns
    colunas_numericas_comuns = [c for c in colunas_comuns if df[c].dtype in [np.float64, np.float32, np.int64, np.int32]]
    for col in colunas_numericas_comuns:
        if df[col].isna().sum() > 0:
            print(f"  🔄 Imputando numérica comum: {col}")
            df[col] = imputar_numerica_por_grupo(df, col)
    
    # Tratar colunas categóricas comuns
    colunas_categoricas_comuns = [c for c in colunas_comuns if df[c].dtype == 'object' or df[c].dtype.name == 'category']
    for col in colunas_categoricas_comuns:
        if df[col].isna().sum() > 0:
            print(f"  🔄 Imputando categórica comum: {col}")
            df[col] = imputar_categorica_por_grupo(df, col)
    
    # Tratar colunas UCI específicas
    colunas_numericas_uci = [c for c in colunas_uci if df[c].dtype in [np.float64, np.float32, np.int64, np.int32]]
    for col in colunas_numericas_uci:
        if df[col].isna().sum() > 0:
            # Apenas para registros UCI
            mask_uci = df['origem_dado'] == 'UCI'
            if mask_uci.sum() > 0:
                print(f"  🔄 Imputando numérica UCI: {col}")
                df.loc[mask_uci, col] = imputar_numerica_uci(df.loc[mask_uci], col)
    
    # Tratar colunas OULAD específicas
    colunas_numericas_oulad = [c for c in colunas_oulad if df[c].dtype in [np.float64, np.float32, np.int64, np.int32]]
    for col in colunas_numericas_oulad:
        if df[col].isna().sum() > 0:
            # Apenas para registros OULAD
            mask_oulad = df['origem_dado'] == 'OULAD'
            if mask_oulad.sum() > 0:
                print(f"  🔄 Imputando numérica OULAD: {col}")
                df.loc[mask_oulad, col] = imputar_numerica_oulad(df.loc[mask_oulad], col)
    
    print("✅ Tratamento de dados ausentes concluído")
    
    return df


def tratar_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata outliers após imputação.
    
    Args:
        df: DataFrame com dados imputados
    
    Returns:
        DataFrame com outliers tratados
    """
    df = df.copy()
    
    print("🔄 Tratando outliers...")
    
    # Clip resultado_final entre 0-10
    if 'resultado_final' in df.columns:
        df['resultado_final'] = df['resultado_final'].clip(0, 10)
        print("  ✅ resultado_final: clipado entre 0-10")
    
    # Clip faltas entre 0-50
    if 'faltas' in df.columns:
        df['faltas'] = df['faltas'].clip(0, 50)
        print("  ✅ faltas: clipado entre 0-50")
    
    # Clip tentativas_anteriores (não pode ser negativo)
    if 'tentativas_anteriores' in df.columns:
        df['tentativas_anteriores'] = df['tentativas_anteriores'].clip(lower=0)
        print("  ✅ tentativas_anteriores: valores negativos removidos")
    
    # Clip idade (15-100 para evitar valores extremos)
    if 'idade' in df.columns and df['idade'].dtype in [np.float64, np.float32, np.int64, np.int32]:
        df['idade'] = df['idade'].clip(15, 100)
        print("  ✅ idade: clipado entre 15-100")
    
    print("✅ Tratamento de outliers concluído")
    
    return df


def validar_imputacao(df: pd.DataFrame) -> Dict:
    """
    Valida qualidade da imputação.
    
    Args:
        df: DataFrame após imputação
    
    Returns:
        Dicionário com métricas de validação
    """
    print("🔄 Validando imputação...")
    
    validacao = {
        'total_registros': len(df),
        'total_colunas': len(df.columns),
        'nan_por_coluna': {},
        'nan_resultado_final': df['resultado_final'].isna().sum() if 'resultado_final' in df.columns else None,
        'estatisticas_resultado_final': {},
        'distribuicao_origem': {},
        'tipos_dados': {}
    }
    
    # Contar NaN por coluna
    for col in df.columns:
        nan_count = df[col].isna().sum()
        if nan_count > 0:
            validacao['nan_por_coluna'][col] = {
                'count': nan_count,
                'percentual': (nan_count / len(df)) * 100
            }
    
    # Estatísticas de resultado_final
    if 'resultado_final' in df.columns:
        validacao['estatisticas_resultado_final'] = {
            'min': df['resultado_final'].min(),
            'max': df['resultado_final'].max(),
            'media': df['resultado_final'].mean(),
            'mediana': df['resultado_final'].median(),
            'std': df['resultado_final'].std(),
            'nan_count': df['resultado_final'].isna().sum()
        }
    
    # Distribuição por origem
    if 'origem_dado' in df.columns:
        validacao['distribuicao_origem'] = df['origem_dado'].value_counts().to_dict()
    
    # Tipos de dados
    validacao['tipos_dados'] = df.dtypes.to_dict()
    
    print("✅ Validação concluída")
    
    return validacao


# ============================================================================
# Função Principal de Unificação
# ============================================================================

def unificar_datasets(base_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Orquestra todo o processo de unificação de datasets UCI e OULAD.
    
    Args:
        base_path: Caminho base do projeto (opcional)
    
    Returns:
        DataFrame unificado com dados UCI e OULAD
    """
    if base_path is None:
        base_path = Path(__file__).parent.parents[1]
    
    print("=" * 70)
    print("🚀 INICIANDO UNIFICAÇÃO DE DATASETS")
    print("=" * 70)
    
    # 1. Carregar dados brutos
    print("\n📥 Etapa 1: Carregando dados brutos...")
    df_uci_raw = carregar_dados_uci_raw()
    print(f"  ✅ UCI carregado: {df_uci_raw.shape}")
    
    dataframes_oulad_raw = carregar_dados_oulad_raw()
    print(f"  ✅ OULAD carregado: {len(dataframes_oulad_raw)} arquivos")
    
    # 2. Mapear colunas UCI
    print("\n🔄 Etapa 2: Mapeando colunas UCI...")
    df_uci_mapeado = mapear_colunas_uci(df_uci_raw)
    print(f"  ✅ UCI mapeado: {df_uci_mapeado.shape}")
    
    # 3. Agregar OULAD
    print("\n🔄 Etapa 3: Agregando dados OULAD...")
    df_oulad_agregado = agregar_oulad_por_estudante(dataframes_oulad_raw)
    print(f"  ✅ OULAD agregado: {df_oulad_agregado.shape}")
    
    # 4. Mapear colunas OULAD
    print("\n🔄 Etapa 4: Mapeando colunas OULAD...")
    df_oulad_mapeado = mapear_colunas_oulad(df_oulad_agregado)
    print(f"  ✅ OULAD mapeado: {df_oulad_mapeado.shape}")
    
    # 5. Adicionar coluna de origem
    print("\n🔄 Etapa 5: Adicionando coluna de origem...")
    df_uci_final = adicionar_coluna_origem(df_uci_mapeado, 'UCI')
    df_oulad_final = adicionar_coluna_origem(df_oulad_mapeado, 'OULAD')
    print(f"  ✅ Coluna origem adicionada")
    
    # 6. Concatenar DataFrames
    print("\n🔄 Etapa 6: Concatenando DataFrames...")
    # Garantir que todas as colunas existam em ambos os dataframes
    colunas_comuns = set(df_uci_final.columns) | set(df_oulad_final.columns)
    
    # Adicionar colunas ausentes como NaN
    for col in colunas_comuns:
        if col not in df_uci_final.columns:
            df_uci_final[col] = np.nan
        if col not in df_oulad_final.columns:
            df_oulad_final[col] = np.nan
    
    # Reordenar colunas para ficarem consistentes
    colunas_ordenadas = sorted(colunas_comuns)
    df_uci_final = df_uci_final[colunas_ordenadas]
    df_oulad_final = df_oulad_final[colunas_ordenadas]
    
    df_unificado = pd.concat([df_uci_final, df_oulad_final], ignore_index=True)
    print(f"  ✅ Dataset unificado: {df_unificado.shape}")
    
    # 7. Tratar dados ausentes
    print("\n🔄 Etapa 7: Tratando dados ausentes...")
    df_unificado = tratar_dados_ausentes(df_unificado)
    
    # 8. Tratar outliers
    print("\n🔄 Etapa 8: Tratando outliers...")
    df_unificado = tratar_outliers(df_unificado)
    
    # 9. Validar imputação
    print("\n🔄 Etapa 9: Validando imputação...")
    validacao = validar_imputacao(df_unificado)
    
    print("\n" + "=" * 70)
    print("✅ UNIFICAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print(f"\n📊 Estatísticas finais:")
    print(f"  - Total de registros: {validacao['total_registros']:,}")
    print(f"  - Total de colunas: {validacao['total_colunas']}")
    print(f"  - Distribuição por origem: {validacao['distribuicao_origem']}")
    print(f"  - NaN em resultado_final: {validacao['nan_resultado_final']}")
    
    return df_unificado


def salvar_dataset_unificado(df_unificado: pd.DataFrame, base_path: Optional[Path] = None) -> Tuple[Path, Path]:
    """
    Salva dataset unificado em formato pickle e CSV.
    
    Args:
        df_unificado: DataFrame unificado
        base_path: Caminho base do projeto (opcional)
    
    Returns:
        Tupla com paths dos arquivos salvos (pickle, csv)
    """
    if base_path is None:
        base_path = Path(__file__).parent.parents[1]
    
    print("\n💾 Salvando dataset unificado...")
    
    # Caminhos dos arquivos
    pickle_path = base_path / "unified_dataset.pkl"
    csv_path = base_path / "unified_dataset.csv"
    
    # Salvar em pickle
    print(f"  📦 Salvando pickle: {pickle_path}")
    df_unificado.to_pickle(pickle_path, protocol=4)
    pickle_size = pickle_path.stat().st_size / (1024 * 1024)  # MB
    print(f"    ✅ Arquivo salvo: {pickle_size:.2f} MB")
    
    # Salvar em CSV
    print(f"  📄 Salvando CSV: {csv_path}")
    df_unificado.to_csv(csv_path, index=False, encoding='utf-8')
    csv_size = csv_path.stat().st_size / (1024 * 1024)  # MB
    print(f"    ✅ Arquivo salvo: {csv_size:.2f} MB")
    
    # Estatísticas de memória
    memory_mb = df_unificado.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f"\n📊 Uso de memória do DataFrame: {memory_mb:.2f} MB")
    
    return pickle_path, csv_path
