import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto16/CasosGeneroEtario_std.csv')
    #df['Semana'] = [datetime.datetime.strptime(df["Fecha"][i], '%Y-%m-%d').date().isocalendar()[1] for i in range(df.shape[0])]
    data = df.groupby(['Fecha','Grupo de edad'], as_index=False).sum()
    data = data.sort_values(['Fecha','Grupo de edad'], ascending=True).reset_index(drop=True)
    data['Fecha'] = [datetime.datetime.strptime(f, '%Y-%m-%d') for f in data['Fecha']]
    nuevos = []
    for i in range(data.shape[0]):
        if i < 17:
            nuevos.append('')
        else:
            nuevos.append(data['Casos confirmados'][i] - data['Casos confirmados'][i-17])
    data['Casos nuevos'] = nuevos
    return data

def my_plot(df, start, end, col):
    df = df[(df['Fecha'] >= str(start)) & (df['Fecha'] <= str(end))]

    fig = go.Figure(data=go.Heatmap(
        z=df[col],
        x=df['Fecha'],
        y=df['Grupo de edad'],
        colorscale='inferno_r',
        ))

    fig.update_layout(
        title=f'{col} por grupo etario',
        xaxis_title="Fecha informe",
        template='ggplot2',
        autosize=False,
    )
    return fig

def get_column_ine(df):
    data = pd.read_csv('https://raw.githubusercontent.com/joaquin-silva/covid-19-chile/master/data/datos_ine_proyecciones.csv',sep=';')
    data = data[['Edad','2020']]
    data['2020'] = [int(1000*x) for x in data['2020']]
    data['Edad'][100] = 100
    l_grupo = []
    for i in range(data.shape[0]):
        e = int(data['Edad'][i])
        if e <= 4:
            grupo = '00 - 04 años'
        elif e <= 9:
            grupo = '05 - 09 años'
        elif e <= 14:
            grupo = '10 - 14 años'
        elif e <= 19:
            grupo = '15 - 19 años'
        elif e <= 24:
            grupo = '20 - 24 años'
        elif e <= 29:
            grupo = '25 - 29 años'
        elif e <= 34:
            grupo = '30 - 34 años'
        elif e <= 39:
            grupo = '35 - 39 años'
        elif e <= 44:
            grupo = '40 - 44 años'
        elif e <= 49:
            grupo = '45 - 49 años'
        elif e <= 54:
            grupo = '50 - 54 años'
        elif e <= 59:
            grupo = '55 - 59 años'
        elif e <= 64:
            grupo = '60 - 64 años'
        elif e <= 69:
            grupo = '65 - 69 años'
        elif e <= 74:
            grupo = '70 - 74 años'
        elif e <= 79:
            grupo = '75 - 79 años'
        elif e <= 84:
            grupo = '80 y más años'
        l_grupo.append(grupo)

    data['Grupo'] = l_grupo   
    grouped = data.groupby('Grupo', as_index=False).sum()

    sent = {}
    for i in range(grouped.shape[0]):
        sent[grouped['Grupo'][i]] = int(grouped['2020'][i])
    
    df['Poblacion 2020'] = df['Grupo de edad'].map(sent)
    incidencia = []
    for i in range(df.shape[0]):
        if i < 17:
            incidencia.append('')
        else:
            incidencia.append(df['Casos nuevos'][i]/df['Poblacion 2020'][i])

    df['Incidencia'] = incidencia
    return df

def main():
    st.title('Casos confirmados por grupo etario')
    st.markdown('''
    - Datos correspondientes a los casos nuevos por grupo etario informados en cada informe epidemiológico.  
    - Fuente: Ministerio de Ciencia - [Producto 16](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto16).
    ''')

    df = get_data()
    st.sidebar.markdown('---')
    start = st.sidebar.date_input('Fecha de inicio', value=df['Fecha'].loc[17])
    end = st.sidebar.date_input('Fecha de término', value=df['Fecha'].loc[df.shape[0]-1])
    
    if start > end:
        st.sidebar.error('Error: La fecha de término debe ser después de la fecha de inicio.')

    else:
        fig = my_plot(df, start, end, 'Casos nuevos')
        st.plotly_chart(fig, use_container_width=True)

        st.header('Incidencia por grupo etario')
        df = get_column_ine(df) 

        fig = my_plot(df, start, end, 'Incidencia')
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()