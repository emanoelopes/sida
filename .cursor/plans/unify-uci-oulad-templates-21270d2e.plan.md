<!-- 21270d2e-cccd-4a07-9630-dcb9e300c50f da91418a-ddb5-4546-9471-7c5c8362edf8 -->
# Sistema de Análise Educacional com IA

## Visão Geral

Criar um sistema completo onde professores/coordenadores podem:

1. Baixar template com as **2 features mais importantes** de UCI e OULAD (não 3)
2. Preencher com dados dos alunos (nome + features + nota final)
3. Fazer upload e receber análise automática completa
4. Gráficos com interpretação em português via OpenAI
5. Configurar sua própria chave OpenAI na sidebar

## Correção Importante

⚠️ **O template deve ter as TOP 2 FEATURES (não 3) de cada dataset**

- 2 features UCI + 2 features OULAD + nome_aluno + resultado_final = 6 colunas totais

## Estrutura de Arquivos

### Arquivos Novos a Criar:

1. **`webapp/home.py`** (Landing Page Principal)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Página inicial com upload de template
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Botão para gerar template unificado
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Seção de análise e resultados

2. **`webapp/pages/1_dashboard.py`** (Dashboard Consolidado)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Visão geral dos datasets UCI e OULAD
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Métricas principais
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Gráficos comparativos

3. **`webapp/src/openai_interpreter.py`** (Novo módulo)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Funções para interpretar gráficos via OpenAI
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Geração de insights em linguagem acessível
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Configuração de API key

### Arquivos a Modificar:

1. **`webapp/src/utilidades.py`**

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Modificar `gerar_template_unificado()` para usar TOP 2 features (não 3)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Adicionar funções de análise completa
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Funções para gerar todos os gráficos

2. **`webapp/src/vizualizacoes.py`**

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Adicionar funções para gráficos específicos
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Gráficos de distribuição, correlação, etc.

## Implementação Detalhada

### 1. Correção do Template Unificado

Modificar `gerar_template_unificado()` em `utilidades.py`:

```python
def gerar_template_unificado() -> pd.DataFrame:
    """Gera template unificado com TOP 2 features de UCI e OULAD"""
    try:
        # Get TOP 2 features from UCI (não 3!)
        df_importance_uci = calcular_feature_importance_uci()
        top_features_uci = df_importance_uci.nlargest(2, 'importance')['feature'].tolist()
        
        # Get TOP 2 features from OULAD (não 3!)
        df_importance_oulad = calcular_feature_importance_oulad()
        top_features_oulad = df_importance_oulad.nlargest(2, 'importance')['feature'].tolist()
        
        # Build template: nome_aluno + 2 UCI + 2 OULAD + resultado_final = 6 colunas
        template_data = {'nome_aluno': [''] * 10}
        
        # Add features...
        # Total: 6 colunas
```

### 2. Novo Módulo OpenAI (`openai_interpreter.py`)

```python
import openai
import streamlit as st

def configurar_openai_key():
    """Permite usuário configurar sua própria chave OpenAI"""
    with st.sidebar:
        st.markdown("### 🔑 Configuração OpenAI")
        api_key = st.text_input(
            "Sua OpenAI API Key:",
            type="password",
            help="Cole sua chave da OpenAI para interpretação de gráficos"
        )
        if api_key:
            st.session_state.openai_key = api_key
            openai.api_key = api_key
            st.success("✅ Chave configurada!")
        return api_key

def interpretar_grafico(tipo_grafico: str, dados_contexto: dict) -> str:
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
```

### 3. Landing Page Principal (`home.py`)

```python
import streamlit as st
from src.utilidades import gerar_template_unificado, validar_template_usuario
from src.openai_interpreter import configurar_openai_key, interpretar_grafico
from src.vizualizacoes import criar_todos_graficos_analise

st.set_page_config(
    page_title="SIDA - Sistema de Análise Educacional",
    page_icon="📊",
    layout="wide"
)

# Configurar OpenAI na sidebar
configurar_openai_key()

st.title("📊 Sistema de Análise de Dados Educacionais")
st.markdown("### Análise Inteligente com IA")

# Seção 1: Geração do Template
st.markdown("## 📥 Passo 1: Baixe o Template")
st.markdown("""
O template inclui as **2 features mais importantes** identificadas em:
- **UCI**: Escolas públicas portuguesas
- **OULAD**: Plataforma de aprendizado online
""")

if st.button("📥 Gerar Template Unificado", type="primary"):
    with st.spinner("Gerando template..."):
        df_template = gerar_template_unificado()
        if not df_template.empty:
            st.success("✅ Template gerado!")
            st.dataframe(df_template.head())
            
            # Download
            excel_data = converter_template_para_excel(df_template)
            st.download_button(
                "⬇️ Baixar Template Excel",
                data=excel_data,
                file_name="template_analise_educacional.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Seção 2: Upload e Análise
st.markdown("## 📤 Passo 2: Envie o Template Preenchido")

uploaded_file = st.file_uploader(
    "Faça upload do template preenchido:",
    type=['xlsx', 'csv'],
    help="Template com dados dos alunos preenchidos"
)

if uploaded_file:
    # Carregar e validar
    df_usuario = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    
    is_valid, msg = validar_template_usuario(df_usuario)
    
    if is_valid:
        st.success(f"✅ {msg}")
        
        if st.button("🔍 Executar Análise Completa", type="primary"):
            with st.spinner("Executando análise..."):
                # Realizar análise
                resultados = realizar_analise_completa(df_usuario)
                
                # Exibir resultados com interpretação IA
                exibir_resultados_com_ia(resultados, df_usuario)
    else:
        st.error(f"❌ {msg}")
```

### 4. Dashboard Separado (`pages/1_dashboard.py`)

```python
import streamlit as st
from src.utilidades import (
    obter_metricas_principais_uci,
    obter_metricas_principais_oulad,
    exibir_cartoes_informativos
)

st.set_page_config(
    page_title="Dashboard Educacional",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Consolidado")
st.markdown("Visão geral dos datasets UCI e OULAD")

# Métricas principais
exibir_cartoes_informativos()

# Gráficos comparativos
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📚 Dataset UCI")
    # Gráficos UCI
    
with col2:
    st.markdown("### 🌐 Dataset OULAD")
    # Gráficos OULAD
```

### 5. Funções de Análise Completa

Em `utilidades.py`, adicionar:

```python
def realizar_analise_completa(df_usuario: pd.DataFrame) -> dict:
    """
    Executa análise completa dos dados do usuário
    Similar às análises feitas em UCI e OULAD
    """
    resultados = {
        'eda': realizar_eda_automatica(df_usuario),
        'graficos': {},
        'metricas': {}
    }
    
    # Estatísticas descritivas
    resultados['metricas']['descritivas'] = df_usuario.describe()
    
    # Correlações
    numeric_cols = df_usuario.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        resultados['metricas']['correlacao'] = df_usuario[numeric_cols].corr()
    
    # Distribuições
    resultados['graficos']['distribuicoes'] = criar_graficos_distribuicao(df_usuario)
    
    # Comparações
    resultados['graficos']['comparacoes'] = criar_graficos_comparacao(df_usuario)
    
    return resultados

def exibir_resultados_com_ia(resultados: dict, df_usuario: pd.DataFrame):
    """Exibe resultados com interpretação via OpenAI"""
    
    st.markdown("## 📊 Resultados da Análise")
    
    # 1. Métricas Gerais
    st.markdown("### 📈 Métricas Gerais")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Alunos", len(df_usuario))
    with col2:
        taxa_aprovacao = (df_usuario['resultado_final'] == 'Pass').mean() * 100
        st.metric("Taxa de Aprovação", f"{taxa_aprovacao:.1f}%")
    with col3:
        st.metric("Features Analisadas", len(df_usuario.columns) - 2)
    
    # 2. Gráfico de Distribuição + Interpretação IA
    st.markdown("### 📊 Distribuição de Resultados")
    fig_dist = criar_grafico_distribuicao_resultados(df_usuario)
    st.pyplot(fig_dist)
    
    # Interpretação via OpenAI
    contexto = {
        'total_alunos': len(df_usuario),
        'aprovados': (df_usuario['resultado_final'] == 'Pass').sum(),
        'reprovados': (df_usuario['resultado_final'] == 'Fail').sum()
    }
    interpretacao = interpretar_grafico('distribuicao_resultados', contexto)
    st.info(f"💡 **Interpretação**: {interpretacao}")
    
    # 3. Gráfico de Correlação + Interpretação IA
    st.markdown("### 🔗 Análise de Correlações")
    if 'correlacao' in resultados['metricas']:
        fig_corr = criar_grafico_correlacao(resultados['metricas']['correlacao'])
        st.pyplot(fig_corr)
        
        # Interpretação via OpenAI
        top_corr = encontrar_top_correlacoes(resultados['metricas']['correlacao'])
        interpretacao = interpretar_grafico('correlacao', top_corr)
        st.info(f"💡 **Interpretação**: {interpretacao}")
    
    # 4. Comparação por Aluno
    st.markdown("### 👥 Análise Individual")
    # Tabela com dados por aluno
    st.dataframe(df_usuario)
```

### 6. Visualizações em `vizualizacoes.py`

```python
def criar_grafico_distribuicao_resultados(df: pd.DataFrame):
    """Cria gráfico de distribuição de resultados"""
    fig, ax = plt.subplots(figsize=(10, 6))
    df['resultado_final'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title('Distribuição de Resultados Finais')
    ax.set_xlabel('Resultado')
    ax.set_ylabel('Quantidade de Alunos')
    return fig

def criar_grafico_correlacao(corr_matrix: pd.DataFrame):
    """Cria heatmap de correlação"""
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Matriz de Correlação entre Features')
    return fig

def criar_graficos_comparacao(df: pd.DataFrame):
    """Cria gráficos de comparação entre aprovados e reprovados"""
    # Implementar gráficos comparativos
    pass
```

## Estrutura da Sidebar

### Sidebar da Landing Page (home.py) - Minimalista

```python
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
```

### Sidebar do Dashboard e Outras Páginas - Informativa

```python
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
```

### Rodapé Padrão (Componente Reutilizável)

```python
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
```

### Uso em Cada Página

**Landing Page (home.py):**
```python
criar_sidebar_landpage()  # Sidebar minimalista com OpenAI
```

**Dashboard (pages/1_dashboard.py):**
```python
criar_sidebar_padrao()  # Sidebar com navegação + status OpenAI
```

**Outras páginas (UCI, OULAD, Analisador):**
```python
criar_sidebar_padrao()  # Mesma sidebar padrão
```

## Fluxo de Uso

1. **Professor/Coordenador acessa landing page**
2. **Clica em "Baixar Template" (já pré-gerado)**
3. **Baixa template Excel com 6 colunas organizadas logicamente**
4. **Preenche dados dos alunos no Excel**
5. **Faz upload do template preenchido**
6. **Sistema valida e executa análise**
7. **Gera todos os gráficos (exceto feature importance)**
8. **OpenAI interpreta cada gráfico**
9. **Exibe resultados com interpretações**

### Organização Lógica das Colunas no Template

O template deve ter uma ordem que faça sentido pedagógico:

**Estrutura Ideal:**

1. `nome_aluno` - Identificação do estudante
2. Features UCI (educação tradicional) - agrupadas
3. Features OULAD (educação online) - agrupadas  
4. `resultado_final` - Nota/resultado ao final

**Exemplo de Ordem Lógica:**

- Se UCI tem: `faltas`, `nota_2bim`
- Se OULAD tem: `cliques`, `pontuacao`

**Template organizado:**

```
| nome_aluno | faltas | nota_2bim | cliques | pontuacao | resultado_final |
```

**Lógica de Agrupamento:**

- Dados demográficos/comportamentais primeiro (faltas, frequência)
- Notas/pontuações juntas (facilita preenchimento do professor)
- Dados de engajamento online juntos (cliques, atividades)
- Resultado final por último

## Gráficos a Gerar

1. ✅ Distribuição de resultados (Pass/Fail)
2. ✅ Correlação entre features
3. ✅ Comparação aprovados vs reprovados
4. ✅ Distribuição de cada feature
5. ✅ Análise por aluno individual
6. ❌ Feature Importance (excluído conforme solicitação)

## Benefícios

- **Acessibilidade**: Linguagem clara para gestores/professores
- **Personalização**: Chave OpenAI própria do usuário
- **Automação**: Análise completa automática
- **Insights**: Interpretação contextualizada via IA
- **Flexibilidade**: Template baseado em features mais relevantes

### To-dos

- [ ] Create gerar_template_unificado() function in utilidades.py that combines top 3 features from both UCI and OULAD with nome_aluno field
- [ ] Update validar_template_usuario() to validate unified template structure with nome_aluno and features from both datasets
- [ ] Modify realizar_eda_automatica() to skip nome_aluno during training and handle unified feature set
- [ ] Update 3_analisador.py to remove dataset selection and use unified template generation
- [ ] Test the unified template generation with both UCI and OULAD feature importance calculations
- [ ] Test complete workflow: generate unified template, fill with sample data, upload, and run EDA