from pathlib import Path
import streamlit as st
import pandas as pd

def leitura_oulad_data():
    datasets_path = Path(__file__).parent.parents / 'datasets' / 'oulad_data'
    st.write(f"Path dos datasets: {datasets_path}")


# Create visualization selection in sidebar
with st.sidebar:
    st.markdown("### Escolha o dataset ")
    eda_dataset = st.selectbox(
        "Analise",
        ["UCI EDA", "OULAD EDA"]
    ) 
           
    ### footer
    st.markdown("Mestrado em Tecnologia Educacional - UFC")



if eda_dataset is 'UCI EDA':
    st.write("UCI EDA")
else
    st.write("OULAD EDA")
