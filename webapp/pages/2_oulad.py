from pathlib import Path
import streamlit as st
import pandas as pd
import os

from utilidades import leitura_de_dados

df_stinfo = st.session_state['dataframes']['studentInfo']

st.dataframe(df_stinfo)