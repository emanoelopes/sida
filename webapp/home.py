"""
Landing Page Principal - Sistema de Análise Educacional
Página inicial com upload de template e análise completa
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.utilidades import (
    gerar_template_unificado, 
    validar_template_usuario, 
    realizar_analise_completa,
    exibir_resultados_com_ia,
    converter_template_para_excel
)
from src.openai_interpreter import criar_sidebar_landpage

# Configuração da página
st.set_page_config(
    page_title="SIDA - Sistema de Análise Educacional",
    page_icon="📊",
    layout="wide"
)

# Sidebar minimalista
criar_sidebar_landpage()

# Título principal
st.title("📊 Sistema de Análise de Dados Educacionais")
st.markdown("### Análise Inteligente com IA")

# Seção 1: Geração do Template
st.markdown("## 📥 Passo 1: Baixe o Template")
st.markdown("""
O template inclui as **2 features mais importantes** identificadas em:
- **UCI**: Escolas públicas portuguesas
- **OULAD**: Plataforma de aprendizado online
""")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **Como usar o Template Unificado:**
    1. Baixe o template Excel com as features mais importantes dos datasets UCI e OULAD
    2. Preencha o template com seus dados (incluindo o nome do aluno)
    3. Mantenha a coluna 'resultado_final' com os resultados esperados
    4. Faça upload do template preenchido para análise automática
    
    **Vantagens do Template Unificado:**
    - Combina insights de educação tradicional (UCI) e online (OULAD)
    - Inclui campo para nome do aluno para personalização
    - Análise mais abrangente com features diversificadas
    """)
with col2:
    st.info("""
    **Template inclui:**
    - Campo para nome do aluno
    - Top 2 features do UCI
    - Top 2 features do OULAD
    - Coluna de resultado final
    """)

if st.button("📥 Gerar Template Unificado", type="primary"):
    with st.spinner("Gerando template..."):
        df_template = gerar_template_unificado()
        
        if not df_template.empty:
            st.session_state.template_downloaded = True
            feature_cols = [col for col in df_template.columns if col not in ['nome_aluno', 'resultado_final']]
            st.success(f"✅ Template unificado gerado com sucesso! Inclui {len(feature_cols)} features: {', '.join(feature_cols)}")
            
            st.markdown("**Preview do Template Unificado:**")
            st.dataframe(df_template.head(), use_container_width=True)
            
            # Download
            excel_data = converter_template_para_excel(df_template)
            if excel_data:
                st.download_button(
                    "⬇️ Baixar Template Excel",
                    data=excel_data,
                    file_name="template_analise_educacional.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key='download_unified_template'
                )
        else:
            st.error("Erro ao gerar template unificado. Verifique se os dados estão carregados.")

# Seção 2: Upload e Análise
st.markdown("## 📤 Passo 2: Envie o Template Preenchido")

uploaded_file = st.file_uploader(
    "Faça upload do template preenchido:",
    type=['xlsx', 'csv'],
    help="Template com dados dos alunos preenchidos"
)

if uploaded_file:
    try:
        # Carregar dados
        if uploaded_file.name.endswith('.xlsx'):
            df_usuario = pd.read_excel(uploaded_file)
        else:
            df_usuario = pd.read_csv(uploaded_file)
        
        # Validar template
        is_valid, msg = validar_template_usuario(df_usuario)
        
        if is_valid:
            st.success(f"✅ {msg}")
            st.session_state.user_data_uploaded = df_usuario
            
            st.markdown("**Preview dos Dados Carregados:**")
            st.dataframe(df_usuario.head(), use_container_width=True)
            
            if st.button("🔍 Executar Análise Completa", type="primary"):
                with st.spinner("Executando análise completa..."):
                    # Realizar análise
                    resultados = realizar_analise_completa(df_usuario)
                    
                    if resultados:
                        st.session_state.analise_resultados = resultados
                        st.success("✅ Análise concluída com sucesso!")
                        
                        # Exibir resultados com interpretação IA
                        exibir_resultados_com_ia(resultados, df_usuario)
                    else:
                        st.error("❌ Erro na análise. Verifique os dados e tente novamente.")
        else:
            st.error(f"❌ {msg}")
            
    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")

# Seção 3: Resultados (se disponíveis)
if 'analise_resultados' in st.session_state and 'user_data_uploaded' in st.session_state:
    st.markdown("---")
    st.markdown("## 📊 Resultados da Análise")
    
    # Exibir resultados salvos
    exibir_resultados_com_ia(st.session_state.analise_resultados, st.session_state.user_data_uploaded)

# Rodapé informativo
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