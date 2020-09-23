import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto45/CasosConfirmadosPorComuna_std.csv')
    df['Numero Semana'] = [int(semana.split('SE')[1]) for semana in df['Semana Epidemiologica']]
    df['Casos 100 mil'] = 100000*df['Casos confirmados']/df['Poblacion']
    return df

@st.cache
def get_data_inicio_sintomas():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/FechaInicioSintomas_std.csv')
    df['Numero Semana'] = [int(semana.split('SE')[1]) for semana in df['Semana Epidemiologica']]
    df['Casos 100 mil'] = 100000*df['Casos confirmados']/df['Poblacion']
    return df

def new_cases_plot(df, op, op_data, op_plot):
    if op:
        y = df['Casos 100 mil']
    else:
        y = df['Casos confirmados']
    fig = go.Figure()
    if op_plot == 'Barras':
        fig.add_trace(go.Bar(x=df['Numero Semana'], y=y, marker_color='cadetblue'))
    if op_plot == 'Lineas':
        fig.add_trace(go.Scatter(x=df['Numero Semana'], y=y, marker_color='cadetblue', mode='lines'))
    fig.update_layout(
        title=f'{op_data} por semana epidemiológica en {list(set(df["Comuna"]))[0]}',
        xaxis_title="Semana epidemiológica",
        yaxis_title="Casos",
        template='ggplot2',
        height=550
    )
    return fig

def my_plot(df, comunas, op, op_data, op_plot):
    colors = ['#d62728','#1f77b4', '#ff7f0e', '#2ca02c', '#ff9896', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22']
    fig = go.Figure()
    for i, comuna in enumerate(comunas):
        aux = df[df['Comuna']==comuna]
        if op:
            y = aux['Casos 100 mil']
        else:
            y = aux['Casos confirmados']
        if op_plot == 'Barras':
            fig.add_trace(go.Bar(x=aux['Numero Semana'], y=y, name=comuna, marker_color=px.colors.qualitative.G10[i]))
        if op_plot == 'Lineas':
            fig.add_trace(go.Scatter(x=aux['Numero Semana'], y=y, name=comuna, marker_color=px.colors.qualitative.G10[i], mode='lines'))
    fig.update_layout(
        barmode='group',
        title=f'{op_data} por semana epidemiológica',
        xaxis_title="Semana epidemiológica",
        yaxis_title="Casos",
        template='ggplot2',
        height=550
    )
    return fig

def main():
    st.title('Casos por comuna')
    
    st.sidebar.markdown('---')
    st.sidebar.markdown('Opciones')
    op_data = st.sidebar.selectbox('Datos', ['Casos confirmados','Casos nuevos por fecha de inicio de síntomas'], key=0)
    
    if op_data == 'Casos confirmados':
        df = get_data()
    if op_data == 'Casos nuevos por fecha de inicio de síntomas':
        df = get_data_inicio_sintomas()

    op_plot = st.sidebar.selectbox('Tipo gráfico', ['Lineas','Barras'])
    op = st.sidebar.checkbox('Ver casos por 100.000 habitantes', value=False, key=0)

    regiones = list(set(df['Region']))
    reg = st.selectbox('Región', regiones, index=regiones.index('Metropolitana'), key=1)
    df_reg = df[df['Region']==reg]

    comunas = list(set(df_reg['Comuna']))
    comuna = st.selectbox('Comuna', comunas)
    df_com = df_reg[df_reg['Comuna']==comuna]

    fig = new_cases_plot(df_com, op, op_data, op_plot)
    st.plotly_chart(fig, use_container_width=True) 

    st.markdown('---')
    st.header('Comparación por comunas')

    comunas = list(set(df['Comuna']))
    select = st.multiselect('Seleccionar comunas', comunas, ['Antofagasta','Puente Alto','Punta Arenas'])
    try:
        fig = my_plot(df, select, op, op_data, op_plot)
        st.plotly_chart(fig, use_container_width=True) 
    except:
        st.write('Demasiadas comunas seleccionadas')

    st.markdown("**Nota:** Los datos de las últimas semanas se pueden ir ajustando con el paso del tiempo.")

    st.markdown("---")
    st.markdown("Autor: [Joaquín Silva](https://github.com/joaquin-silva)")
    st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")

if __name__ == "__main__":
    main()
