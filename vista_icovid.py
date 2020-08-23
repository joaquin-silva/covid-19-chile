import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data_comuna():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto55/Positividad_por_comuna.csv')
    return df

@st.cache
def get_data_reg():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto55/Positividad_por_region.csv')
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

def my_plot_reg(df, regiones, op):
    fig = go.Figure()
    for i, region in enumerate(regiones):
        aux = df[df['Region']==region]
        aux = aux.sort_values(by=['fecha']).reset_index(drop=True)
        if op:
            y = aux['positividad'].rolling(7).mean()
        else:
            y = aux['positividad']
        fig.add_trace(go.Scatter(
            x=aux['fecha'],
            y=100*y,
            name=str(region),
            mode='lines'
        ))
    fig.update_layout(
        title_text="Positividad Exámenes PCR",
        xaxis_title="Fecha",
        yaxis_title="Porcentaje Positividad",
    )
    return fig

def main():
    st.title('Positividad ICOVID Chile')

    st.header('Vista regional')
    
    df = get_data_reg()
    l_reg = list(set(df['Region']))
    regiones = st.multiselect('Regiones', l_reg, l_reg, key=0)

    op = st.checkbox("Suavizar datos (Promedio móvil 7 días)", value=True, key=0)
    fig = my_plot_reg(df, regiones, op)
    st.plotly_chart(fig, use_container_width=True) 

    st.header('Vista comunal')

    df = get_data_comuna()
    regiones = list(set(df['Region']))
    reg = st.selectbox('Region', regiones, index=regiones.index('Metropolitana'))
    df_reg = df[df['Region']==reg].reset_index(drop=True)

    l_comunas = list(set(df_reg['Comuna']))
    comunas = st.multiselect('Comunas', l_comunas, l_comunas, key=1)

    op = st.checkbox("Suavizar datos (Promedio móvil 7 días)", value=True, key=1)
    fig = my_plot(df, comunas, op)
    st.plotly_chart(fig, use_container_width=True) 

    st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")