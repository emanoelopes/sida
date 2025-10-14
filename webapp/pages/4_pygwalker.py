import pandas as pd
import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st

if "df_uci" in st.session_state:
    df = st.session_state['df_uci']
    walker = pyg.walk(df)
else:
    st.write("Nenhum dado disponível. Por favor, navegue para a página UCI primeiro.")
