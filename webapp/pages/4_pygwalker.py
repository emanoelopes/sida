import pandas as pd
import pygwalker as pyg
import streamlit as st
import pygwalker as pyg

df = st.session_state['df_uci']
walker = pyg.walk(df)