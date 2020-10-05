import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache   
def get_data():
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    df = pd.read_csv(url)
    df = df.rename(columns={
        'continent':'Continente',
        'location':'País',
        'date':'Fecha',
        'total_cases':'Casos totales',
        'new_cases':'Casos nuevos',
        'total_deaths':'Fallecidos totales',
        'new_deaths':'Fallecidos nuevos',
        'new_tests':'Test nuevos',
        'total_tests':'Test totales',
        'positive_rate':'Positividad',
        'total_cases_per_million':'Casos totales por millón',
        'new_cases_per_million':'Casos nuevos por millón',
        'total_deaths_per_million':'Fallecidos totales por millón',
        'new_deaths_per_million':'Fallecidos nuevos por millón'})
    return df

def my_plot_1(df, paises, col, op):
    fig = go.Figure()
    for i, pais in enumerate(paises):
        aux = df[df['País']==pais]
        aux = aux.sort_values(by=['Fecha']).reset_index(drop=True)

        if op:
            y = aux[col].rolling(7).mean()
        else:
            y = aux[col]

        fig.add_trace(go.Scatter(
            x=aux['Fecha'],
            y=y,
            name=pais,
            marker_color=px.colors.qualitative.G10[i],
        ))

    if op:
        col = col + ' (Promedio móvil 7 días)'

    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title=col,
        legend=dict(
            orientation="h",
            x=1,
            xanchor="right",
            y=1.02,
            yanchor="bottom",
            font=dict(size=12),
        ),
        height=550,
        template='ggplot2'
    )
    return fig

def my_plot_2(df, col):
    df = df[df['País']!='World']
    df = df[df['Fecha']==max(df['Fecha'])].reset_index(drop=True)
    df = df.sort_values(col, ascending=False).reset_index(drop=True)
    df = df[:20]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df['País'][::-1],
        x=df[col][::-1],
        text=df[col][::-1],
        textposition='inside',
        orientation='h',
        marker_color='steelblue'))

    fig.update_layout(
        title=f'{col} por país',
        xaxis_title=col,
        template='ggplot2',
        height=750
    )

    return fig


def main():
    st.title('Vista Mundial')

    st.markdown('Datos provistos por [Our World in Data](https://github.com/owid/covid-19-data/tree/master/public/data).')
    st.header('Evolución por países')

    df = get_data()
    #st.write(df)

    paises = list(set(df['País']))
    pais_select = st.multiselect('Seleccionar países', paises, ['Chile','Argentina','Peru'])

    columns = [
        'Casos nuevos',
        'Casos nuevos por millón',
        'Casos totales',
        'Casos totales por millón'
        'Fallecidos nuevos',
        'Fallecidos nuevos por millón',
        'Fallecidos totales',
        'Fallecidos totales por millón',
        'Test nuevos',
        'Test totales',
        'Positividad']

    col_select = st.selectbox("Elegir columna", columns, key=0)

    op = st.checkbox("Suavizar datos (Promedio móvil 7 días)", value=True, key=0)

    try:
        fig = my_plot_1(df, pais_select, col_select, op)
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.write('Demasiados países seleccionados')

    st.markdown('---')
    st.header('Países más afectados')
    fecha = max(df['Fecha'])
    d, m, y = str(fecha).split()[0].split('-')[::-1]
    fecha = f'{d}-{m}-{y}'
    st.markdown(f"**Datos actualizados a la fecha: {fecha}**")

    columns = [
        'Casos totales',
        'Casos totales por millón',
        'Casos nuevos',
        'Casos nuevos por millón',
        'Fallecidos totales',
        'Fallecidos totales por millón',
        'Fallecidos nuevos',
        'Fallecidos nuevos por millón',
        ]
    col_select = st.selectbox("Elegir columna", columns, key=1)

    fig = my_plot_2(df, col_select)
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()