import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    data_2020_raw = pd.read_csv("https://raw.githubusercontent.com/alonsosilvaallende/COVID-19/master/data/DEFUNCIONES_FUENTE_DEIS_SOLO_A%C3%91O_2020_2020-08-06.csv")
    data_2020_raw["fecha"] = pd.to_datetime(data_2020_raw["fecha"])
    data_2020_raw["mes"] = data_2020_raw["fecha"].dt.month
    return data_2020_raw

def get_deaths(data_2020_raw, region, mes):
    age_groups = ['< 1','1 a 4','5 a 9','10 a 14','15 a 19','20 a 24','25 a 29','30 a 34','35 a 39','40 a 44','45 a 49','50 a 54','55 a 59','60 a 64','65 a 69','70 a 74','75 a 79','80 a 84','85 a 89','90 a 99','100 +']
    
    deaths = pd.DataFrame()
    deaths['edades'] = age_groups + ['Total']
    for causa in data_2020_raw['causa'].unique():
        deaths[causa] = [len(data_2020_raw[data_2020_raw["mes"].isin([mes])].query(f"región == '{region}' & edad == '{edades}' & causa == '{causa}'")) for edades in age_groups] + [len(data_2020_raw[data_2020_raw["mes"].isin([mes])].query(f"región == '{region}' & causa == '{causa}'"))]
    deaths = deaths.set_index('edades')

    deaths_percentage = deaths.apply(lambda x: 100*x/deaths.sum(axis=1))
    lista = list(deaths_percentage.loc["Total"].sort_values(ascending=False).index)
    deaths_percentage = deaths_percentage[lista]

    # Acortar nombres demasiado largos
    deaths_percentage.columns = [causa[:37] for causa in deaths_percentage.columns]
    return deaths, deaths_percentage

def my_plot(df, region, mes):
    df = df.drop(['Total'])
    flatui = ['#d62728','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
    fig = go.Figure()
    for i, col in enumerate(df.columns):
        fig.add_trace(go.Bar(
            y=df.index,
            x=df[col],
            name=str(col),
            orientation='h',
            marker_color=flatui[i]
        ))

    fig.update_layout(
        barmode='stack',
        title_text=f'Porcentaje de defunciones en región {region} en {mes} del 2020',
        xaxis_title='Porcentaje',
        yaxis_title='Grupo etario'
    )
    return fig

def main():
    st.title('Porcentaje de defunciones por causa básica de muerte')

    df = get_data()
	#if st.checkbox("Mostrar datos", value=False): 
    #    st.write(df)

    regiones = list(set(df['región']))
    regiones.remove('Ignorada')
    reg = st.selectbox('Región', regiones)
    df_reg = df[df['región']==reg]

    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto']
    mes = st.selectbox('Mes', meses)
    num_mes = int(meses.index(mes)) + 1
    deaths, deaths_percentage = get_deaths(df_reg, reg, num_mes)

    fig = my_plot(deaths_percentage, reg, mes)
    st.plotly_chart(fig, use_container_width=True) 

    st.markdown('---')
