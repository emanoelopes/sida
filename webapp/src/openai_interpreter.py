"""
Módulo para interpretação de gráficos via OpenAI
Gera insights em linguagem acessível para educadores
"""

import streamlit as st
import openai
from typing import Dict, Any

def configurar_openai_key():
    """Permite usuário configurar sua própria chave OpenAI"""
    with st.sidebar:
        st.markdown("### 🔑 Configuração OpenAI")
        st.markdown("*Para interpretação automática dos gráficos*")
        
        api_key = st.text_input(
            "Cole sua API Key:",
            type="password",
            placeholder="sk-...",
            help="Obtenha sua chave em https://platform.openai.com/api-keys"
        )
        
        if st.button("💾 Salvar Chave", type="primary"):
            if api_key and api_key.startswith('sk-'):
                st.session_state.openai_key = api_key
                openai.api_key = api_key
                st.success("✅ Chave salva com sucesso!")
            else:
                st.error("❌ Chave inválida. Deve começar com 'sk-'")
        
        if 'openai_key' in st.session_state:
            st.info("🔓 Chave OpenAI configurada")
        
        st.markdown("---")
        st.markdown("#### 💡 Como usar:")
        st.markdown("""
        1. Configure sua chave OpenAI acima
        2. Baixe o template Excel
        3. Preencha com dados dos alunos
        4. Faça upload para análise
        """)
        
        # Rodapé padrão
        st.markdown("---")
        st.markdown("### ℹ️ Sobre o Sistema")
        st.caption("""
        **SIDA - Sistema Inteligente de Análise Educacional**
        
        Mestrado em Tecnologia Educacional  
        Programa de Pós-Graduação em Tecnologias Educacionais (PPGTE)  
        Instituto UFC Virtual (IUVI)  
        Universidade Federal do Ceará (UFC)
        
        Versão 1.0.0 - 2025
        """)

def interpretar_grafico(tipo_grafico: str, dados_contexto: Dict[str, Any]) -> str:
    """
    Gera interpretação do gráfico via OpenAI
    
    Args:
        tipo_grafico: 'distribuicao', 'correlacao', 'comparacao', etc.
        dados_contexto: Dados estatísticos do gráfico
    
    Returns:
        Texto de interpretação em português para gestores/professores
    """
    if 'openai_key' not in st.session_state:
        return "⚠️ Configure sua chave OpenAI na sidebar para interpretação automática."
    
    # Configurar OpenAI
    openai.api_key = st.session_state.openai_key
    
    prompt = f"""
    Você é um especialista em análise educacional. Interprete o seguinte gráfico
    de forma clara e objetiva para gestores escolares e professores.
    
    Tipo de gráfico: {tipo_grafico}
    Dados: {dados_contexto}
    
    Forneça uma interpretação em 1 parágrafo (máximo 4 linhas) focando em:
    - O que o gráfico mostra
    - Implicações práticas para educadores
    - Ações recomendadas (se aplicável)
    
    Use linguagem acessível, evite jargões técnicos.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro ao gerar interpretação: {str(e)}"

def gerar_interpretacao_traduzida(tipo_grafico: str, dados: Dict[str, Any]) -> str:
    """Gera interpretação em português para educadores (sem OpenAI)"""
    
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
        st.markdown("### 🔑 Configuração OpenAI")
        st.markdown("*Para interpretação automática dos gráficos*")
        
        api_key = st.text_input(
            "Cole sua API Key:",
            type="password",
            placeholder="sk-...",
            help="Obtenha sua chave em https://platform.openai.com/api-keys"
        )
        
        if st.button("💾 Salvar Chave", type="primary"):
            if api_key and api_key.startswith('sk-'):
                st.session_state.openai_key = api_key
                st.success("✅ Chave salva com sucesso!")
            else:
                st.error("❌ Chave inválida. Deve começar com 'sk-'")
        
        if 'openai_key' in st.session_state:
            st.info("🔓 Chave OpenAI configurada")
        
        st.markdown("---")
        st.markdown("#### 💡 Como usar:")
        st.markdown("""
        1. Configure sua chave OpenAI acima
        2. Baixe o template Excel
        3. Preencha com dados dos alunos
        4. Faça upload para análise
        """)
        
        # Rodapé padrão
        st.markdown("---")
        st.markdown("### ℹ️ Sobre o Sistema")
        st.caption("""
        **SIDA - Sistema Inteligente de Análise Educacional**
        
        Mestrado em Tecnologia Educacional  
        Programa de Pós-Graduação em Tecnologias Educacionais (PPGTE)  
        Instituto UFC Virtual (IUVI)  
        Universidade Federal do Ceará (UFC)
        
        Versão 1.0.0 - 2025
        """)

def criar_sidebar_padrao():
    """Sidebar padrão para páginas internas (Dashboard, UCI, OULAD, etc.)"""
    with st.sidebar:
        st.markdown("### 📊 Navegação")
        st.markdown("""
        - 🏠 **Home**: Análise Customizada
        - 📊 **Dashboard**: Visão Consolidada
        - 📈 **UCI**: Análise Detalhada
        - 🌐 **OULAD**: Análise Detalhada
        - 🔍 **Analisador**: Ferramenta de Análise
        """)
        
        st.markdown("---")
        st.markdown("### 🔑 OpenAI")
        
        if 'openai_key' in st.session_state:
            st.success("✅ API Key configurada")
            if st.button("🔄 Reconfigurar"):
                del st.session_state.openai_key
                st.rerun()
        else:
            st.warning("⚠️ Configure na página inicial")
        
        # Rodapé padrão (mesmo em todas as páginas)
        st.markdown("---")
        st.markdown("### ℹ️ Sobre o Sistema")
        st.caption("""
        **SIDA - Sistema Inteligente de Análise Educacional**
        
        Mestrado em Tecnologia Educacional  
        Programa de Pós-Graduação em Tecnologias Educacionais (PPGTE)  
        Instituto UFC Virtual (IUVI)  
        Universidade Federal do Ceará (UFC)
        
        Versão 1.0.0 - 2025
        """)

def criar_rodape_sidebar():
    """Rodapé padronizado para todas as sidebars"""
    st.markdown("---")
    st.markdown("### ℹ️ Sobre o Sistema")
    st.caption("""
    **SIDA - Sistema Inteligente de Análise Educacional**
    
    Mestrado em Tecnologia Educacional  
    Programa de Pós-Graduação em Tecnologias Educacionais (PPGTE)  
    Instituto UFC Virtual (IUVI)  
    Universidade Federal do Ceará (UFC)
    
    Versão 1.0.0 - 2025
    """)
