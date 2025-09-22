from pathlib import Path
import streamlit as st
import pandas as pd
import os

from utilidades import leitura_uci_data

df_stinfo = st.session_state['dataframes_uci']['portuguese']

st.dataframe(df_stinfo)