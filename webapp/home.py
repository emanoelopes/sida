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

# Seção 1: Download do Template
st.markdown("## 📥 Passo 1: Baixe o Template")
st.markdown("""
O template inclui as **2 features mais importantes** identificadas em:
- **UCI**: Escolas públicas portuguesas (nota_2bim, faltas)
- **OULAD**: Plataforma de aprendizado online (pontuacao, regiao)
""")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **Como usar o Template Unificado:**
    1. Baixe o template Excel pré-gerado com as features mais importantes
    2. Preencha o template com seus dados (incluindo o nome do aluno)
    3. Use escala 0-10 para 'resultado_final' (padrão brasileiro)
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

# Botão para download do template pré-gerado
if st.button("📥 Baixar Template Unificado", type="primary"):
    import os
    
    # Verificar se o arquivo existe
    template_path = "template_unificado_features.xlsx"
    if os.path.exists(template_path):
        st.session_state.template_downloaded = True
        
        # Carregar e mostrar preview
        df_template = pd.read_excel(template_path)
        feature_cols = [col for col in df_template.columns if col not in ['nome_aluno', 'resultado_final']]
        st.success(f"✅ Template unificado disponível! Inclui {len(feature_cols)} features: {', '.join(feature_cols)}")
        
        st.markdown("**Preview do Template Unificado:**")
        st.dataframe(df_template.head(), use_container_width=True)
        
        # Download do arquivo
        with open(template_path, "rb") as file:
            st.download_button(
                "⬇️ Baixar Template Excel",
                data=file.read(),
                file_name="template_analise_educacional.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key='download_unified_template'
            )
    else:
        st.error("❌ Template não encontrado. Execute o sistema para gerar o template.")

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
                        
                        # Os resultados serão exibidos na seção abaixo
                    else:
                        st.error("❌ Erro na análise. Verifique os dados e tente novamente.")
        else:
            st.error(f"❌ {msg}")
            
    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")

# Seção 3: Resultados (se disponíveis)
if 'analise_resultados' in st.session_state and 'user_data_uploaded' in st.session_state:
    st.markdown("---")
    # Exibir resultados salvos (título já está na função exibir_resultados_com_ia)
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

Versão 0.1.1 - 2025
""")