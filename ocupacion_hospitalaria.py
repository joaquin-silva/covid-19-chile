import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto24/CamasHospital_Diario_T.csv')
    df = df.rename(columns={"Tipo de cama": "Fecha"})
    return df

@st.cache
def my_plot(df):
    colors = ["royalblue","skyblue","palevioletred","mediumpurple"]
    fig = go.Figure()
    for i, tipo in enumerate(df.columns[1:]):
        fig.add_trace(go.Scatter(x=df["Fecha"], y=df[tipo], mode='lines', name=tipo, marker_color=colors[i]))
    fig.update_layout(
        title_text='Ocupación de camas hospitalarias',
        xaxis_title='Fecha',
        template='ggplot2'
        )
    return fig

def main():
    st.title('Ocupación Hospitalaria Nacional')

    df = get_data()
    fig = my_plot(df)
    st.plotly_chart(fig, use_container_width=True)

    if st.checkbox("Mostrar datos", value=False): 
        st.write(df) 

    st.markdown("Autor: [Joaquín Silva](https://github.com/joaquin-silva)")
    st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")
    st.markdown("---")