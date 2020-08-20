import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto55/Positividad_por_comuna.csv')
    return df

def my_plot(df, comunas, op):
    fig = go.Figure()
    for i, comuna in enumerate(comunas):
        aux = df[df['Comuna']==comuna]
        aux = aux.sort_values(by=['fecha']).reset_index(drop=True)
        if op:
            y = aux['positividad'].rolling(7).mean()
        else:
            y = aux['positividad']
        fig.add_trace(go.Scatter(
            x=aux['fecha'],
            y=100*y,
            name=str(comuna),
            mode='lines'
        ))
    fig.update_layout(
        title_text="Positividad Exámenes PCR",
        xaxis_title="Fecha",
        yaxis_title="Porcentaje Positividad",
    )
    return fig

def main():
    st.title('Positividad Diaria')

    df = get_data()
    regiones = list(set(df['Region']))
    reg = st.selectbox('Region', regiones, index=regiones.index('Metropolitana'))
    df_reg = df[df['Region']==reg].reset_index(drop=True)
    l_comunas = list(set(df_reg['Comuna']))
    comunas = st.multiselect('Comunas', l_comunas, l_comunas)

    op = st.checkbox("Suavizar datos (Promedio móvil 7 días)", value=True)
    fig = my_plot(df, comunas, op)
    st.plotly_chart(fig, use_container_width=True) 

    st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")