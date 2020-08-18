import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    #url = "https://raw.githubusercontent.com/alonsosilvaallende/COVID-19/master/data/DEFUNCIONES_FUENTE_DEIS_SOLO_A%C3%91O_2020_2020-08-06.csv"
    url = "https://raw.githubusercontent.com/joaquin-silva/covid-19-chile/master/data/data_deis_2020.csv"
    data_2020_raw = pd.read_csv(url)
    data_2020_raw["fecha"] = pd.to_datetime(data_2020_raw["fecha"])
    data_2020_raw["mes"] = data_2020_raw["fecha"].dt.month
    return data_2020_raw

@st.cache
def get_deaths(data_2020_raw, region, mes):
    age_groups = ['< 1','1 a 4','5 a 9','10 a 14','15 a 19','20 a 24','25 a 29','30 a 34','35 a 39','40 a 44','45 a 49','50 a 54','55 a 59','60 a 64','65 a 69','70 a 74','75 a 79','80 a 84','85 a 89','90 a 99','100 +']
    
    deaths = pd.DataFrame()
    deaths['edades'] = age_groups + ['Total']
    for causa in data_2020_raw['causa'].unique():
        deaths[causa] = [len(data_2020_raw[data_2020_raw["mes"].isin(mes)].query(f'región == "{region}" & edad == "{edades}" & causa == "{causa}"')) for edades in age_groups] + [len(data_2020_raw[data_2020_raw["mes"].isin(mes)].query(f'región == "{region}" & causa == "{causa}"'))]
    deaths = deaths.set_index('edades')

    deaths_percentage = deaths.apply(lambda x: 100*x/deaths.sum(axis=1))
    lista = list(deaths_percentage.loc["Total"].sort_values(ascending=False).index)
    deaths_percentage = deaths_percentage[lista]

    # Acortar nombres demasiado largos
    deaths_percentage.columns = [causa[:37] for causa in deaths_percentage.columns]
    return deaths, deaths_percentage

@st.cache
def my_plot(df, region):
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
        title_text=f'Porcentaje de defunciones en región {region}',
        xaxis_title='Porcentaje',
        yaxis_title='Grupo etario'
    )
    return fig

def deaths_genre_plot(df):
    df = df[df['causa']=='COVID-19']
    grouped = df.groupby(["género","edad"])
    l_genero = []
    l_edad = []
    l_def = []
    for name, group in grouped:
        l_genero.append(name[0])
        l_edad.append(name[1])
        l_def.append(group.shape[0])

    if len(l_genero) < 42:
        l_genero.append("Hombre")
        l_edad.append("5 a 9")
        l_def.append(0)

    data_deis_grouped = pd.DataFrame({"genero":l_genero,"edad":l_edad,"fallecidos":l_def})

    sent_to_id = {"< 1":0,"1 a 4":1,"5 a 9":2,"10 a 14":3,"15 a 19":4,"20 a 24":5,"25 a 29":6,"30 a 34":7,"35 a 39":8,
                "40 a 44":9,"45 a 49":10,"50 a 54":11,"55 a 59":12,"60 a 64":13,"65 a 69":14,"70 a 74":15,"75 a 79":16,
                "80 a 84":17,"85 a 89":18,"90 a 99":19,"100 +":20}
    data_deis_grouped["edad_id"] = data_deis_grouped["edad"].map(sent_to_id)
    data_deis_grouped = data_deis_grouped.sort_values(by=["edad_id"])

    fig = go.Figure()
    colors = ['lightskyblue','steelblue']
    for i, genero in enumerate(["Mujer","Hombre"]):
        data_aux = data_deis_grouped[data_deis_grouped["genero"]==genero]
        fig.add_trace(go.Bar(x=data_aux["edad"], y=data_aux["fallecidos"], name=genero, marker_color=colors[i]))

    fig.update_layout(
        barmode='group',
        title_text="Defunciones COVID-19 confirmado + sospechoso",
        xaxis_title="Grupo etario",
        yaxis_title="Cantidad de fallecidos"
    )
    return fig

@st.cache
def my_groupby(data):
    df = data.groupby(['fecha','región','causa'], as_index=False).count()
    df = df[df.columns[:4]]
    df = df.rename(columns={'año':'cantidad'})
    df = df.sort_values(by=['fecha','causa']).reset_index(drop=True)
    df['causa'] = [causa[:37] for causa in df['causa']]
    return df

def my_plot_2(df):
    df = df.sort_values(by=['causa']).reset_index(drop=True)
    flatui = ['#d62728','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
    fig = go.Figure()
    causas = list(set(df['causa']))[::-1]
    for i, causa in enumerate(causas):
        aux = df[df['causa']==causa]
        aux = aux.sort_values(by=['fecha']).reset_index(drop=True)
        aux['media movil'] =  aux['cantidad'].rolling(7).mean()
        fig.add_trace(go.Scatter(
            x=aux['fecha'],
            y=aux['media movil'],
            name=str(causa),
            mode='lines',
            marker_color=flatui[i],
        ))
        fig.update_layout(
        title_text="Defunciones por causa básica",
        xaxis_title="Fecha",
        yaxis_title="Defunciones"
        )

    return fig

def main():
    st.title('Porcentaje de defunciones por causa básica de muerte')

    df = get_data()

    st.sidebar.markdown('---')
    regiones = list(set(df['región']))
    regiones.remove('Ignorada')
    reg = st.sidebar.selectbox('Elegir Región', regiones, key=0)
    df_reg = df[df['región']==reg]

    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto']
    mes = st.multiselect('Elegir meses', meses, ['Junio','Julio'])
    num_mes = [int(meses.index(m)) + 1 for m in mes] 

    try:
        deaths, deaths_percentage = get_deaths(df_reg, reg, num_mes)
        fig = my_plot(deaths_percentage, reg)
        st.plotly_chart(fig, use_container_width=True) 

        if st.checkbox("Mostrar datos", value=False, key=0): 
            st.write(deaths_percentage)  
    except:
        st.write('Se ha producido un error')

    st.markdown('---')
    st.title('Defunciones por género y grupo etario')
    st.header('Gráfico Nacional')
    fig = deaths_genre_plot(df)
    st.plotly_chart(fig, use_container_width=True)

    st.header(f'Gráfico Región {reg}')

    fig = deaths_genre_plot(df_reg)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('---')
    st.title('Defunciones por causa básica')

    st.header(f'Gráfico Región {reg}')
    group = my_groupby(df)
    df_reg = group[group['región']==reg]

    fig = my_plot_2(df_reg)
    st.plotly_chart(fig, use_container_width=True)

    if st.checkbox("Mostrar datos", value=False, key=1): 
        st.write(df_reg)  