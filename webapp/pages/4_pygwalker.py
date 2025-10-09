import pandas as pd
import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st

df = st.session_state['df_uci']
walker = pyg.walk(df)
 
