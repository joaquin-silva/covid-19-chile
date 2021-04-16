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
        height=550
        )
    return fig

@st.cache
def get_data_uci():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto9/HospitalizadosUCIEtario_std.csv')
    return df.pivot('fecha', 'Grupo de edad', 'Casos confirmados')

def my_plot_uci(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['<=39'], name='<=39', marker_color='green'))
    fig.add_trace(go.Scatter(x=df.index, y=df['40-49'], name='40-49', marker_color='royalblue'))
    fig.add_trace(go.Scatter(x=df.index, y=df['50-59'], name='50-59', marker_color='slategray'))
    fig.add_trace(go.Scatter(x=df.index, y=df['60-69'], name='60-69', marker_color='darkcyan'))
    fig.add_trace(go.Scatter(x=df.index, y=df['>=70'], name='>=70', marker_color='orange'))
    fig.update_layout(
        title="Pacientes UCI por edad",
        xaxis_title="Fecha",
        template='ggplot2',
        height=550
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
    st.title('Pacientes UCI por edad')
    df = get_data_uci()
    fig = my_plot_uci(df)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("Autor: [Joaquín Silva](https://github.com/joaquin-silva)")
    st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")

if __name__ == "__main__":
    main()