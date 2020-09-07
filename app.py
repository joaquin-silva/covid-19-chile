import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
import calendar
import os

import defunciones_registro
import casos_covid
import vista_deis
import ocupacion_hospitalaria
import vista_icovid
import reporte_diario
import casos_comuna
import casos_activos

# cd Downloads\Python\Streamlit\Covid-19
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
    ("Reporte Diario",
    "Casos por región",
    "Casos por comuna",
    "Defunciones Registro Civil",
    "Datos Deis",
    "Ocupación Hospitalaria",
    "Positivad Diaria",
    "Casos Activos"
    )
)

if opt == "Defunciones Registro Civil":
    defunciones_registro.main()

if opt == "Casos por región":
    casos_covid.main()

if opt == "Datos Deis":
    vista_deis.main()

if opt == "Ocupación Hospitalaria":
    ocupacion_hospitalaria.main()

if opt == "Positivad Diaria":
    vista_icovid.main()

if opt == "Reporte Diario":
    reporte_diario.main()

if opt == "Casos por comuna":
    casos_comuna.main()

if opt == "Casos Activos":
    casos_activos.main()
