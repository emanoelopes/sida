import streamlit as st
import pandas as pd
import io
import plotly.express as px     # FIX: Correct Plotly Express import
import tabula                   # For PDF reading
import tempfile                 # To save PDF temporarily for Tabula
import os
import numpy as np              # For numeric checks
import logging                  # For better error logging (optional but good practice)

# --- Basic Logging Setup ---
# Helps in debugging, especially if deployed
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Page Configuration (MUST be the first Streamlit command) ---
# Initialize theme based on session state *before* first run
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False # Default to light mode

# NOTE: Streamlit's native theme setting (3 dots menu > Settings) is often preferred.
# This programmatic toggle is an alternative but less standard.
# We set the initial config, but CSS will handle the dynamic switching visually.
st.set_page_config(
    page_title='Ferramenta de Análise de Dados Educacionais',
    layout="wide",
    initial_sidebar_state="expanded"
    # theme="dark" if st.session_state.dark_mode else "light" # This doesn't work dynamically after first run
)

# --- Custom CSS Injection ---
# FIX: Corrected CSS injection with markdown and modern styles
# Enhancement: Added styles for dark mode toggle and improved button/sidebar look
def apply_custom_css():
    """Applies custom CSS for styling and dark mode."""
    light_mode_css = """
    <style>
        /* --- Light Mode Variables --- */
        :root {
            --primary-bg: #FFFFFF;
            --secondary-bg: #f8f9fa;
            --text-color: #212529;
            --primary-color: #007bff; /* Blue */
            --primary-color-hover: #0056b3;
            --secondary-color: #6c757d; /* Gray */
            --border-color: #dee2e6;
            --button-bg: var(--primary-color);
            --button-text: white;
            --button-hover-bg: var(--primary-color-hover);
            --button-hover-text: white;
            --button-border: var(--primary-color);
            --sidebar-bg: var(--secondary-bg);
        }

        /* --- General Styling --- */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--text-color);
            background-color: var(--primary-bg);
        }
        .main .block-container {
            padding-top: 2rem; padding-bottom: 2rem; padding-left: 3rem; padding-right: 3rem;
        }
        h1, h2, h3 { color: var(--primary-color); }

        /* --- Sidebar Styling (Modern) --- */
        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
             color: var(--primary-color); /* Match main area heading color */
        }
        [data-testid="stSidebar"] .stButton>button { /* Specificity for sidebar buttons */
             border-color: var(--secondary-color);
             color: var(--secondary-color);
             background-color: transparent;
        }
         [data-testid="stSidebar"] .stButton>button:hover {
             background-color: var(--secondary-color);
             color: white;
         }


        /* --- Button Styling (Modern) --- */
        .stButton>button {
            border: 2px solid var(--button-border);
            border-radius: 20px; /* Rounded */
            padding: 0.5rem 1.25rem;
            color: var(--button-text);
            background-color: var(--button-bg);
            transition: all 0.3s ease-in-out;
            font-weight: 500;
        }
        .stButton>button:hover {
            background-color: var(--button-hover-bg);
            color: var(--button-hover-text);
            border-color: var(--button-hover-bg);
            transform: translateY(-2px); /* Slight lift */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stButton>button:active {
             transform: translateY(0);
             box-shadow: none;
        }

        /* --- DataFrame Styling --- */
        .stDataFrame { border: 1px solid var(--border-color); border-radius: 5px; }

        /* --- Expander Styling --- */
        .stExpander { border: 1px solid var(--border-color); border-radius: 5px; margin-bottom: 1rem; }
        .stExpander header { background-color: var(--secondary-bg); border-radius: 5px 5px 0 0; }

        /* --- Download Button --- */
        /* Might need more specific selector if default styling overrides */
        div[data-testid="stDownloadButton"] > button {
             background-color: #28a745; /* Green */
             border-color: #28a745;
        }
        div[data-testid="stDownloadButton"] > button:hover {
            background-color: #218838;
            border-color: #1e7e34;
        }

    </style>
    """

    dark_mode_css = """
    <style>
        /* --- Dark Mode Variables --- */
        body.dark-mode {
            --primary-bg: #0e1117;  /* Streamlit dark background */
            --secondary-bg: #1c1e24; /* Slightly lighter dark */
            --text-color: #fafafa; /* Light text */
            --primary-color: #00aeff; /* Brighter Blue for dark */
            --primary-color-hover: #008ecc;
            --secondary-color: #8e949c; /* Lighter Gray */
            --border-color: #31333F;
            --button-bg: var(--primary-color);
            --button-text: var(--primary-bg); /* Dark text on bright button */
            --button-hover-bg: var(--primary-color-hover);
            --button-hover-text: var(--primary-bg);
            --button-border: var(--primary-color);
            --sidebar-bg: #15181e; /* Darker sidebar */
        }

        /* --- Dark Mode Overrides --- */
        body.dark-mode { background-color: var(--primary-bg); color: var(--text-color); }
        body.dark-mode h1, body.dark-mode h2, body.dark-mode h3 { color: var(--primary-color); }
        body.dark-mode [data-testid="stSidebar"] { background-color: var(--sidebar-bg); border-right-color: var(--border-color); }
        body.dark-mode [data-testid="stSidebar"] h1, body.dark-mode [data-testid="stSidebar"] h2, body.dark-mode [data-testid="stSidebar"] h3 {
             color: var(--primary-color);
        }
        body.dark-mode .stButton>button {
            border-color: var(--button-border);
            color: var(--button-text);
            background-color: var(--button-bg);
        }
        body.dark-mode .stButton>button:hover {
            background-color: var(--button-hover-bg);
            color: var(--button-hover-text);
            border-color: var(--button-hover-bg);
        }
        body.dark-mode .stDataFrame { border-color: var(--border-color); }
        body.dark-mode .stExpander { border-color: var(--border-color); }
        body.dark-mode .stExpander header { background-color: var(--secondary-bg); }

        body.dark-mode div[data-testid="stDownloadButton"] > button {
             background-color: #34c759; /* Brighter Green */
             border-color: #34c759;
             color: var(--primary-bg);
        }
        body.dark-mode div[data-testid="stDownloadButton"] > button:hover {
            background-color: #2fad4f;
            border-color: #2fad4f;
        }

         body.dark-mode [data-testid="stSidebar"] .stButton>button { /* Sidebar buttons in dark mode */
             border-color: var(--secondary-color);
             color: var(--secondary-color);
             background-color: transparent;
        }
         body.dark-mode [data-testid="stSidebar"] .stButton>button:hover {
             background-color: var(--secondary-color);
             color: var(--primary-bg);
         }

    </style>
    """

    # JavaScript to add/remove 'dark-mode' class from body
    # FIX: Correct use of unsafe_allow_html for CSS and JS
    js_code = f"""
    <script>
    function addDarkTheme() {{
        document.body.classList.add('dark-mode');
    }}
    function removeDarkTheme() {{
         document.body.classList.remove('dark-mode');
    }}
    {'addDarkTheme();' if st.session_state.dark_mode else 'removeDarkTheme();'}
    </script>
    """

    st.markdown(light_mode_css, unsafe_allow_html=True)
    st.markdown(dark_mode_css, unsafe_allow_html=True)
    st.markdown(js_code, unsafe_allow_html=True)

apply_custom_css() # Apply the styling

# --- Helper Functions ---

# FIX: Added show_spinner for user feedback during caching
# FIX: Enhanced error handling within load_data
@st.cache_data(show_spinner="Reading file...")
def load_data(uploaded_file):
    """Loads data from CSV, Excel, or PDF into a DataFrame list."""
    if uploaded_file is None:
        return None # Should not happen if called correctly, but good practice

    dfs_list = None
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    logging.info(f"Attempting to load file: {uploaded_file.name}, extension: {file_extension}")

    try:
        if file_extension == '.csv':
            df = pd.read_csv(uploaded_file)
            dfs_list = [df]
        elif file_extension in ['.xlsx', '.xls']:
            # Consider sheet selection for robustness later
            df = pd.read_excel(uploaded_file, sheet_name=0)
            dfs_list = [df]
        elif file_extension == '.pdf':
            # FIX: Robust PDF handling with Tabula and error checking
            # ENHANCEMENT: Use with statement for temp file ensures cleanup
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            logging.info(f"Saved PDF to temporary file: {tmp_file_path}")

            read_successful = False
            try:
                # Try reading with lattice=True (good for tables with lines)
                logging.info("Trying tabula.read_pdf with lattice=True")
                dfs_tabula = tabula.read_pdf(tmp_file_path, pages='all', multiple_tables=True, lattice=True)
                read_successful = True
            except Exception as e_lattice:
                logging.warning(f"Tabula lattice=True failed: {e_lattice}. Trying stream=True.")
                try:
                    # Fallback to stream=True (good for whitespace separation)
                    logging.info("Trying tabula.read_pdf with stream=True")
                    dfs_tabula = tabula.read_pdf(tmp_file_path, pages='all', multiple_tables=True, stream=True)
                    read_successful = True
                except Exception as e_stream:
                    logging.error(f"Tabula stream=True also failed: {e_stream}")
                    # Check for common Java error
                    if "java" in str(e_stream).lower() or isinstance(e_stream, FileNotFoundError):
                         st.error("Error processing PDF: Java not found or not configured correctly. Please ensure Java Development Kit (JDK) is installed and in your system's PATH.")
                    else:
                        st.error(f"Failed to read PDF tables using Tabula: {e_stream}")
                    dfs_tabula = None # Ensure it's None on failure
            finally:
                # FIX: Ensure temporary file is always removed
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
                    logging.info(f"Removed temporary PDF file: {tmp_file_path}")

            if read_successful and isinstance(dfs_tabula, list):
                # Filter out empty DataFrames and check if any tables were found
                dfs_list = [df for df in dfs_tabula if isinstance(df, pd.DataFrame) and not df.empty]
                if not dfs_list:
                    st.warning("Tabula processed the PDF, but no data tables were found.")
                    logging.warning(f"No non-empty tables extracted from PDF: {uploaded_file.name}")
                    dfs_list = None # Set back to None if only empty tables found
                else:
                     logging.info(f"Successfully extracted {len(dfs_list)} table(s) from PDF.")

        else:
            st.error(f"Unsupported file format: '{file_extension}'. Please upload CSV, Excel, or PDF.")
            logging.error(f"Unsupported file type uploaded: {uploaded_file.name}")
            return None # Explicitly return None for unsupported types

        return dfs_list

    # FIX: Catch specific library errors and general exceptions during file reading
    except ImportError as ie:
         if 'tabula' in str(ie).lower():
             st.error("Processing Error: `tabula-py` library not installed or Java not found/configured. Cannot process PDF files.")
             logging.error("ImportError related to tabula-py or Java.")
         else:
            st.error(f"Import Error: {ie}. Please ensure required libraries (pandas, openpyxl, tabula-py) are installed.")
            logging.error(f"ImportError: {ie}")
         return None
    except Exception as e:
        st.error(f"An error occurred while reading '{uploaded_file.name}': {e}")
        st.warning("Please ensure the file is valid, not password-protected or corrupted, and that Java is installed (for PDF).")
        logging.error(f"Failed to load file {uploaded_file.name}: {e}", exc_info=True) # Log traceback
        return None


# FIX: Added show_spinner
@st.cache_data(show_spinner="Preparing download...")
def convert_df_to_csv(df):
    """Converts DataFrame to CSV bytes for download."""
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode('utf-8')

# --- Session State Initialization ---
# (Ensures variables persist across reruns)
if 'dataframes_list' not in st.session_state:
    st.session_state.dataframes_list = None
if 'selected_df_index' not in st.session_state:
    st.session_state.selected_df_index = 0
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'current_df' not in st.session_state:
    st.session_state.current_df = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
# 'dark_mode' initialized near st.set_page_config

# --- Sidebar ---
with st.sidebar: # ENHANCEMENT: Use 'with' context manager for sidebar clarity
    st.header("⚙️ Upload & Options")

    # ENHANCEMENT: Dark mode toggle removed
    def apply_custom_css():
        pass  # No custom css applied


    uploaded_file = st.file_uploader(
        "Choose a CSV, Excel, or PDF file",
        type=['csv', 'xlsx', 'xls', 'pdf'],
        accept_multiple_files=False,
        help="Upload your dataset (CSV, Excel, PDF)."
    )

    # --- File Processing Logic ---
    if uploaded_file is not None:
        # Process only if it's a new file or data hasn't been loaded successfully before
        if not st.session_state.data_loaded or uploaded_file.name != st.session_state.get('uploaded_file_name'):
            st.session_state.dataframes_list = load_data(uploaded_file) # Call robust load_data
            st.session_state.uploaded_file_name = uploaded_file.name
            st.session_state.selected_df_index = 0 # Reset index for new file

            if st.session_state.dataframes_list: # Check if load_data returned a valid list
                st.session_state.data_loaded = True
                # Handle multiple tables from PDF
                if len(st.session_state.dataframes_list) > 1:
                    st.success(f"Found {len(st.session_state.dataframes_list)} tables.")
                    table_options = {i: f"Table {i+1} (Shape: {df.shape})" for i, df in enumerate(st.session_state.dataframes_list)}
                    st.session_state.selected_df_index = st.selectbox(
                        "Select table to analyze:",
                        options=list(table_options.keys()),
                        format_func=lambda x: table_options[x],
                        key='pdf_table_select'
                    )
                else:
                    st.success(f"File '{uploaded_file.name}' loaded.")

                # Set initial dataframes in session state
                st.session_state.original_df = st.session_state.dataframes_list[st.session_state.selected_df_index].copy()
                st.session_state.current_df = st.session_state.original_df.copy()
                # Force a rerun to update the main panel immediately after successful load
                # st.rerun() # Careful with rerun, can cause loops if not managed well. Often UI updates automatically.

            else: # load_data returned None or empty list
                st.session_state.data_loaded = False
                st.session_state.original_df = None
                st.session_state.current_df = None
                # Error/Warning message is handled inside load_data()

        # Handling selection change for multi-table PDFs *after* initial load
        elif st.session_state.data_loaded and st.session_state.dataframes_list and len(st.session_state.dataframes_list) > 1:
            table_options = {i: f"Table {i+1} (Shape: {df.shape})" for i, df in enumerate(st.session_state.dataframes_list)}
            new_index = st.selectbox(
                "Select table to analyze:",
                options=list(table_options.keys()),
                index=st.session_state.selected_df_index, # Default to current selection
                format_func=lambda x: table_options[x],
                key='pdf_table_select_rerun'
            )
            if new_index != st.session_state.selected_df_index:
                st.session_state.selected_df_index = new_index
                # Update dfs based on new selection
                st.session_state.original_df = st.session_state.dataframes_list[st.session_state.selected_df_index].copy()
                st.session_state.current_df = st.session_state.original_df.copy()
                st.rerun() # Rerun needed to reflect the change in the main panel

    # --- Sidebar Analysis Options (Conditional Display) ---
    if st.session_state.data_loaded and st.session_state.current_df is not None:
        st.markdown("---") # Visual separator
        st.header("📊 Analysis Options")
        df = st.session_state.current_df # Use current (possibly cleaned) df

        analysis_options = ['Data Preview & Info', 'Data Cleaning']
        numeric_cols_exist = any(pd.api.types.is_numeric_dtype(dtype) for dtype in df.dtypes)

        if numeric_cols_exist:
            analysis_options.extend(['Column Statistics', 'Visualizations', 'Correlation Analysis'])
        else:
            st.warning("No numeric columns detected. Some analysis options disabled.", icon="⚠️")

        # Use session state to remember the choice, preventing reset on reruns
        if 'analysis_choice' not in st.session_state:
             st.session_state.analysis_choice = analysis_options[0] # Default choice

        st.session_state.analysis_choice = st.radio(
            "Choose Analysis:",
            analysis_options,
            index=analysis_options.index(st.session_state.analysis_choice), # Set index based on state
            key='analysis_radio' # Consistent key
        )
    else:
        # Clear analysis choice if data is unloaded
        if 'analysis_choice' in st.session_state:
            del st.session_state.analysis_choice


    # --- Footer ---
    st.markdown("---")
    st.caption("PPGTE | IUVI | UFC - SIDA 0.2.1")


# --- Main Application Area ---
st.title("📈 Ferramenta de Análise de Dados")

if not st.session_state.data_loaded or st.session_state.current_df is None:
    st.info("👈 Enviar um conjunto de dados (CSV, Excel, PDF) usando a barra lateral para iniciar a análise.")
    st.markdown("""
    **instruções:**
    1.  Use o botão na barra lateral para enviar o seu arquivo com o conjunto de dados que deseja analisar.
    2.  Se desejar enviar um PDF com múltiplas tabelas, selecione uma para analisar na lista suspensa da barra lateral.
    3.  Use as **Opções de Análise** na barra lateral para explorar e limpar seus dados.
    4.  Ative o **Modo Escuro** na barra lateral para o tema de visualização que preferir.
    """)
else:
    df = st.session_state.current_df # Work with the current dataframe
    analysis_type = st.session_state.analysis_choice # Get selected analysis from state

    st.header(f"🔎 {analysis_type}") # Show title for the selected analysis

    # --- Data Preview & Info ---
    if analysis_type == 'Data Preview & Info':
        # ENHANCEMENT: Use st.columns for better layout
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Informação básica do conjunto de dados")
            st.write(f"**Nome do Arquivo:** `{st.session_state.uploaded_file_name}`")
            if st.session_state.dataframes_list and len(st.session_state.dataframes_list) > 1:
                st.write(f"**Tabela Selecionada:** `Table {st.session_state.selected_df_index + 1}`")
            st.write(f"**Linhas:** `{df.shape[0]}`")
            st.write(f"**Colunas:** `{df.shape[1]}`")
        with col2:
             st.subheader("Tipos de Colunas")
             # Improve display of dtypes
             st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={'index': 'Column', 0: 'DataType'}), height=200, use_container_width=True, hide_index=True)

        st.subheader("Data Preview")
        st.dataframe(df.head()) # Show first 5 rows by default

        # ENHANCEMENT: Use st.expander for download section
        with st.expander("Baixar Dados"):
            st.markdown("Baixe os dados *conforme exibido atualmente* (incluindo qualquer limpeza).")
            csv_data = convert_df_to_csv(df) # Use cached function
            st.download_button(
                label="⬇️ Baixar Dados como CSV",
                data=csv_data,
                file_name=f"current_data_{st.session_state.uploaded_file_name.split('.')[0]}{'_T'+str(st.session_state.selected_df_index+1) if st.session_state.dataframes_list and len(st.session_state.dataframes_list)>1 else ''}.csv",
                mime='text/csv',
                key='download-current-csv'
            )

    # --- Data Cleaning ---
    elif analysis_type == 'Data Cleaning':
        st.subheader("Tratar Valores Ausentes")

        # ENHANCEMENT: Use spinner for calculations if dataset is large
        with st.spinner("Analisando valores ausentes..."):
            missing_values = df.isnull().sum()
            missing_summary = missing_values[missing_values > 0].sort_values(ascending=False)

        # ENHANCEMENT: Use st.columns for layout
        col1, col2 = st.columns([1, 2]) # Column for summary, column for options

        with col1:
            st.write("**Resumo de Valores Ausentes:**")
            if not missing_summary.empty:
                st.dataframe(missing_summary.reset_index().rename(columns={'index': 'Coluna', 0: 'Contagem de Ausentes'}), use_container_width=True, hide_index=True)
                st.metric(label="Total de Valores Ausentes", value=f"{missing_summary.sum():,}") # Formatted number
            else:
                st.success("✅ Nenhum valor ausente encontrado!")

            if st.button("🔄 Resetar para os Dados Originais", key='reset_data', help="Descarta todas as etapas de limpeza aplicadas nesta sessão."):
                # ENHANCEMENT: Use spinner for reset action
                with st.spinner("Resetando dados..."):
                    st.session_state.current_df = st.session_state.original_df.copy()
                    st.success("Dados restaurados para o estado original.")
                st.rerun() # Rerun to reflect the reset

        with col2:
            if not missing_summary.empty:
                st.write("**Opções de Limpeza:**")
                # FIX: Ensure unique keys for widgets if they might reappear
                cleaning_strategy = st.radio(
                    "Escolha uma estratégia:",
                    ('Remover linhas com valores ausentes',
                     'Remover colunas com valores ausentes',
                     'Impute missing values (Fill)'),
                    key='clean_strategy_radio'
                )

                imputation_method = None
                constant_value = None
                cols_to_impute = None

                if cleaning_strategy == 'Impute missing values (Fill)':
                    imputation_method = st.selectbox(
                        "Método de Imputação:",
                        ('Média (Apenas Numérico)', 'Mediana (Apenas Numérico)', 'Moda (Mais Frequente)', 'Valor Constante', 'Preencher para Frente (ffill)', 'Preencher para Trás (bfill)'), # Added ffill/bfill
                        key='impute_method_select'
                    )
                    if imputation_method == 'Valor Constante':
                        constant_value = st.text_input("Digite o valor constante para preencher:", value="NA", key='impute_constant_input')

                    # Option to select columns for imputation
                    all_cols_with_na = missing_summary.index.tolist()
                    cols_to_impute = st.multiselect(
                        "Selecione as colunas para imputação (padrão: todas com valores ausentes):",
                        options=df.columns.tolist(),
                        default=all_cols_with_na,
                        key='impute_cols_multi'
                    )

                if st.button("✨ Aplicar Limpeza", key='apply_cleaning_button'):
                    # ENHANCEMENT: Use spinner for cleaning action
                    with st.spinner("Aplicando regras de limpeza..."):
                        df_cleaned = df.copy() # Work on a copy
                        action_taken = "Nenhuma alteração aplicada." # Default message
                        try:
                            if cleaning_strategy == 'Drop rows with any missing values':
                                rows_before = len(df_cleaned)
                                df_cleaned.dropna(axis=0, inplace=True)
                                rows_after = len(df_cleaned)
                                action_taken = f"Removidas {rows_before - rows_after} linhas com valores ausentes."
                            elif cleaning_strategy == 'Drop columns with any missing values':
                                cols_before = df_cleaned.shape[1]
                                df_cleaned.dropna(axis=1, inplace=True)
                                cols_after = df_cleaned.shape[1]
                                action_taken = f"Removidas {cols_before - cols_after} colunas com valores ausentes."

                            elif cleaning_strategy == 'Impute missing values (Fill)':
                                if not cols_to_impute:
                                    st.warning("Por favor, selecione pelo menos uma coluna para imputação.")
                                    action_taken = "Nenhuma coluna selecionada para imputação."
                                else:
                                    imputed_cols_count = 0
                                    skipped_cols = []
                                    for col in cols_to_impute:
                                        if col not in df_cleaned.columns or not df_cleaned[col].isnull().any():
                                            continue # Skip if column doesn't exist or has no NaNs

                                        if imputation_method in ['Mean (Numeric Only)', 'Median (Numeric Only)']:
                                            if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                                                fill_value = df_cleaned[col].mean() if 'Mean' in imputation_method else df_cleaned[col].median()
                                                df_cleaned[col].fillna(fill_value, inplace=True)
                                                imputed_cols_count += 1
                                            else:
                                                skipped_cols.append(col)
                                        elif imputation_method == 'Mode (Most Frequent)':
                                            mode_val = df_cleaned[col].mode()
                                            if not mode_val.empty:
                                                df_cleaned[col].fillna(mode_val[0], inplace=True)
                                                imputed_cols_count += 1
                                            else: skipped_cols.append(col) # Handle cases with no mode
                                        elif imputation_method == 'Constant Value':
                                            try: # Attempt type conversion for consistency
                                                typed_value = pd.Series([constant_value]).astype(df_cleaned[col].dtype).iloc[0]
                                            except Exception:
                                                typed_value = constant_value # Use raw value if conversion fails
                                            df_cleaned[col].fillna(typed_value, inplace=True)
                                            imputed_cols_count += 1
                                        elif imputation_method == 'Forward Fill (ffill)':
                                             df_cleaned[col].ffill(inplace=True)
                                             imputed_cols_count += 1
                                        elif imputation_method == 'Backward Fill (bfill)':
                                             df_cleaned[col].bfill(inplace=True)
                                             imputed_cols_count += 1

                                    action_taken = f"Imputed {imputed_cols_count} column(s) using {imputation_method}."
                                    if skipped_cols:
                                        st.warning(f"Skipped non-numeric columns for Mean/Median or columns with no mode: {', '.join(skipped_cols)}", icon="⚠️")

                            # Update the main dataframe in session state
                            st.session_state.current_df = df_cleaned
                            st.success(f"Cleaning applied: {action_taken}")
                            logging.info(f"Data cleaning action: {action_taken}")
                            st.rerun() # Rerun to update display (summary, preview)

                        except Exception as clean_e:
                            st.error(f"Error during cleaning: {clean_e}")
                            logging.error(f"Cleaning failed: {clean_e}", exc_info=True)
            else:
                st.info("Select a cleaning strategy and click 'Apply Cleaning'.")


    # --- Column Statistics ---
    elif analysis_type == 'Column Statistics':
        st.subheader("Descriptive Statistics (Numeric Columns)")
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not numeric_cols:
            st.warning("No numeric columns found in the current dataset.")
        else:
            # ENHANCEMENT: Use spinner for describe() if large
            with st.spinner("Calculating statistics..."):
                stats_df = df[numeric_cols].describe()
            st.dataframe(stats_df, use_container_width=True)

    # --- Visualizations ---
    elif analysis_type == 'Visualizations':
        st.subheader("Interactive Plots")
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        all_cols = df.columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns available for plotting.")
        else:
            # ENHANCEMENT: Use st.tabs for different plot types
            tab1, tab2 = st.tabs(["📊 Histogram", "📈 Scatter Plot"])

            with tab1:
                st.markdown("#### Histogram")
                hist_col = st.selectbox("Select column:", numeric_cols, key='hist_col_select_tab')
                # ENHANCEMENT: Add optional color dimension
                hist_color = st.selectbox("Optional: Color by:", [None] + all_cols, key='hist_color_select_tab')

                if hist_col:
                     # ENHANCEMENT: Use spinner for plotting
                    with st.spinner("Generating Histogram..."):
                        try:
                            fig_hist = px.histogram(df, x=hist_col, color=hist_color, title=f'Histogram of {hist_col}' + (f' (Colored by {hist_color})' if hist_color else ''))
                            fig_hist.update_layout(bargap=0.1)
                            st.plotly_chart(fig_hist, use_container_width=True)
                        except Exception as e:
                            st.error(f"Could not generate histogram: {e}")
                            logging.error(f"Histogram error for {hist_col}: {e}", exc_info=True)

            with tab2:
                st.markdown("#### Scatter Plot")
                if len(numeric_cols) >= 2:
                    # FIX: Ensure unique keys for widgets in tabs
                    scatter_x = st.selectbox("Select X-axis:", numeric_cols, index=0, key='scatter_x_select_tab')
                    # Try to select a different default Y axis
                    default_y_index = 1 if len(numeric_cols) > 1 and numeric_cols[1] != scatter_x else 0
                    scatter_y = st.selectbox("Select Y-axis:", numeric_cols, index=default_y_index, key='scatter_y_select_tab')
                    scatter_color = st.selectbox("Optional: Color by:", [None] + all_cols, key='scatter_color_select_tab')
                    scatter_size = st.selectbox("Optional: Size by (Numeric):", [None] + numeric_cols, key='scatter_size_select_tab') # ENHANCEMENT: Size dimension


                    if scatter_x and scatter_y:
                         # ENHANCEMENT: Use spinner for plotting
                        with st.spinner("Generating Scatter Plot..."):
                            try:
                                fig_scatter = px.scatter(df, x=scatter_x, y=scatter_y,
                                                         color=scatter_color, size=scatter_size,
                                                         title=f'Scatter: {scatter_x} vs {scatter_y}' + (f' (Color: {scatter_color})' if scatter_color else '') + (f' (Size: {scatter_size})' if scatter_size else ''))
                                st.plotly_chart(fig_scatter, use_container_width=True)
                            except Exception as e:
                                st.error(f"Could not generate scatter plot: {e}")
                                logging.error(f"Scatter plot error ({scatter_x} vs {scatter_y}): {e}", exc_info=True)
                else:
                    st.warning("Requires at least two numeric columns for a scatter plot.")

    # --- Correlation Analysis ---
    elif analysis_type == 'Correlation Analysis':
        st.subheader("Correlation Analysis (Numeric Columns)")
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if len(numeric_cols) < 2:
            st.warning("Requires at least two numeric columns to calculate correlations.")
        else:
            # ENHANCEMENT: Use spinner
            with st.spinner("Calculating correlations..."):
                try:
                    # FIX: Ensure only numeric calculations if mixed types are suspected
                    correlation_matrix = df[numeric_cols].corr(numeric_only=True)

                    # ENHANCEMENT: Use st.tabs for table vs heatmap
                    tab1, tab2 = st.tabs(["🔢 Matrix Table", "🔥 Heatmap"])

                    with tab1:
                        st.dataframe(correlation_matrix, use_container_width=True)

                    with tab2:
                        # ENHANCEMENT: Use spinner for potentially large heatmap render
                         with st.spinner("Generating Heatmap..."):
                            try:
                                fig_corr = px.imshow(
                                    correlation_matrix,
                                    text_auto=True, # Show values on heatmap
                                    aspect="auto",
                                    color_continuous_scale='RdBu_r', # Red-Blue diverging scale good for correlation
                                    title='Correlation Heatmap'
                                )
                                fig_corr.update_layout(coloraxis_colorbar=dict(title='Correlation'))
                                st.plotly_chart(fig_corr, use_container_width=True)
                            except Exception as e_heatmap:
                                st.error(f"Could not generate correlation heatmap: {e_heatmap}")
                                logging.error(f"Correlation heatmap error: {e_heatmap}", exc_info=True)

                except Exception as corr_e:
                     st.error(f"Could not calculate correlations. Ensure numeric columns contain valid numbers. Error: {corr_e}")
                     logging.error(f"Correlation calculation error: {corr_e}", exc_info=True)