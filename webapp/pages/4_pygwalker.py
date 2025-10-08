import pandas as pd
import pygwalker as pyg
import streamlit as st
import pygwalker as pyg

df = st.session_state['df_uci']
walker = pyg.walk(df)

import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
 
st.set_page_config(page_title="PyGWalker in Streamlit", layout="wide")
st.title("PyGWalker in Streamlit Demo")
 
@st.cache_resource
def get_pyg_renderer() -> StreamlitRenderer:
    return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw")
 
renderer = get_pyg_renderer()
 
tab1, tab2, tab3 = st.tabs(["Explorer", "Data Profiling", "Charts"])
 
with tab1:
    renderer.explorer()
 
with tab2:
    renderer.explorer(default_tab="data")
 
with tab3:
    st.subheader("Registered per Weekday")
    renderer.chart(0)
    st.subheader("Registered per Day")
    renderer.chart(1)