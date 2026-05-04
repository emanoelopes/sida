"""
Módulo para interpretação de gráficos
Gera insights em linguagem acessível para educadores
"""

import streamlit as st
from typing import Dict, Any

def gerar_interpretacao_traduzida(tipo_grafico: str, dados: Dict[str, Any]) -> str:
    """Gera interpretação em português para educadores"""
    
    interpretacoes = {
        'distribuicao_resultados': """
        📊 **Distribuição de Resultados da Turma**
        
        Este gráfico mostra quantos alunos foram aprovados, reprovados ou obtiveram distinção.
        Uma distribuição saudável mostra mais alunos aprovados. Se houver muitos reprovados,
        considere estratégias de apoio pedagógico.
        """,
        
        'correlacao_features': """
        🔗 **Relação entre Fatores de Desempenho**
        
        Este gráfico mostra como diferentes fatores se relacionam. Cores mais intensas
        indicam relações mais fortes. Por exemplo, se faltas e notas têm cor forte,
        significa que alunos com muitas faltas tendem a ter notas menores.
        """,
        
        'comparacao_aprovados_reprovados': """
        ⚖️ **Comparação: Aprovados vs Reprovados**
        
        Este gráfico compara as médias dos dois grupos. Use para identificar padrões:
        - Aprovados têm menos faltas?
        - Aprovados são mais ativos online?
        - Que fatores diferenciam os grupos?
        """,
        
        'distribuicao_faltas': """
        📅 **Distribuição de Faltas dos Alunos**
        
        Mostra quantos alunos têm cada número de faltas. Uma distribuição concentrada
        em poucas faltas indica boa frequência. Muitos alunos com muitas faltas
        pode indicar problemas de engajamento ou motivação.
        """,
        
        'engajamento_digital': """
        💻 **Engajamento Digital dos Alunos**
        
        Mostra a atividade online dos alunos. Alunos mais ativos na plataforma
        tendem a ter melhor desempenho. Use para identificar alunos que precisam
        de incentivo para usar recursos digitais.
        """,
        
        'histograma_notas': """
        📊 **Histograma de Distribuição das Notas**
        
        Este gráfico mostra a distribuição das notas finais da turma. A média e mediana
        indicam o desempenho central. Use para identificar padrões de desempenho e
        propor estratégias de apoio pedagógico quando necessário.
        """,
        
        'distribuicao_nota_2bim': """
        📈 **Distribuição das Notas do 2º Bimestre**
        
        Este gráfico mostra a distribuição das notas do 2º bimestre. Notas baixas podem
        indicar necessidade de reforço pedagógico. Use para identificar alunos que
        precisam de apoio adicional.
        """,
        
        'grafico_linhas_regiao': """
        📊 **Análise por Região**
        
        Este gráfico mostra a média das notas finais por região, categorizada por nível de faltas.
        Linhas mais altas indicam melhor desempenho. Use para identificar padrões regionais
        e a relação entre frequência e desempenho acadêmico.
        """,
        
        'radar_comparacao': """
        🎯 **Gráfico Radar - Comparação Individual**
        
        Este gráfico compara o desempenho do aluno selecionado com a média da turma.
        Áreas onde o aluno está acima da média indicam pontos fortes. Áreas abaixo da média
        podem indicar necessidades de apoio pedagógico.
        """
    }
    
    return interpretacoes.get(tipo_grafico, "Gráfico de análise educacional.")

def traduzir_rotulos_graficos(tipo_grafico: str, dados_contexto: Dict[str, Any]) -> Dict[str, str]:
    """
    Traduz rótulos de gráficos para contexto educacional brasileiro
    
    Args:
        tipo_grafico: Tipo do gráfico ('distribuicao', 'correlacao', 'comparacao', etc.)
        dados_contexto: Dados do gráfico
    
    Returns:
        Dicionário com rótulos traduzidos
    """
    
    rotulos_traduzidos = {
        # Gráficos de Distribuição
        'distribuicao_resultados': {
            'titulo': 'Distribuição de Resultados da Turma',
            'eixo_x': 'Resultado Final',
            'eixo_y': 'Quantidade de Alunos',
            'legenda': {
                'Pass': 'Aprovados',
                'Fail': 'Reprovados',
                'Distinction': 'Com Distinção'
            }
        },
        
        'distribuicao_faltas': {
            'titulo': 'Distribuição de Faltas dos Alunos',
            'eixo_x': 'Número de Faltas',
            'eixo_y': 'Quantidade de Alunos',
            'legenda': 'Frequência de Faltas'
        },
        
        'distribuicao_notas': {
            'titulo': 'Distribuição das Notas do 2º Bimestre',
            'eixo_x': 'Nota (0-10)',
            'eixo_y': 'Quantidade de Alunos',
            'legenda': 'Distribuição de Notas'
        },
        
        'distribuicao_cliques': {
            'titulo': 'Engajamento Digital dos Alunos',
            'eixo_x': 'Número de Cliques na Plataforma',
            'eixo_y': 'Quantidade de Alunos',
            'legenda': 'Atividade Online'
        },
        
        # Gráficos de Correlação
        'correlacao_features': {
            'titulo': 'Relação entre Fatores de Desempenho',
            'eixo_x': 'Fatores Analisados',
            'eixo_y': 'Fatores Analisados',
            'legenda': 'Força da Relação (Correlação)'
        },
        
        'scatter_notas_faltas': {
            'titulo': 'Relação entre Notas e Faltas',
            'eixo_x': 'Número de Faltas',
            'eixo_y': 'Nota do 2º Bimestre',
            'legenda': 'Cada ponto = 1 aluno'
        },
        
        'scatter_engajamento_desempenho': {
            'titulo': 'Relação entre Engajamento Online e Desempenho',
            'eixo_x': 'Cliques na Plataforma',
            'eixo_y': 'Pontuação nas Atividades',
            'legenda': 'Cada ponto = 1 aluno'
        },
        
        # Gráficos de Comparação
        'comparacao_aprovados_reprovados': {
            'titulo': 'Comparação: Aprovados vs Reprovados',
            'eixo_x': 'Categoria de Resultado',
            'eixo_y': 'Valor Médio',
            'legenda': {
                'Aprovados': 'Alunos Aprovados',
                'Reprovados': 'Alunos Reprovados'
            }
        },
        
        'boxplot_faltas_por_resultado': {
            'titulo': 'Distribuição de Faltas por Resultado',
            'eixo_x': 'Resultado Final',
            'eixo_y': 'Número de Faltas',
            'legenda': 'Boxplot de Faltas'
        },
        
        'boxplot_notas_por_resultado': {
            'titulo': 'Distribuição de Notas por Resultado',
            'eixo_x': 'Resultado Final',
            'eixo_y': 'Nota do 2º Bimestre',
            'legenda': 'Boxplot de Notas'
        },
        
        # Gráficos de Performance
        'metricas_turma': {
            'titulo': 'Métricas Gerais da Turma',
            'eixo_x': 'Indicadores',
            'eixo_y': 'Valores',
            'legenda': {
                'taxa_aprovacao': 'Taxa de Aprovação (%)',
                'media_faltas': 'Média de Faltas',
                'media_notas': 'Média das Notas',
                'engajamento_medio': 'Engajamento Médio'
            }
        },
        
        # Gráficos de Análise Individual
        'ranking_alunos': {
            'titulo': 'Ranking de Desempenho dos Alunos',
            'eixo_x': 'Nome do Aluno',
            'eixo_y': 'Pontuação Geral',
            'legenda': 'Desempenho Individual'
        },
        
        'alunos_risco': {
            'titulo': 'Identificação de Alunos em Risco',
            'eixo_x': 'Fatores de Risco',
            'eixo_y': 'Número de Alunos',
            'legenda': 'Alunos que precisam de atenção'
        }
    }
    
    return rotulos_traduzidos.get(tipo_grafico, {})

def criar_sidebar_landpage():
    """Sidebar limpa e focada para a landing page"""
    with st.sidebar:        
        st.markdown("#### 💡 Como usar:")
        st.markdown("""
        1. 📥 Baixe o template Excel
        2. 📝 Preencha com dados dos alunos
        3. 📤 Faça upload para análise
        4. 📊 Visualize gráficos e métricas
        """)
        
        # Rodapé
        criar_rodape_sidebar()

def criar_sidebar_padrao():
    """Sidebar padrão para páginas internas (Painel Analítico, Análise Exploratória, etc.)"""
    with st.sidebar:
        st.markdown("### 📊 Navegação")
        st.markdown("""
        - 🏠 **Home**: Análise Consolidada
        - 📊 **Painel Analítico**: Visão Consolidada
        - 📈 **Análise Exploratória**: Interativa (PygWalker)
        """)
        
        # Rodapé padrão (mesmo em todas as páginas)
        criar_rodape_sidebar()

def criar_rodape_sidebar():
    """Rodapé padronizado para todas as sidebars - informações do sistema e badges"""
    st.markdown("---")
    st.markdown("### ℹ️ Sobre o Sistema")
    st.caption("""
    **CLAREIA - Sistema de Análise de Dados Educacionais**
    
    Mestrado em Tecnologia Educacional  
    Programa de Pós-Graduação em Tecnologias Educacionais (PPGTE)  
    Instituto UFC Virtual (IUVI)  
    Universidade Federal do Ceará (UFC)
    
    Versão 1.1.0 - 2026
    """)
    
    # Badges de status do projeto
    st.markdown("""
    <div style="margin-top: 10px; text-align: center;">
        <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python 3.9+"/>
        <img src="https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
        <img src="https://img.shields.io/badge/Docker-Supported-2496ED?logo=docker&logoColor=white" alt="Docker"/>
        <img src="https://img.shields.io/badge/License-GPL--3.0-green" alt="License GPL-3.0"/>
        <img src="https://img.shields.io/badge/Version-1.1.0-orange" alt="Version"/>
    </div>
    """, unsafe_allow_html=True)
