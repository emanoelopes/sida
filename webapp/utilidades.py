from pathlib import Path
import streamlit as st
import pandas as pd
import os

def leitura_oulad_data():
    datasets_path = Path(__file__).parent.parents / 'datasets' / 'oulad_data'
    st.write(f"Path dos datasets: {datasets_path}")
