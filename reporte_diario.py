import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def data_positividad():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto49/Positividad_Diaria_Media_T.csv')
    df['Fecha'] = [datetime.datetime.strptime(f, '%Y-%m-%d') for f in df['Fecha']]
    df['positividad'] = 100*df['positividad']
    df['mediamovil_positividad'] = 100*df['mediamovil_positividad']
    return df

@st.cache
def data_ventiladores():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto20/NumeroVentiladores_T.csv')
    df = df.rename(columns={'Ventiladores':'Fecha'})
    df['Fecha'] = [datetime.datetime.strptime(f, '%Y-%m-%d') for f in df['Fecha']]
    return df
 
@st.cache
def data_criticos():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto23/PacientesCriticos_std.csv')
    df = df.rename(columns={'fecha':'Fecha','Casos confirmados':'criticos'})
    df['Fecha'] = [datetime.datetime.strptime(f, '%Y-%m-%d') for f in df['Fecha']]
    df = df[['Fecha','criticos']]
    return df

@st.cache
def data_nacionales():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales_T.csv')
    df['nuevos fallecidos'] = [df['Fallecidos'][i] - df['Fallecidos'][i-1] if df['Fallecidos'][i] > 0 else 0 for i in range(df.shape[0])]
    df['Fecha'] = [datetime.datetime.strptime(f, '%Y-%m-%d') for f in df['Fecha']]
    return df

def my_plot(df, col, referencia, tipo):
    df = df.tail(40).reset_index(drop=True)

    if referencia == 'Día anterior':
        ref = df[col][df.shape[0]-2]
    elif referencia == '7 días atrás':
        ref = df[col][df.shape[0]-8]
    elif referencia == '14 días atrás':
        ref = df[col][df.shape[0]-15]
    elif referencia == '21 días atrás':
        ref = df[col][df.shape[0]-22]

    if tipo == 'Diferencia':
        delta = {"reference": ref}
    elif tipo == 'Porcentaje':
        delta = {"reference": ref, "relative": True}

    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = df[col][df.shape[0]-1],
        delta = delta,
        title = {"text": col}
        ))

    fig.add_trace(go.Scatter(
        x=df['Fecha reporte'],
        y=df[col],
        marker_color='cadetblue'
        ))

    fig.update_layout(
        template='ggplot2',
    )

    return fig

def my_join():
    df_pos = data_positividad()
    df_vent = data_ventiladores()
    df_criticos = data_criticos()
    df_nac = data_nacionales()
    df_nac = df_nac[['Fecha','nuevos fallecidos','Casos totales','Fallecidos','Casos nuevos con sintomas','Casos nuevos sin sintomas','Casos activos']]

    df = df_pos.join(df_vent.set_index('Fecha'), on='Fecha')
    df = df.join(df_criticos.set_index('Fecha'), on='Fecha')
    df = df.join(df_nac.set_index('Fecha'), on='Fecha')
    df.columns = [
        'Fecha reporte',
        'Test informados',
        'Casos nuevos',
        'Positividad',
        'Media móvil positividad',
        'Ventiladores totales',    
        'Ventiladores disponibles',
        'Ventiladores ocupados',
        'Pacientes críticos',
        'Nuevos fallecidos',
        'Casos totales',
        'Fallecidos totales',
        'Casos nuevos con síntomas',
        'Casos nuevos sin síntomas',
        'Casos activos'
        ]

    df['Media móvil casos nuevos'] = df['Casos nuevos'].rolling(7).mean()
    df['Media móvil nuevos fallecidos'] = df['Nuevos fallecidos'].rolling(7).mean()
    
    df = df[[
        'Fecha reporte',
        'Casos nuevos',
        'Casos nuevos con síntomas',
        'Casos nuevos sin síntomas',
        'Media móvil casos nuevos',
        'Casos totales',
        'Nuevos fallecidos',
        'Media móvil nuevos fallecidos',
        'Fallecidos totales',
        'Positividad',
        'Media móvil positividad',
        'Test informados',
        'Casos activos',
        'Pacientes críticos',
        'Ventiladores totales',    
        'Ventiladores disponibles',
        'Ventiladores ocupados'   
    ]]
    
    return df

def my_plot_2(df, col):
    media_movil = df[col].rolling(7).mean()

    fig = go.Figure(go.Scatter(
        x=df['Fecha reporte'],
        y=df[col],
        marker_color='cadetblue',
        name=col
    ))

    fig.add_trace(go.Scatter(
        x=df['Fecha reporte'],
        y=media_movil,
        marker_color='red',
        name='Media móvil 7 días'
    ))

    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title=col,
        template='ggplot2',
        legend=dict(
            orientation="h",
            x=1,
            xanchor="right",
            y=1.02,
            yanchor="bottom",
            font=dict(size=12),
        )
    )

    return fig

@st.cache
def get_data_reg():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/TotalesPorRegion_std.csv')
    df = df.query('Categoria == "Casos nuevos totales" and Region != "Total"').reset_index(drop=True)
    return df

def my_plot_reg(df):
    df = df[df['Fecha'] == max(df['Fecha'])]
    df = df.sort_values('Total', ascending=False).reset_index(drop=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df['Region'][::-1],
        x=df['Total'][::-1],
        text=df['Total'][::-1],
        textposition='inside',
        orientation='h',
        marker_color='steelblue'))

    fig.update_layout(
        title='Casos nuevos totales por región',
        xaxis_title='Casos nuevos',
        template='ggplot2',
        height=800
    )

    return fig

def main():
    df = my_join()    

    st.title('Reporte Diario Nacional')
    d, m, y = str(df['Fecha reporte'][df.shape[0]-1]).split()[0].split('-')[::-1]
    fecha = f'{d}-{m}-{y}'
    st.markdown(f"**Última actualización: {fecha}**")

    st.sidebar.markdown('---')
    referencia = st.sidebar.selectbox('Referencia del indicador', ['Día anterior','7 días atrás','14 días atrás','21 días atrás'])
    tipo = st.sidebar.selectbox('Tipo de referencia', ['Diferencia','Porcentaje'])

    op = st.checkbox("Ver media móvil 7 días", value=False)

    if op:
        columns = ['Media móvil casos nuevos','Media móvil nuevos fallecidos','Media móvil positividad']
    else:
        columns = ['Casos nuevos','Nuevos fallecidos','Positividad']

    for col in columns:

        fig = my_plot(df, col, referencia, tipo)
        st.plotly_chart(fig, use_container_width=True)

    df_reg = get_data_reg()
    fig = my_plot_reg(df_reg)
    st.plotly_chart(fig, use_container_width=True)

    st.header('Más indicadores')

    cols = list(df.columns[1:])
    for col in columns:
        cols.remove(col)

    ind =  st.selectbox('Indicador', cols)
    fig = my_plot(df, ind, referencia, tipo)
    st.plotly_chart(fig, use_container_width=True)

    st.header('Gráfico')
    cols = list(df.columns[1:])
    for c in cols:
        if c.split()[0] == 'Media':
            cols.remove(c)

    col = st.selectbox('Columna', cols)
    fig = my_plot_2(df, col)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("Autor: [Joaquín Silva](https://github.com/joaquin-silva)")
    st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")

if __name__ == "__main__":
    main()