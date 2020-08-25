import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    url = "https://raw.githubusercontent.com/joaquin-silva/covid-19-chile/master/data/new_data_deis_2020.csv"
    data_2020_raw = pd.read_csv(url)
    data_2020_raw["fecha"] = pd.to_datetime(data_2020_raw["fecha"])
    data_2020_raw["mes"] = data_2020_raw["fecha"].dt.month
    sent_to = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}
    data_2020_raw["nombre_mes"] = data_2020_raw['mes'].map(sent_to)
    return data_2020_raw

@st.cache
def get_deaths(data_2020_raw, region, mes):
    age_groups = ['< 1','1 a 4','5 a 9','10 a 14','15 a 19','20 a 24','25 a 29','30 a 34','35 a 39','40 a 44','45 a 49','50 a 54','55 a 59','60 a 64','65 a 69','70 a 74','75 a 79','80 a 84','85 a 89','90 a 99','100 +']
    
    deaths = pd.DataFrame()
    deaths['edades'] = age_groups + ['Total']
    for causa in data_2020_raw['causa'].unique():
        deaths[causa] = [len(data_2020_raw[data_2020_raw["mes"].isin(mes)].query(f'región == "{region}" & grupo_edad == "{edades}" & causa == "{causa}"')) for edades in age_groups] + [len(data_2020_raw[data_2020_raw["mes"].isin(mes)].query(f'región == "{region}" & causa == "{causa}"'))]
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
    grouped = df.groupby(["género","grupo_edad"])
    l_genero = []
    l_edad = []
    l_def = []
    for name, group in grouped:
        l_genero.append(name[0])
        l_edad.append(name[1])
        l_def.append(group.shape[0])

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

def my_plot_2(df, op):
    df = df.sort_values(by=['causa']).reset_index(drop=True)
    flatui = ['#d62728','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
    fig = go.Figure()
    causas = list(set(df['causa']))
    for i, causa in enumerate(causas):
        aux = df[df['causa']==causa]
        aux = aux.sort_values(by=['fecha']).reset_index(drop=True)
        if op:
            y =  aux['cantidad'].rolling(7).mean()
        else:
            y = aux['cantidad']
        fig.add_trace(go.Scatter(
            x=aux['fecha'],
            y=y,
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

@st.cache
def my_groupby_2(data):
    df = data.groupby(['fecha','región','causa_detalle'], as_index=False).count()
    df = df[df.columns[:4]]
    df = df.rename(columns={'año':'cantidad'})
    df = df.sort_values(by=['fecha']).reset_index(drop=True)
    return df

@st.cache
def my_groupby_3(data):
    df = data.groupby(['fecha','causa_detalle'], as_index=False).count()
    df = df[df.columns[:3]]
    df = df.rename(columns={'año':'cantidad'})
    df = df.sort_values(by=['fecha']).reset_index(drop=True)
    return df

def my_plot_3(df):
    colors = ['#d62728','#1f77b4']
    fig = go.Figure()
    #causas = list(set(df['causa_detalle']))
    causas = ['COVID-19, virus identificado','COVID-19, virus no identificado']
    names = ['Covid-19, confirmado','Covid-19, sospechoso']
    for i, causa in enumerate(causas):
        aux = df[df['causa_detalle']==causa]
        aux = aux.sort_values(by=['fecha']).reset_index(drop=True)
        fig.add_trace(go.Bar(
            x=aux['fecha'],
            y=aux['cantidad'],
            name=names[i],
            marker_color=colors[i],
        ))

    fig.update_layout(
        title_text="Defunciones Covid-19 confirmado y sospechoso",
        barmode="stack",
        xaxis_title="Fecha",
        yaxis_title="Defunciones"
    )
    return fig

@st.cache
def my_groupby_4(df):
    data = df.groupby(['región','comuna','mes','nombre_mes'], as_index=False).count()
    data =data[data.columns[:5]]
    data = data.rename(columns={'año':'cantidad'})
    data = data.sort_values(by=['mes']).reset_index(drop=True)
    return data

def my_plot_4(df):
    fig = go.Figure(data=go.Heatmap(
        z=df['cantidad'],
        x=df['nombre_mes'],
        y=df['comuna'],
        colorscale='inferno_r'
        ))

    fig.update_layout(
        title='Defunciones Covid-19 confirmado + sospechoso',
        xaxis_title="Mes",
        template='ggplot2',
        autosize=False,
        width=800,
        height=1100,
    )
    return fig

def main():
    df = get_data()
    df_covid = df[df["causa"]=='COVID-19'].reset_index(drop=True)

    st.sidebar.markdown('---')
    regiones = list(set(df['región']))
    regiones.remove('Ignorada')
    reg = st.sidebar.selectbox('Elegir Región', regiones, key=0, index=regiones.index('Metropolitana de Santiago'))
    df_reg = df[df['región']==reg]

    st.title('Defunciones Covid-19 por fecha')

    st.header('Gráfico Nacional')
    group = my_groupby_3(df_covid)
    fig = my_plot_3(group)
    st.plotly_chart(fig, use_container_width=True)

    st.header(f'Gráfico Región {reg}')
    group = my_groupby_2(df_covid)
    df_reg_covid = group[group['región']==reg]

    fig = my_plot_3(df_reg_covid)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('---')
    st.title('Porcentaje de defunciones por causa básica de muerte')

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

    op = st.checkbox("Suavizar datos (Promedio móvil 7 días)", value=True)
    fig = my_plot_2(df_reg, op)
    st.plotly_chart(fig, use_container_width=True)

    if st.checkbox("Mostrar datos", value=False, key=1): 
        st.write(df_reg)  

    st.markdown('---')
    st.title(f'Defunciones Región {reg} por comuna')

    df_reg_covid = df_covid[df_covid['región']==reg]
    group = my_groupby_4(df_reg_covid)
    fig = my_plot_4(group)
    st.plotly_chart(fig, use_container_width=True)