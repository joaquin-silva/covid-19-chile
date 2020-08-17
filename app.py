import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
import calendar

import defunciones_registro
import casos_covid
import casos_comuna
import vista_deis

# cd Downloads\Python\Streamlit
# streamlit run app.py    

# Config
st.beta_set_page_config(
    page_title="Covid-19 Chile",
 	layout="centered",
 	initial_sidebar_state="expanded",
)

# Sidebar   
st.sidebar.title('Navegación')
opt = st.sidebar.radio("",
    ("Casos", "Defunciones Registro Civil", "Datos Deis")
)

if opt == "Defunciones Registro Civil":
    defunciones_registro.main()

if opt == "Casos":
    casos_covid.main()

if opt == "Datos Deis":
    vista_deis.main()
