import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto32/Defunciones_std.csv')
    df["Año"] = [df["Fecha"][i].split("-")[0] for i in range(df.shape[0])]
    df["Mes"] = [df["Fecha"][i].split("-")[1] for i in range(df.shape[0])]
    df["Dia"] = [df["Fecha"][i].split("-")[2] for i in range(df.shape[0])]
    df = df[[int(df['Año'][i])>=2016 for i in range(df.shape[0])]].reset_index(drop=True)
    l_semana = [datetime.datetime.strptime(df["Fecha"][i], '%Y-%m-%d').date().isocalendar()[1] for i in range(df.shape[0])]
    df['Semana'] = l_semana

    data = df.groupby(['Año','Semana','Region','Comuna'],as_index=False).sum()
    data = data.drop(columns=['Codigo region','Codigo comuna'])
    return data

def grafico_nacional(dfs):
    fig = go.Figure()
    colors = ["seagreen","teal","deepskyblue","gray","red"]
    grouped = dfs.groupby("Año")
    i = 0
    for year, group in grouped:
        l_semana = []
        l_def = []
        grouped2 = group.groupby("Semana")
        for semana, group2 in grouped2:
            l_semana.append(semana)
            l_def.append(sum(group2["Defunciones"]))

        fig.add_trace(go.Scatter(x=l_semana[1:-1], y=l_def[1:-1],
                        mode='lines',
                        name=year,
                        marker_color=colors[i]))

        i += 1

    fig.update_layout(
        title_text='Defunciones inscritas en Chile',
        xaxis_title='Número de semana',
        height=550)
    return fig

def grafica_region(dfs, region):
    dfs = dfs[dfs['Region']==region]
    fig = go.Figure()
    colors = ["seagreen","teal","deepskyblue","gray","red"]
    grouped = dfs.groupby("Año")
    i = 0
    for year, group in grouped:
        l_semana = []
        l_def = []
        grouped2 = group.groupby("Semana")
        for semana, group2 in grouped2:
            l_semana.append(semana)
            l_def.append(sum(group2["Defunciones"]))
        fig.add_trace(go.Scatter(x=l_semana[1:-1], y=l_def[1:-1],
                    mode='lines',
                    name=year,
                    marker_color=colors[i]))
        i += 1
    fig.update_layout(
        title_text=f'Defunciones inscritas en Región {region}', 
        xaxis_title='Número de semana',
        height=550)
    return fig

def grafico_acumulado(dfs, region):
    if region != 'Chile':
        dfs = dfs[dfs['Region']==region]
    data = dfs.groupby("Año", as_index=False).sum()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['Año'],
        y=data['Defunciones'],
        text=data['Defunciones'],
        textposition='inside',
        texttemplate='%{text:.2s}',
        orientation='v',
        marker_color='steelblue'))

    if region == 'Chile':
        title = 'Defunciones totales por año en Chile'
    else:
        title = f'Defunciones totales por año en Región {region}'

    fig.update_layout(
        title=title,
        template='ggplot2',
        xaxis_title='Año',
        height=450
    )
    return fig

def main():
    st.title("Defunciones inscritas Registro Civil")

    st.header('Datos')
    st.write('Cantidad de defunciones inscritas en el Registro Civil por número de semana.')
    df = get_data()
    show_df = st.checkbox('Mostrar datos')
    if show_df:
        st.write(df.sort_values(by="Año"))

    st.header('Nacional')
    fig = grafico_nacional(df)
    st.plotly_chart(fig, use_container_width=True)

    fig = grafico_acumulado(df, 'Chile')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.header('Regiones')
    regiones = list(set(df['Region']))
    reg = st.selectbox('Region', regiones, index=regiones.index('Metropolitana de Santiago'))
    fig = grafica_region(df, reg)
    st.plotly_chart(fig, use_container_width=True) 

    fig = grafico_acumulado(df, reg)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("Autor: [Joaquín Silva](https://github.com/joaquin-silva)")
    st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")

if __name__ == "__main__":
    main()