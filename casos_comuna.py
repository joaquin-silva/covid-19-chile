import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto45/CasosConfirmadosPorComuna_std.csv')
    df['Año'] = [int(str(semana)[:4]) for semana in df['Semana Epidemiologica']]
    df['Numero Semana'] = [int(str(semana)[-2:]) for semana in df['Semana Epidemiologica']]
    df['Casos 100 mil'] = 100000*df['Casos confirmados']/df['Poblacion']
    return df

@st.cache
def get_data_inicio_sintomas():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/FechaInicioSintomas_std.csv')
    df['Año'] = [int(str(semana)[:4]) for semana in df['Semana Epidemiologica']]
    df['Numero Semana'] = [int(str(semana)[-2:]) for semana in df['Semana Epidemiologica']]
    df['Casos 100 mil'] = 100000*df['Casos confirmados']/df['Poblacion']
    return df

def my_plot(df, comunas, op, op_data, op_plot):
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

def my_heatmap(df, comunas, op, op_data):
    data = df[df['Comuna'].isin(comunas)]
    if op:
        z = data['Casos 100 mil']
    else:
        z = data['Casos confirmados']

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=data['Numero Semana'],
        y=data['Comuna'],   
        colorscale='inferno_r'
        ))

    fig.update_layout(
        title=f'{op_data} por semana epidemiológica',
        xaxis_title="Semana epidemiológica",
        template='ggplot2',
        autosize=False,
        height=300 + 25*len(comunas) ,
    )

    return fig

def main():
    st.title('Casos por comuna')
    
    st.sidebar.markdown('---')
    st.sidebar.markdown('Opciones')

    op_año = st.sidebar.selectbox('Año', [2020,2021])
    op_data = st.sidebar.selectbox('Datos', ['Casos confirmados','Casos nuevos por fecha de inicio de síntomas'], key=0)
    
    if op_data == 'Casos confirmados':
        df = get_data()
    if op_data == 'Casos nuevos por fecha de inicio de síntomas':
        df = get_data_inicio_sintomas()

    df = df[df['Año']==op_año]

    op_plot = st.sidebar.selectbox('Tipo gráfico', ['Lineas','Barras','Heatmap'])
    op = st.sidebar.checkbox('Ver casos por 100.000 habitantes', value=False, key=0)

    comunas = list(set(df['Comuna']))
    select = st.multiselect('Seleccionar comunas', comunas, ['Antofagasta','Puente Alto','Punta Arenas'])

    if op_plot != 'Heatmap':
        try:
            fig = my_plot(df, select, op, op_data, op_plot)
            st.plotly_chart(fig, use_container_width=True) 
        except:
            st.write('Demasiadas comunas seleccionadas')
    else:
        fig = my_heatmap(df, select, op, op_data)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Nota:** Los datos de las últimas semanas se pueden ir ajustando con el paso del tiempo.")

    st.markdown("---")
    st.markdown("Autor: [Joaquín Silva](https://github.com/joaquin-silva)")
    st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")

if __name__ == "__main__":
    main()