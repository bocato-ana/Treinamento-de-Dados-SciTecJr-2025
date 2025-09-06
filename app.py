import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if'df' not in st.session_state:
    st.session_state['df'] = pd.read_parquet('Student Mental health.parquet')


#st.write(st.session_state['df'])

#st.data_editor(st.session_state['df'],
 #              num_rows="dynamic",
  #             use_container_width=True)


pg = st.navigation([
    st.Page("pages/pag1.py", title="Dashboard"),
    st.Page("pages/pag2.py", title="Forms"),
    st.Page("pages/pag3.py", title="Machine Learning")
])

pg.run()
