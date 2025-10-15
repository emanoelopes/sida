# src/carregar_dados.py
import pandas as pd
from pathlib import Path
import pickle
import os

def carregar_uci_dados(pickle_path: str = "../uci_dataframe.pkl") -> pd.DataFrame:
    """Carrega dados UCI processados do arquivo pickle"""
    # Tentar diferentes caminhos para o arquivo pickle
    possible_paths = [
        pickle_path,
        f"../{pickle_path}",
        f"../../{pickle_path}",
        Path(__file__).parent.parents[1] / "uci_dataframe.pkl"
    ]
    
    df = None
    for path in possible_paths:
        p = Path(path)
        if p.is_file():
            try:
                with p.open("rb") as f:
                    df = pickle.load(f)
                if isinstance(df, pd.DataFrame):
                    break
            except Exception as e:
                continue
    
    if df is None:
        raise FileNotFoundError(f"Arquivo uci_dataframe.pkl não encontrado em nenhum dos caminhos: {possible_paths}")
    
    return df

def carregar_oulad_dados(pickle_path: str = "../oulad_dataframe.pkl") -> pd.DataFrame:
    """Carrega dados OULAD processados do arquivo pickle"""
    # Tentar diferentes caminhos para o arquivo pickle
    possible_paths = [
        pickle_path,
        f"../{pickle_path}",
        f"../../{pickle_path}",
        Path(__file__).parent.parents[1] / "oulad_dataframe.pkl"
    ]
    
    df = None
    for path in possible_paths:
        p = Path(path)
        if p.is_file():
            try:
                with p.open("rb") as f:
                    df = pickle.load(f)
                if isinstance(df, pd.DataFrame):
                    break
            except Exception as e:
                continue
    
    if df is None:
        raise FileNotFoundError(f"Arquivo oulad_dataframe.pkl não encontrado em nenhum dos caminhos: {possible_paths}")
    
    return df

def carregar_dados_uci_raw():
    """Carrega dados UCI brutos dos arquivos CSV"""
    datasets_path = Path(__file__).parent.parents[1] / 'datasets' / 'uci_data'
    
    # Português
    por_path = os.path.join(datasets_path, 'student-por.csv')
    por = pd.read_csv(por_path, sep=';')
    
    # Matemática
    mat_path = os.path.join(datasets_path, 'student-mat.csv')
    mat = pd.read_csv(mat_path, sep=';')
    
    # Adicionando coluna com o conjunto de dados de origem
    mat['origem'] = 'mat'
    por['origem'] = 'por'
    
    # Concatenando os dataframes
    df = pd.concat([mat, por])
    
    # Transformando valores e tipos de dados
    df['traveltime'] = df['traveltime'].map({1: '<15m', 2: '15-30m', 3: '30-1h', 4: '>1h'})
    df['studytime'] = df['studytime'].map({1: '<2h', 2: '2-5h', 3: '5-10h', 4: '>10h'})
    df[['Medu','Fedu','famrel','goout','Dalc','Walc','health']] = \
        df[['Medu','Fedu','famrel','goout','Dalc','Walc','health']].astype('object')
    
    return df

def carregar_dados_oulad_raw():
    """Carrega dados OULAD brutos dos arquivos CSV"""
    datasets_path = Path(__file__).parent.parents[1] / 'datasets' / 'oulad_data'
    
    dataframes_oulad = {}
    
    for filename in os.listdir(datasets_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(datasets_path, filename)
            df_name = os.path.splitext(filename)[0]
            try:
                dataframes_oulad[df_name] = pd.read_csv(file_path, sep=',', encoding='ISO-8859-1')
            except Exception as e:
                print(f"Erro ao carregar o arquivo '{filename}': {e}")
    
    return dataframes_oulad

def processar_dados_oulad(dataframes_oulad):
    """Processa os dados OULAD para análise"""
    # Limitar dados para performance
    df_assessments = dataframes_oulad['assessments'].head(10_000)
    df_courses = dataframes_oulad['courses'].head(10_000)
    df_vle = dataframes_oulad['vle'].head(10_000)
    df_studentinfo = dataframes_oulad['studentInfo'].head(10_000)
    df_studentregistration = dataframes_oulad['studentRegistration'].head(10_000)
    df_studentassessment = dataframes_oulad['studentAssessment'].head(10_000)
    df_studentvle = dataframes_oulad['studentVle'].head(10_000)
    
    # Processar dados
    new_vle = df_vle.drop(['week_from','week_to'], axis=1)
    
    # Imputação com os valores mais frequentes por região
    dataframes_oulad['studentInfo']['imd_band_2'] = dataframes_oulad['studentInfo'].apply(
        lambda x: dataframes_oulad['studentInfo'][dataframes_oulad['studentInfo']['region']==x['region']]['imd_band'].mode()[0] 
        if pd.isna(x['imd_band']) else x['imd_band'], axis=1)
    new_studentInfo = df_studentinfo.drop(['imd_band'], axis=1)
    
    # Imputando valores ausentes
    df_student_registration_copy = df_studentregistration.copy()
    mean_date_registration = df_student_registration_copy['date_registration'].mean()
    df_student_registration_copy['date_unregistration'] = df_student_registration_copy['date_unregistration'].fillna(
        df_student_registration_copy['date_unregistration'].max())
    df_student_registration_copy['date_registration'] = df_student_registration_copy['date_registration'].fillna(mean_date_registration)
    
    # Junção dos dados
    vle_activities = pd.merge(df_studentvle, new_vle, on=['code_module','code_presentation','id_site'], how='inner')
    assessments_activities = pd.merge(df_studentassessment, df_assessments, on='id_assessment', how='inner')
    studentinfo_activities = pd.merge(vle_activities, new_studentInfo, on=['code_module','code_presentation','id_student'], how='inner')
    merged_df = pd.merge(studentinfo_activities, assessments_activities, on=['code_module','code_presentation','id_student'], how='inner')
    
    # Merge com outros dataframes
    merged_df = pd.merge(merged_df, df_courses, on=['code_presentation'], how='inner')
    merged_df = pd.merge(merged_df, df_studentregistration, on=['code_presentation','id_student'], how='inner')
    
    # Imputando valores ausentes
    for col in merged_df.select_dtypes(include=['number']).columns:
        merged_df[col] = merged_df[col].fillna(merged_df[col].mean())
    
    for col in merged_df.select_dtypes(include='object').columns:
        merged_df[col] = merged_df[col].fillna(merged_df[col].mode()[0])
    
    return merged_df