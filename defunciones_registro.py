import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto32/Defunciones_T.csv')
    reg = list(df.columns)
    dicc = {}
    for i,r in enumerate(reg):
        if i == 0:
            dicc[r] = 'Fecha'
        else:
            dicc[r] = df[r][1]

    df = df.rename(dicc, axis='columns')
    df = df.drop([0,1,2])
    df = df.reset_index(drop=True)
    df["Año"] = [df["Fecha"][i].split("-")[0] for i in range(df.shape[0])]
    df["Mes"] = [df["Fecha"][i].split("-")[1] for i in range(df.shape[0])]
    df["Dia"] = [df["Fecha"][i].split("-")[2] for i in range(df.shape[0])]

    dicc_regiones = {}
    for n, k in dicc.items():
        reg = n.split('.')[0]
        dicc_regiones[reg] = []

    for n, k in dicc.items():
        reg = n.split('.')[0]
        dicc_regiones[reg].append(k)

    dicc_regiones.pop("Region")

    df = df[[int(df['Año'][i])>=2016 for i in range(df.shape[0])]].reset_index(drop=True)
    l_semana = [datetime.datetime.strptime(df["Fecha"][i], '%Y-%m-%d').date().isocalendar()[1] for i in range(df.shape[0])]
    df['Semana'] = l_semana

    l_year = []
    l_semana = []
    l_region = []
    l_comuna = []
    l_def = []
    #dfs = pd.DataFrame(columns=["Año","Semana","Region","Comuna","Defunciones"])
    grouped = df.groupby(["Año","Semana"])
    for name, group in grouped: 
        for reg, comunas in dicc_regiones.items():
            for comuna in comunas:
                #dfs.loc[dfs.shape[0]] = [name[0],name[1],reg,comuna,sum(group[comuna])]
                l_year.append(name[0])
                l_semana.append(name[1])
                l_region.append(reg)
                l_comuna.append(comuna)
                l_def.append(np.sum(group[comuna]))

    dfs = pd.DataFrame()
    dfs["Año"] = l_year
    dfs["Semana"] = l_semana
    dfs["Region"] = l_region
    dfs["Comuna"] = l_comuna
    dfs["Defunciones"] = l_def

    return dfs

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

    fig.update_layout(title_text='Defunciones inscritas en Chile',  xaxis_title='Número de semana')
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
    fig.update_layout(title_text=f'Defunciones inscritas en Región {region}',  xaxis_title='Número de semana')
    return fig

def main():
    st.title("Defunciones inscritas Registro Civil")

    st.header('Datos')
    st.write('Cantidad de defunciones inscritas en el Registro Civil por número de semana.')
    df = get_data()
    st.write(df)

    st.header('Gráfico Nacional')
    fig = grafico_nacional(df)
    st.plotly_chart(fig, use_container_width=True)

    st.header('Gráfico por regiones')
    reg = st.selectbox('Region', list(set(df['Region'])))
    fig = grafica_region(df, reg)
    st.plotly_chart(fig, use_container_width=True) 

    st.markdown("Autor: [Joaquín Silva](https://github.com/joaquin-silva)")
    st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")