import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna_std.csv')
    return df

def my_groupby(df):
    df = df[df['Fecha'] == max(df['Fecha'])]
    data = df.groupby(by=['Region','Comuna'], as_index=False).sum()
    data = data[data['Comuna'] != 'Total']
    data = data[['Region','Comuna','Casos activos']]
    data = data.sort_values('Casos activos', ascending=False).reset_index(drop=True)
    return data

def plot_mas_activos(data):
    cant = 20
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=data['Comuna'][:cant][::-1],
        x=data['Casos activos'][:cant][::-1],
        text=data['Casos activos'][:cant][::-1],
        textposition='inside',
        orientation='h',
        marker_color='steelblue'))
    fig.update_layout(
        title=f'Las {cant} comunas con más casos activos',
        xaxis_title='Casos activos',
        template='ggplot2',
        height=700,
    )
    return fig

def plot_activos_region(df):
    df = df[df['Fecha'] == max(df['Fecha'])]
    data = df.groupby(by=['Region'], as_index=False).sum()
    data = data[['Region','Casos activos']]
    data = data.sort_values('Casos activos', ascending=False).reset_index(drop=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=data['Region'][::-1],
        x=data['Casos activos'][::-1],
        text=data['Casos activos'][::-1],
        textposition='inside',
        orientation='h',
        marker_color='steelblue'))

    fig.update_layout(
        title='Casos activos por región',
        xaxis_title='Casos activos',
        template='ggplot2',
        height=750,
    )
    return fig


def plot_comunas(data):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=data['Comuna'][::-1],
        x=data['Casos activos'][::-1],
        text=data['Casos activos'][::-1],
        textposition='inside',
        orientation='h',
        marker_color='steelblue'))
    
    if data.shape[0] > 25:
        height = 25*data.shape[0]
    else:
        height = 500

    fig.update_layout(
        title='Casos activos por comuna',
        xaxis_title='Casos activos',
        template='ggplot2',
        height=height,
    )
    return fig


def main():
    st.title('Casos Activos')
    df = get_data()

    d, m, y = max(df['Fecha']).split('-')[::-1]
    fecha = f'{d}-{m}-{y}'
    st.header('Descripción')
    st.markdown(f'''
    - Datos correspondientes a la cantidad de casos confirmados activos notificados en cada una de las comunas de Chile.
    - Casos activos a la fecha {fecha}.
    ''')

    #fechas = sorted(list(set(df['Fecha'])))
    #f = st.select_slider('Cambiar fecha de informe', options=fechas)

    st.header('Comunas con más casos activos')
    data = my_groupby(df)

    fig = plot_mas_activos(data)
    st.plotly_chart(fig, use_container_width=True) 

    st.write('---')
    st.header('Casos activos por región')

    fig = plot_activos_region(df)
    st.plotly_chart(fig, use_container_width=True) 

    st.write('---')
    st.header('Casos activos por comuna')

    regiones = list(set(data['Region']))
    reg = st.selectbox('Región', regiones, index=regiones.index('Metropolitana'))

    data_reg = data[data['Region']==reg]
    fig = plot_comunas(data_reg)
    st.plotly_chart(fig, use_container_width=True) 


if __name__ == "__main__":
    main()