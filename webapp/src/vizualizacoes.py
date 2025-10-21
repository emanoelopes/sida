# src/vizualizacoes.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def criar_grafico_distribuicao_notas(df_uci):
    """Cria gráfico de distribuição de notas para UCI"""
    if df_uci.empty or 'G3' not in df_uci.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_uci['G3'], bins=20, kde=True, ax=ax)
    ax.set_title("Distribuição de Notas Finais (UCI)")
    ax.set_xlabel("Nota Final")
    ax.set_ylabel("Frequência")
    return fig

def criar_grafico_distribuicao_cliques(df_oulad):
    """Cria gráfico de distribuição de cliques para OULAD"""
    if df_oulad.empty or 'clicks' not in df_oulad.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_oulad['clicks'], bins=20, kde=True, ax=ax)
    ax.set_title("Distribuição de Cliques (OULAD)")
    ax.set_xlabel("Número de Cliques")
    ax.set_ylabel("Frequência")
    return fig

def criar_grafico_desempenho_por_genero_uci(df_uci):
    """Cria gráfico de desempenho por gênero para UCI"""
    if df_uci.empty or 'sex' not in df_uci.columns or 'G3' not in df_uci.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='sex', y='G3', data=df_uci, ax=ax, palette='Set1')
    ax.set_title("Notas Finais por Gênero (UCI)")
    ax.set_xlabel("Gênero")
    ax.set_ylabel("Nota Final")
    return fig

def criar_grafico_desempenho_por_genero_oulad(df_oulad):
    """Cria gráfico de desempenho por gênero para OULAD"""
    if df_oulad.empty or 'gender' not in df_oulad.columns or 'final_result' not in df_oulad.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    # Contar estudantes únicos por gênero e resultado final
    if 'id_student' in df_oulad.columns:
        genero_resultado = df_oulad.groupby(['gender', 'final_result'])['id_student'].nunique().reset_index()
        genero_resultado.columns = ['gender', 'final_result', 'count']
        import seaborn as sns
        sns.barplot(data=genero_resultado, x='gender', y='count', hue='final_result', ax=ax)
        ax.set_ylabel("Número de Estudantes Únicos")
    else:
        sns.countplot(data=df_oulad, x='gender', hue='final_result', ax=ax)
        ax.set_ylabel("Contagem")
    ax.set_title("Resultado Final por Gênero (OULAD)")
    ax.set_xlabel("Gênero")
    ax.legend(title="Resultado Final")
    return fig

def criar_grafico_correlacao_uci(df_uci):
    """Cria matriz de correlação para UCI"""
    if df_uci.empty:
        return None
    
    # Selecionar apenas colunas numéricas
    numeric_cols = df_uci.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        return None
    
    corr = df_uci[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                square=True, linewidths=.5, annot=True, fmt=".2f", ax=ax)
    ax.set_title('Matriz de Correlação - UCI', fontsize=15)
    return fig

def criar_grafico_atividades_oulad(df_oulad):
    """Cria gráfico de distribuição de atividades para OULAD"""
    if df_oulad.empty or 'activity_type' not in df_oulad.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df_oulad, x='activity_type', 
                  order=df_oulad['activity_type'].value_counts().index, ax=ax)
    ax.set_title("Distribuição de Atividades por Tipo (OULAD)")
    ax.set_xlabel("Tipo de Atividade")
    ax.set_ylabel("Contagem")
    plt.xticks(rotation=45)
    return fig

def criar_grafico_faltas_vs_desempenho(df_uci):
    """Cria gráfico de faltas vs desempenho para UCI"""
    if df_uci.empty or 'absences' not in df_uci.columns or 'G3' not in df_uci.columns:
        return None
    
    # Criar categorias de faltas
    temp_df = df_uci.reset_index(drop=True).copy()
    temp_df['absences_cat'] = pd.cut(temp_df['absences'], 
                           bins=[0, 5, 10, 15, 20, 100], 
                           labels=['0-5', '6-10', '11-15', '16-20', '21+'])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='absences_cat', y='G3', data=temp_df, ax=ax, palette='Paired')
    ax.set_title("Faltas vs Nota Final (UCI)")
    ax.set_xlabel("Número de Faltas")
    ax.set_ylabel("Nota Final")
    return fig

def criar_grafico_tempo_estudo_vs_desempenho(df_uci):
    """Cria gráfico de tempo de estudo vs desempenho para UCI"""
    if df_uci.empty or 'studytime' not in df_uci.columns or 'G3' not in df_uci.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='studytime', y='G3', data=df_uci, ax=ax, palette='coolwarm')
    ax.set_title("Tempo de Estudo vs Nota Final (UCI)")
    ax.set_xlabel("Tempo de Estudo Semanal")
    ax.set_ylabel("Nota Final")
    return fig

def criar_grafico_distribuicao_idade_oulad(df_oulad):
    """Cria gráfico de distribuição de idade para OULAD"""
    if df_oulad.empty or 'age_band' not in df_oulad.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Contar estudantes únicos por faixa etária
    if 'id_student' in df_oulad.columns:
        idade_counts = df_oulad.groupby('age_band')['id_student'].nunique()
        sns.barplot(x=idade_counts.index, y=idade_counts.values, ax=ax)
        ax.set_ylabel("Número de Estudantes Únicos")
    else:
        sns.histplot(df_oulad['age_band'], bins=30, ax=ax)
        ax.set_ylabel("Frequência")
    ax.set_title("Distribuição de Estudantes por Idade (OULAD)")
    ax.set_xlabel("Faixa Etária")
    return fig

def criar_grafico_resultado_final_oulad(df_oulad):
    """Cria gráfico de distribuição de resultado final para OULAD"""
    if df_oulad.empty or 'final_result' not in df_oulad.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    # Contar estudantes únicos por resultado final
    if 'id_student' in df_oulad.columns:
        resultado_counts = df_oulad.groupby('final_result')['id_student'].nunique().sort_values(ascending=False)
        sns.barplot(x=resultado_counts.index, y=resultado_counts.values, ax=ax)
        ax.set_ylabel("Número de Estudantes Únicos")
    else:
        sns.countplot(data=df_oulad, x='final_result', 
                      order=df_oulad['final_result'].value_counts().index, ax=ax)
        ax.set_ylabel("Contagem")
    ax.set_title("Distribuição de Resultados Finais (OULAD)")
    ax.set_xlabel("Resultado Final")
    return fig

def criar_grafico_consumo_alcool_vs_desempenho(df_uci):
    """Cria gráfico de consumo de álcool vs desempenho para UCI"""
    if df_uci.empty or 'Dalc' not in df_uci.columns or 'G3' not in df_uci.columns:
        return None
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.boxplot(x='Dalc', y='G3', data=df_uci, ax=axes[0], palette='tab10')
    axes[0].set_title('Consumo de Álcool Durante a Semana vs Nota Final')
    axes[0].set_xlabel('Nível de Consumo de Álcool Durante a Semana')
    axes[0].set_ylabel('Nota Final')
    
    sns.boxplot(x='Walc', y='G3', data=df_uci, ax=axes[1], palette='tab10')
    axes[1].set_title('Consumo de Álcool no Final de Semana vs Nota Final')
    axes[1].set_xlabel('Nível de Consumo de Álcool no Final de Semana')
    axes[1].set_ylabel('Nota Final')
    
    plt.tight_layout()
    return fig

def criar_grafico_escolaridade_pais_vs_desempenho(df_uci):
    """Cria gráfico de escolaridade dos pais vs desempenho para UCI"""
    if df_uci.empty or 'Fedu' not in df_uci.columns or 'Medu' not in df_uci.columns or 'G3' not in df_uci.columns:
        return None
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.boxplot(data=df_uci, x='Fedu', y='G3', ax=axes[0], palette='rainbow')
    axes[0].set_title('Distribuição das Notas Finais por Grau de Formação do Pai')
    axes[0].set_xlabel('Grau de Formação do Pai')
    axes[0].set_ylabel('Nota Final')
    
    sns.boxplot(data=df_uci, x='Medu', y='G3', ax=axes[1], palette='rainbow')
    axes[1].set_title('Distribuição das Notas Finais por Grau de Formação da Mãe')
    axes[1].set_xlabel('Grau de Formação da Mãe')
    axes[1].set_ylabel('Nota Final')
    
    plt.tight_layout()
    return fig

def criar_grafico_comparativo_aprovacao(df_uci, df_oulad):
    """Cria gráfico comparativo de aprovação entre UCI e OULAD"""
    if df_uci.empty and df_oulad.empty:
        return None
    
    # Calcular taxas de aprovação
    uci_aprov = (df_uci['G3'] >= 10).mean() * 100 if not df_uci.empty and 'G3' in df_uci.columns else 0
    oulad_aprov = (df_oulad['final_result'] == 'Pass').mean() * 100 if not df_oulad.empty and 'final_result' in df_oulad.columns else 0
    
    datasets = ['UCI', 'OULAD']
    taxas = [uci_aprov, oulad_aprov]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(datasets, taxas, color=['skyblue', 'lightcoral'])
    ax.set_title("Comparação de Taxa de Aprovação")
    ax.set_ylabel("Taxa de Aprovação (%)")
    ax.set_ylim(0, 100)
    
    # Adicionar valores nas barras
    for bar, taxa in zip(bars, taxas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{taxa:.1f}%', ha='center', va='bottom')
    
    return fig

def criar_grafico_sugerido_uci():
    """Cria gráfico sugerido para UCI baseado em dados reais"""
    try:
        from .utilidades import carregar_dados_uci_cached
        df_uci = carregar_dados_uci_cached()
        
        if df_uci.empty:
            return None
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Distribuição de notas finais
        if 'G3' in df_uci.columns:
            axes[0, 0].hist(df_uci['G3'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            axes[0, 0].set_title('Distribuição de Notas Finais (UCI)')
            axes[0, 0].set_xlabel('Nota Final')
            axes[0, 0].set_ylabel('Frequência')
            axes[0, 0].axvline(x=10, color='red', linestyle='--', label='Nota de Aprovação')
            axes[0, 0].legend()
        else:
            axes[0, 0].text(0.5, 0.5, 'Dados de notas não disponíveis', ha='center', va='center', transform=axes[0, 0].transAxes)
            axes[0, 0].set_title('Distribuição de Notas Finais (UCI)')
        
        # 2. Desempenho por gênero
        if 'sex' in df_uci.columns and 'G3' in df_uci.columns:
            genero_medias = df_uci.groupby('sex')['G3'].mean()
            generos = genero_medias.index.tolist()
            medias = genero_medias.values.tolist()
            cores = ['pink', 'lightblue']
            
            bars = axes[0, 1].bar(generos, medias, color=cores[:len(generos)])
            axes[0, 1].set_title('Média de Notas por Gênero')
            axes[0, 1].set_ylabel('Média de Notas')
            for bar, media in zip(bars, medias):
                axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                               f'{media:.1f}', ha='center', va='bottom')
        else:
            axes[0, 1].text(0.5, 0.5, 'Dados de gênero/notas não disponíveis', ha='center', va='center', transform=axes[0, 1].transAxes)
            axes[0, 1].set_title('Média de Notas por Gênero')
        
        # 3. Faltas vs Desempenho
        if 'absences' in df_uci.columns and 'G3' in df_uci.columns:
            # Criar categorias de faltas
            temp_df = df_uci.copy()
            temp_df['absences_cat'] = pd.cut(temp_df['absences'], 
                                   bins=[0, 5, 10, 15, 20, 100], 
                                   labels=['0-5', '6-10', '11-15', '16-20', '21+'])
            
            faltas_medias = temp_df.groupby('absences_cat')['G3'].mean()
            faltas_cat = faltas_medias.index.tolist()
            medias_notas = faltas_medias.values.tolist()
            
            axes[1, 0].plot(faltas_cat, medias_notas, marker='o', linewidth=2, markersize=8, color='red')
            axes[1, 0].set_title('Faltas vs Média de Notas')
            axes[1, 0].set_xlabel('Categoria de Faltas')
            axes[1, 0].set_ylabel('Média de Notas')
            axes[1, 0].tick_params(axis='x', rotation=45)
        else:
            axes[1, 0].text(0.5, 0.5, 'Dados de faltas/notas não disponíveis', ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('Faltas vs Média de Notas')
        
        # 4. Tempo de estudo vs Desempenho
        if 'studytime' in df_uci.columns and 'G3' in df_uci.columns:
            tempo_medias = df_uci.groupby('studytime')['G3'].mean()
            tempo_estudo = tempo_medias.index.tolist()
            medias_tempo = tempo_medias.values.tolist()
            cores = ['lightcoral', 'lightgreen', 'gold', 'lightblue']
            
            bars = axes[1, 1].bar(tempo_estudo, medias_tempo, color=cores[:len(tempo_estudo)])
            axes[1, 1].set_title('Tempo de Estudo vs Média de Notas')
            axes[1, 1].set_xlabel('Tempo de Estudo Semanal')
            axes[1, 1].set_ylabel('Média de Notas')
            axes[1, 1].tick_params(axis='x', rotation=45)
            for i, media in enumerate(medias_tempo):
                axes[1, 1].text(i, media + 0.1, f'{media:.1f}', ha='center', va='bottom')
        else:
            axes[1, 1].text(0.5, 0.5, 'Dados de tempo de estudo/notas não disponíveis', ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Tempo de Estudo vs Média de Notas')
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        st.warning(f"Erro ao criar gráfico UCI: {e}")
        return None

def criar_grafico_sugerido_oulad():
    """Cria gráfico sugerido para OULAD baseado em dados reais"""
    try:
        from .utilidades import carregar_dados_oulad_cached
        df_oulad = carregar_dados_oulad_cached()
        
        if df_oulad.empty:
            return None
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Distribuição de resultados finais
        if 'final_result' in df_oulad.columns and 'id_student' in df_oulad.columns:
            # Contar estudantes únicos por resultado final
            resultados_counts = df_oulad.groupby('final_result')['id_student'].nunique()
            resultados = resultados_counts.index.tolist()
            total_estudantes = df_oulad['id_student'].nunique()
            percentuais = (resultados_counts / total_estudantes * 100).tolist()
            cores = ['lightgreen', 'gold', 'lightcoral', 'lightgray']
            
            wedges, texts, autotexts = axes[0, 0].pie(percentuais, labels=resultados, colors=cores[:len(resultados)], autopct='%1.1f%%', startangle=90)
            axes[0, 0].set_title('Distribuição de Resultados Finais (OULAD)')
        else:
            axes[0, 0].text(0.5, 0.5, 'Dados de resultados não disponíveis', ha='center', va='center', transform=axes[0, 0].transAxes)
            axes[0, 0].set_title('Distribuição de Resultados Finais (OULAD)')
        
        # 2. Distribuição por gênero
        if 'gender' in df_oulad.columns and 'id_student' in df_oulad.columns:
            # Contar estudantes únicos por gênero
            genero_counts = df_oulad.groupby('gender')['id_student'].nunique()
            generos = genero_counts.index.tolist()
            total_estudantes = df_oulad['id_student'].nunique()
            percentuais_gen = (genero_counts / total_estudantes * 100).tolist()
            cores_gen = ['lightblue', 'pink']
            
            bars = axes[0, 1].bar(generos, percentuais_gen, color=cores_gen[:len(generos)])
            axes[0, 1].set_title('Distribuição por Gênero')
            axes[0, 1].set_ylabel('Percentual (%)')
            for bar, pct in zip(bars, percentuais_gen):
                axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                               f'{pct:.1f}%', ha='center', va='bottom')
        else:
            axes[0, 1].text(0.5, 0.5, 'Dados de gênero não disponíveis', ha='center', va='center', transform=axes[0, 1].transAxes)
            axes[0, 1].set_title('Distribuição por Gênero')
        
        # 3. Distribuição de atividades
        if 'activity_type' in df_oulad.columns:
            atividades_counts = df_oulad['activity_type'].value_counts().head(6)  # Top 6 atividades
            atividades = atividades_counts.index.tolist()
            cliques = atividades_counts.values.tolist()
            
            axes[1, 0].barh(atividades, cliques, color='lightsteelblue')
            axes[1, 0].set_title('Distribuição de Atividades por Tipo')
            axes[1, 0].set_xlabel('Número de Registros')
        else:
            axes[1, 0].text(0.5, 0.5, 'Dados de atividades não disponíveis', ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('Distribuição de Atividades por Tipo')
        
        # 4. Distribuição por faixa etária
        if 'age_band' in df_oulad.columns and 'id_student' in df_oulad.columns:
            # Contar estudantes únicos por faixa etária
            idade_counts = df_oulad.groupby('age_band')['id_student'].nunique()
            faixas_etarias = idade_counts.index.tolist()
            total_estudantes = df_oulad['id_student'].nunique()
            percentuais_idade = (idade_counts / total_estudantes * 100).tolist()
            cores_idade = ['lightgreen', 'gold', 'lightcoral']
            
            bars = axes[1, 1].bar(faixas_etarias, percentuais_idade, color=cores_idade[:len(faixas_etarias)])
            axes[1, 1].set_title('Distribuição por Faixa Etária')
            axes[1, 1].set_ylabel('Percentual (%)')
            axes[1, 1].tick_params(axis='x', rotation=45)
            for bar, pct in zip(bars, percentuais_idade):
                axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                               f'{pct:.1f}%', ha='center', va='bottom')
        else:
            axes[1, 1].text(0.5, 0.5, 'Dados de idade não disponíveis', ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Distribuição por Faixa Etária')
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        st.warning(f"Erro ao criar gráfico OULAD: {e}")
        return None

def criar_grafico_comparativo_insights():
    """Cria gráfico comparativo de insights entre os datasets baseado em dados reais"""
    try:
        from .utilidades import carregar_dados_uci_cached, carregar_dados_oulad_cached, obter_metricas_principais_uci, obter_metricas_principais_oulad
        
        # Carregar métricas
        metricas_uci = obter_metricas_principais_uci()
        metricas_oulad = obter_metricas_principais_oulad()
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # 1. Taxa de aprovação comparativa
        datasets = ['UCI\n(Escolas Públicas)', 'OULAD\n(Online)']
        taxas = [metricas_uci['taxa_aprovacao'], metricas_oulad['taxa_aprovacao']]
        cores = ['lightcoral', 'lightgreen']
        
        bars = axes[0].bar(datasets, taxas, color=cores)
        axes[0].set_title('Taxa de Aprovação Comparativa')
        axes[0].set_ylabel('Taxa de Aprovação (%)')
        axes[0].set_ylim(0, 100)
        for bar, taxa in zip(bars, taxas):
            axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                        f'{taxa:.1f}%', ha='center', va='bottom')
        
        # 2. Distribuição de gênero comparativa
        if metricas_uci['distribuicao_genero'] and metricas_oulad['distribuicao_genero']:
            # Normalizar para ter os mesmos gêneros
            generos = ['F', 'M']  # Assumindo F e M como padrão
            uci_pct = [metricas_uci['distribuicao_genero'].get('F', 0), metricas_uci['distribuicao_genero'].get('M', 0)]
            oulad_pct = [metricas_oulad['distribuicao_genero'].get('F', 0), metricas_oulad['distribuicao_genero'].get('M', 0)]
            
            x = range(len(generos))
            width = 0.35
            
            axes[1].bar([i - width/2 for i in x], uci_pct, width, label='UCI', color='lightcoral', alpha=0.8)
            axes[1].bar([i + width/2 for i in x], oulad_pct, width, label='OULAD', color='lightgreen', alpha=0.8)
            axes[1].set_title('Distribuição de Gênero Comparativa')
            axes[1].set_ylabel('Percentual (%)')
            axes[1].set_xlabel('Gênero')
            axes[1].set_xticks(x)
            axes[1].set_xticklabels(generos)
            axes[1].legend()
        else:
            axes[1].text(0.5, 0.5, 'Dados de gênero não disponíveis', ha='center', va='center', transform=axes[1].transAxes)
            axes[1].set_title('Distribuição de Gênero Comparativa')
        
        # 3. Comparação de métricas principais
        metricas_comparacao = ['Total de\nEstudantes', 'Taxa de\nAprovação', 'Média de\nNotas/Cliques']
        uci_valores = [metricas_uci['total_estudantes']/1000, metricas_uci['taxa_aprovacao'], metricas_uci['media_nota_final']]
        oulad_valores = [metricas_oulad['total_estudantes']/1000, metricas_oulad['taxa_aprovacao'], metricas_oulad['media_cliques']]
        
        x = range(len(metricas_comparacao))
        width = 0.35
        
        axes[2].bar([i - width/2 for i in x], uci_valores, width, label='UCI', color='lightcoral', alpha=0.8)
        axes[2].bar([i + width/2 for i in x], oulad_valores, width, label='OULAD', color='lightgreen', alpha=0.8)
        axes[2].set_title('Comparação de Métricas Principais')
        axes[2].set_ylabel('Valores')
        axes[2].set_xlabel('Métricas')
        axes[2].set_xticks(x)
        axes[2].set_xticklabels(metricas_comparacao)
        axes[2].legend()
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        st.warning(f"Erro ao criar gráfico comparativo: {e}")
        return None

# =============================================================================
# FUNÇÕES PARA EDA DE DADOS DO USUÁRIO
# =============================================================================

def criar_graficos_eda_usuario(df: pd.DataFrame, resultado_eda: dict) -> list:
    """Cria gráficos de EDA para dados do usuário"""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        
        figuras = []
        
        if resultado_eda.get('is_regression', True):
            # EDA para regressão
            figuras.extend(_criar_graficos_regressao(df, resultado_eda))
        else:
            # EDA para classificação
            figuras.extend(_criar_graficos_classificacao(df, resultado_eda))
        
        # Gráficos comuns
        figuras.extend(_criar_graficos_comuns(df, resultado_eda))
        
        return figuras
        
    except Exception as e:
        st.warning(f"Erro ao criar gráficos EDA: {e}")
        return []

def _criar_graficos_regressao(df: pd.DataFrame, resultado_eda: dict) -> list:
    """Cria gráficos específicos para regressão"""
    figuras = []
    
    try:
        # 1. Distribuição da variável target
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df['resultado_final'], bins=20, kde=True, ax=ax)
        ax.set_title('Distribuição da Variável Target (Resultado Final)')
        ax.set_xlabel('Resultado Final')
        ax.set_ylabel('Frequência')
        figuras.append(fig)
        
        # 2. Box plots das features vs target
        numeric_features = df.select_dtypes(include=[np.number]).columns
        numeric_features = [col for col in numeric_features if col != 'resultado_final']
        
        if len(numeric_features) > 0:
            n_cols = min(2, len(numeric_features))
            n_rows = (len(numeric_features) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 4*n_rows))
            if n_rows == 1:
                axes = [axes] if n_cols == 1 else axes
            else:
                axes = axes.flatten()
            
            for i, feature in enumerate(numeric_features):
                if i < len(axes):
                    sns.boxplot(data=df, x=feature, y='resultado_final', ax=axes[i])
                    axes[i].set_title(f'{feature} vs Resultado Final')
                    axes[i].tick_params(axis='x', rotation=45)
            
            # Ocultar subplots vazios
            for i in range(len(numeric_features), len(axes)):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            figuras.append(fig)
        
    except Exception as e:
        st.warning(f"Erro ao criar gráficos de regressão: {e}")
    
    return figuras

def _criar_graficos_classificacao(df: pd.DataFrame, resultado_eda: dict) -> list:
    """Cria gráficos específicos para classificação"""
    figuras = []
    
    try:
        # 1. Distribuição das classes
        fig, ax = plt.subplots(figsize=(8, 6))
        class_counts = df['resultado_final'].value_counts()
        sns.barplot(x=class_counts.index, y=class_counts.values, ax=ax)
        ax.set_title('Distribuição das Classes (Resultado Final)')
        ax.set_xlabel('Resultado Final')
        ax.set_ylabel('Frequência')
        plt.xticks(rotation=45)
        figuras.append(fig)
        
        # 2. Box plots das features por classe
        numeric_features = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_features) > 0:
            n_cols = min(2, len(numeric_features))
            n_rows = (len(numeric_features) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 4*n_rows))
            if n_rows == 1:
                axes = [axes] if n_cols == 1 else axes
            else:
                axes = axes.flatten()
            
            for i, feature in enumerate(numeric_features):
                if i < len(axes):
                    sns.boxplot(data=df, x='resultado_final', y=feature, ax=axes[i])
                    axes[i].set_title(f'{feature} por Classe')
                    axes[i].tick_params(axis='x', rotation=45)
            
            # Ocultar subplots vazios
            for i in range(len(numeric_features), len(axes)):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            figuras.append(fig)
        
    except Exception as e:
        st.warning(f"Erro ao criar gráficos de classificação: {e}")
    
    return figuras

def _criar_graficos_comuns(df: pd.DataFrame, resultado_eda: dict) -> list:
    """Cria gráficos comuns para ambos os tipos de problema"""
    figuras = []
    
    try:
        # 1. Matriz de correlação (apenas features numéricas)
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) >= 2:
            fig, ax = plt.subplots(figsize=(10, 8))
            corr = numeric_df.corr()
            mask = np.triu(np.ones_like(corr, dtype=bool))
            sns.heatmap(corr, mask=mask, cmap='RdBu_r', center=0,
                       square=True, linewidths=0.5, annot=True, fmt='.2f', ax=ax)
            ax.set_title('Matriz de Correlação - Features Numéricas')
            figuras.append(fig)
        
        # 2. Feature importance
        if not resultado_eda.get('feature_importance', pd.DataFrame()).empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            df_importance = resultado_eda['feature_importance']
            bars = ax.barh(df_importance['feature'], df_importance['importance'], color='skyblue')
            ax.set_title('Importância das Features')
            ax.set_xlabel('Importância')
            ax.set_ylabel('Features')
            
            # Adicionar valores nas barras
            for bar, importance in zip(bars, df_importance['importance']):
                ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                       f'{importance:.3f}', va='center', fontsize=10)
            
            plt.tight_layout()
            figuras.append(fig)
        
        # 3. Scatter plots entre features (se houver pelo menos 2 features numéricas)
        numeric_features = df.select_dtypes(include=[np.number]).columns
        if len(numeric_features) >= 2:
            fig, ax = plt.subplots(figsize=(10, 6))
            feature1, feature2 = numeric_features[0], numeric_features[1]
            sns.scatterplot(data=df, x=feature1, y=feature2, hue='resultado_final', ax=ax)
            ax.set_title(f'Relação entre {feature1} e {feature2}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            figuras.append(fig)
        
    except Exception as e:
        st.warning(f"Erro ao criar gráficos comuns: {e}")
    
    return figuras

def criar_grafico_metricas_modelo(resultado_eda: dict) -> plt.Figure:
    """Cria gráfico com métricas do modelo"""
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        metrics = resultado_eda.get('metrics', {})
        model_type = metrics.get('type', 'regression')
        
        if model_type == 'regression':
            # Métricas de regressão
            mae = metrics.get('mae', 0)
            rmse = metrics.get('rmse', 0)
            r2 = metrics.get('r2', 0)
            
            metricas = ['MAE', 'RMSE', 'R²']
            valores = [mae, rmse, r2]
            cores = ['lightcoral', 'lightblue', 'lightgreen']
            
            bars = ax.bar(metricas, valores, color=cores)
            ax.set_title('Métricas do Modelo de Regressão')
            ax.set_ylabel('Valor')
            
            # Adicionar valores nas barras
            for bar, valor in zip(bars, valores):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                       f'{valor:.3f}', ha='center', va='bottom')
        
        else:
            # Métricas de classificação
            accuracy = metrics.get('accuracy', 0)
            
            metricas = ['Acurácia']
            valores = [accuracy]
            cores = ['lightgreen']
            
            bars = ax.bar(metricas, valores, color=cores)
            ax.set_title('Métricas do Modelo de Classificação')
            ax.set_ylabel('Valor')
            ax.set_ylim(0, 1)
            
            # Adicionar valores nas barras
            for bar, valor in zip(bars, valores):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                       f'{valor:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        st.warning(f"Erro ao criar gráfico de métricas: {e}")
        return None
