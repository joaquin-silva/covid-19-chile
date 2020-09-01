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

def report_data(df):
    data = pd.DataFrame(columns=['Fecha reporte','Casos nuevos','Nuevos fallecidos','Positividad','Test informados','Ventiladores disponibles','Ventiladores ocupados','Pacientes críticos'])
    index = df.shape[0] - 1
    for i in range(4):
        data.loc[i] = [df[col][index] for col in list(data.columns)]
        index -= 7
    
    data.index=['Último reporte','Reporte hace 7 días','Reporte hace 14 días','Reporte hace 21 días']
    return data

def report(df):
    df = df[['Fecha reporte','Casos nuevos','Nuevos fallecidos','Positividad','Test informados','Ventiladores disponibles','Ventiladores ocupados','Pacientes críticos']]
    df = df.tail(8)
    df = df.iloc[::-1].reset_index(drop=True)
    return df

def write_text(data):
    columns = ['Casos nuevos','Nuevos fallecidos','Test informados','Ventiladores ocupados','Pacientes críticos']
    names = ['casos','fallecidos','test','ventiladores ocupados','pacientes críticos']
    for i in range(len(columns)):
        dif = data[columns[i]][1] - data[columns[i]][0]
        p = 100*(1-data[columns[i]][0]/data[columns[i]][1])
        if dif > 0:
            txt = f'- En el último reporte se informaron {int(dif)} {names[i]} menos (-{round(p,1)}%) que hace una semana.'
        elif dif < 0:
            txt = f'- En el último reporte se informaron {-int(dif)} {names[i]} más (+{round(-p,1)}%) que hace una semana.'
        elif dif == 0:
            txt = '- En el último reporse se informaron la misma cantidad de casos que hace una semana.'
        st.markdown(txt)

def my_plot(df, col, referencia, tipo):
    df = df.tail(40).reset_index(drop=True)

    if referencia == 'Día anterior':
        ref = df[col][df.shape[0]-2]
    elif referencia == '7 días atrás':
        ref = df[col][df.shape[0]-8]
    elif referencia == '14 días atrás':
        ref = df[col][df.shape[0]-15]


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
    df_nac = df_nac[['Fecha','nuevos fallecidos','Casos totales','Fallecidos']]

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
        'Fallecidos totales'
        ]

    df['Media móvil casos nuevos'] = df['Casos nuevos'].rolling(7).mean()
    df['Media móvil nuevos fallecidos'] = df['Nuevos fallecidos'].rolling(7).mean()
    '''
    df = df[[
        'Fecha reporte',
        'Casos nuevos',
        'Media móvil casos nuevos',
        'Casos totales',
        'Nuevos fallecidos',
        'Media móvil nuevos fallecidos',
        'Fallecidos totales',
        'Positividad',
        'Media móvil positividad',
        'Test informados',
        'Ventiladores totales',    
        'Ventiladores disponibles',
        'Ventiladores ocupados',
        'Pacientes críticos'
    ]]
    '''
    return df

def main():
    df = my_join()    

    st.title('Reporte Diario')

    st.sidebar.markdown('---')
    referencia = st.sidebar.selectbox('Referencia del indicador', ['Día anterior','7 días atrás','14 días atrás'])
    tipo = st.sidebar.selectbox('Tipo de referencia', ['Diferencia','Porcentaje'])

    columns = ['Casos nuevos','Nuevos fallecidos','Positividad']

    for col in columns:

        fig = my_plot(df, col, referencia, tipo)
        st.plotly_chart(fig, use_container_width=True)


    st.header('Más indicadores')

    col = list(set(list(df.columns[1:])).difference(set(columns)))

    ind =  st.selectbox('Indicador', col)
    fig = my_plot(df, ind, referencia, tipo)
    st.plotly_chart(fig, use_container_width=True)

    st.header('Últimos reportes')
    data = report(df)
    st.table(data)

    st.header('Reportes por semana')
    data = report_data(df)
    st.table(data)

if __name__ == "__main__":
    main()