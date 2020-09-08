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

def my_plot(df):
    colors = ["royalblue","skyblue","palevioletred","mediumpurple"]
    fig = go.Figure()
    for i, tipo in enumerate(df.columns[1:]):
        fig.add_trace(go.Scatter(x=df["Fecha"], y=df[tipo], mode='lines', name=tipo, marker_color=colors[i]))
    fig.update_layout(
        title_text='Ocupación de camas hospitalarias',
        xaxis_title='Fecha',
        template='ggplot2',
        )
    return fig

@st.cache
def get_data_sochimi():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto48/SOCHIMI_std.csv')
    df['Vmi otro'] = df['Vmi ocupados'] - df['Vmi covid19 confirmados'] - df['Vmi covid19 sospechosos']
    df = df.drop(columns=['Codigo region'])
    return df

def my_groupby_reg(df):
    return df.groupby(['Fecha','Region'], as_index=False).sum()

def my_groupby_nat(df):
    return df.groupby(['Fecha'], as_index=False).sum()

def my_plot_vmi(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Vmi covid19 confirmados'], name='VMI Covid-19 confirmado', stackgroup='one', marker_color='red'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Vmi covid19 sospechosos'], name='VMI Covid-19 sospechoso', stackgroup='one', marker_color='orange'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Vmi otro'], name='VMI Otro',stackgroup='one', marker_color='steelblue'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Vmi totales'], name='VMI Totales', marker_color='silver'))
    fig.update_layout(
        title="Ocupación de Ventiladores Mecánicos Invasivos (VMI)",
        xaxis_title="Fecha",
        yaxis_title="Ventiladores",
        template='ggplot2',
        barmode='stack'
        )
    return fig

def main():
    st.title('Ocupación Hospitalaria Nacional')

    df = get_data()
    fig = my_plot(df)
    st.plotly_chart(fig, use_container_width=True)

    if st.checkbox("Mostrar datos", value=False, key=0): 
        st.write(df) 

    st.markdown("---")
    st.title('Encuesta SOCHIMI')

    st.write('Datos de la encuesta diaria realidad nacional medicina intensiva provistos por el Ministerio de Ciencia en su [producto 48](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto48).')
   
    df = get_data_sochimi()
    regiones = list(set(df['Region']))
    st.sidebar.markdown("---")
    reg = st.sidebar.selectbox('Elegir Región', regiones, key=0, index=regiones.index('Metropolitana'))

    if st.checkbox("Mostrar datos", value=False, key=1): 
        st.write(df)

    st.header('Ocupación de VMI Nacional')

    data = my_groupby_nat(df)
    fig = my_plot_vmi(data)
    st.plotly_chart(fig, use_container_width=True)

    st.header(f'Ocupación de VMI en Región {reg}')
    data = my_groupby_reg(df)
    df_reg = data[data['Region']==reg]

    fig = my_plot_vmi(df_reg)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("Autor: [Joaquín Silva](https://github.com/joaquin-silva)")
    st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")