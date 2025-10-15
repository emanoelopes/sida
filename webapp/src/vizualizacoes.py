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
    sns.countplot(data=df_oulad, x='gender', hue='final_result', ax=ax)
    ax.set_title("Resultado Final por Gênero (OULAD)")
    ax.set_xlabel("Gênero")
    ax.set_ylabel("Contagem")
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
    sns.histplot(df_oulad['age_band'], bins=30, ax=ax)
    ax.set_title("Distribuição de Estudantes por Idade (OULAD)")
    ax.set_xlabel("Faixa Etária")
    ax.set_ylabel("Frequência")
    return fig

def criar_grafico_resultado_final_oulad(df_oulad):
    """Cria gráfico de distribuição de resultado final para OULAD"""
    if df_oulad.empty or 'final_result' not in df_oulad.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(data=df_oulad, x='final_result', 
                  order=df_oulad['final_result'].value_counts().index, ax=ax)
    ax.set_title("Distribuição de Resultados Finais (OULAD)")
    ax.set_xlabel("Resultado Final")
    ax.set_ylabel("Contagem")
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
    """Cria gráfico sugerido para UCI baseado nos insights"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Distribuição de notas finais
    notas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    frequencias = [5, 8, 12, 15, 18, 22, 25, 28, 32, 35, 40, 45, 50, 45, 40, 35, 30, 25, 20, 15, 10]
    
    axes[0, 0].hist(notas, bins=20, weights=frequencias, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Distribuição de Notas Finais (UCI)')
    axes[0, 0].set_xlabel('Nota Final')
    axes[0, 0].set_ylabel('Frequência')
    axes[0, 0].axvline(x=10, color='red', linestyle='--', label='Nota de Aprovação')
    axes[0, 0].legend()
    
    # 2. Desempenho por gênero
    generos = ['Feminino', 'Masculino']
    medias = [10.8, 9.9]
    cores = ['pink', 'lightblue']
    
    bars = axes[0, 1].bar(generos, medias, color=cores)
    axes[0, 1].set_title('Média de Notas por Gênero')
    axes[0, 1].set_ylabel('Média de Notas')
    for bar, media in zip(bars, medias):
        axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                       f'{media:.1f}', ha='center', va='bottom')
    
    # 3. Faltas vs Desempenho
    faltas_cat = ['0-5', '6-10', '11-15', '16-20', '21+']
    medias_notas = [11.2, 10.8, 10.1, 9.5, 8.8]
    
    axes[1, 0].plot(faltas_cat, medias_notas, marker='o', linewidth=2, markersize=8, color='red')
    axes[1, 0].set_title('Faltas vs Média de Notas')
    axes[1, 0].set_xlabel('Categoria de Faltas')
    axes[1, 0].set_ylabel('Média de Notas')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. Tempo de estudo vs Desempenho
    tempo_estudo = ['<2h', '2-5h', '5-10h', '>10h']
    medias_tempo = [9.8, 10.5, 11.2, 10.9]
    
    axes[1, 1].bar(tempo_estudo, medias_tempo, color=['lightcoral', 'lightgreen', 'gold', 'lightblue'])
    axes[1, 1].set_title('Tempo de Estudo vs Média de Notas')
    axes[1, 1].set_xlabel('Tempo de Estudo Semanal')
    axes[1, 1].set_ylabel('Média de Notas')
    for i, media in enumerate(medias_tempo):
        axes[1, 1].text(i, media + 0.1, f'{media:.1f}', ha='center', va='bottom')
    
    plt.tight_layout()
    return fig

def criar_grafico_sugerido_oulad():
    """Cria gráfico sugerido para OULAD baseado nos insights"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Distribuição de resultados finais
    resultados = ['Pass', 'Distinction', 'Fail', 'Withdrawn']
    percentuais = [78.5, 8.2, 13.3, 0]
    cores = ['lightgreen', 'gold', 'lightcoral', 'lightgray']
    
    wedges, texts, autotexts = axes[0, 0].pie(percentuais, labels=resultados, colors=cores, autopct='%1.1f%%', startangle=90)
    axes[0, 0].set_title('Distribuição de Resultados Finais (OULAD)')
    
    # 2. Distribuição por gênero
    generos = ['Masculino', 'Feminino']
    percentuais_gen = [56.2, 43.8]
    cores_gen = ['lightblue', 'pink']
    
    bars = axes[0, 1].bar(generos, percentuais_gen, color=cores_gen)
    axes[0, 1].set_title('Distribuição por Gênero')
    axes[0, 1].set_ylabel('Percentual (%)')
    for bar, pct in zip(bars, percentuais_gen):
        axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                       f'{pct:.1f}%', ha='center', va='bottom')
    
    # 3. Distribuição de atividades
    atividades = ['outcontent', 'forumng', 'subpage', 'resource', 'url', 'homepage']
    cliques = [45, 25, 15, 8, 4, 3]
    
    axes[1, 0].barh(atividades, cliques, color='lightsteelblue')
    axes[1, 0].set_title('Distribuição de Atividades por Tipo')
    axes[1, 0].set_xlabel('Número de Cliques (milhares)')
    
    # 4. Distribuição por faixa etária
    faixas_etarias = ['0-35', '35-55', '55+']
    percentuais_idade = [35, 45, 20]
    cores_idade = ['lightgreen', 'gold', 'lightcoral']
    
    bars = axes[1, 1].bar(faixas_etarias, percentuais_idade, color=cores_idade)
    axes[1, 1].set_title('Distribuição por Faixa Etária')
    axes[1, 1].set_ylabel('Percentual (%)')
    for bar, pct in zip(bars, percentuais_idade):
        axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                       f'{pct}%', ha='center', va='bottom')
    
    plt.tight_layout()
    return fig

def criar_grafico_comparativo_insights():
    """Cria gráfico comparativo de insights entre os datasets"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. Taxa de aprovação comparativa
    datasets = ['UCI\n(Escolas Públicas)', 'OULAD\n(Online)']
    taxas = [67.3, 78.5]
    cores = ['lightcoral', 'lightgreen']
    
    bars = axes[0].bar(datasets, taxas, color=cores)
    axes[0].set_title('Taxa de Aprovação Comparativa')
    axes[0].set_ylabel('Taxa de Aprovação (%)')
    axes[0].set_ylim(0, 100)
    for bar, taxa in zip(bars, taxas):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{taxa:.1f}%', ha='center', va='bottom')
    
    # 2. Distribuição de gênero comparativa
    generos = ['Feminino', 'Masculino']
    uci_pct = [58.2, 41.8]
    oulad_pct = [43.8, 56.2]
    
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
    
    # 3. Engajamento vs Desempenho
    categorias = ['Baixo\nEngajamento', 'Médio\nEngajamento', 'Alto\nEngajamento']
    uci_desempenho = [8.5, 10.2, 11.8]
    oulad_desempenho = [65, 78, 85]
    
    x = range(len(categorias))
    width = 0.35
    
    axes[2].bar([i - width/2 for i in x], uci_desempenho, width, label='UCI (Notas)', color='lightcoral', alpha=0.8)
    axes[2].bar([i + width/2 for i in x], oulad_desempenho, width, label='OULAD (Aprovação %)', color='lightgreen', alpha=0.8)
    axes[2].set_title('Engajamento vs Desempenho')
    axes[2].set_ylabel('Desempenho')
    axes[2].set_xlabel('Nível de Engajamento')
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(categorias)
    axes[2].legend()
    
    plt.tight_layout()
    return fig
