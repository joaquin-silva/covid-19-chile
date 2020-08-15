import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import datetime

import defunciones_registro
import casos_covid

# cd Downloads\Python\Streamlit
# streamlit run main.py    

# Config
st.beta_set_page_config(
    page_title="Covid-19 Chile",
 	layout="centered",
 	initial_sidebar_state="expanded",
)

# Sidebar   
st.sidebar.title('Navegación')
opt = st.sidebar.radio("",
    ("Casos", "Defunciones Registro Civil", "Más")
)

if opt == "Defunciones Registro Civil":
    defunciones_registro.main()

if opt == "Casos":
    casos_covid.main()

if opt == "Más":
    st.write("En construcción...")