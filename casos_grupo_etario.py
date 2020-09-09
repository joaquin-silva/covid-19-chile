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

def my_plot(df, start, end):
    df = df[(df['Fecha'] >= str(start)) & (df['Fecha'] <= str(end))]

    fig = go.Figure(data=go.Heatmap(
        z=df['Casos nuevos'],
        x=df['Fecha'],
        y=df['Grupo de edad'],
        colorscale='inferno_r',
        ))

    fig.update_layout(
        title='Casos nuevos por grupo etario',
        xaxis_title="Fecha informe",
        template='ggplot2',
        autosize=False,
    )
    return fig

def main():
    st.title('Casos confirmados por grupo etario')
    st.markdown('''
    - Datos correspondientes a los casos nuevos por grupo etario informados en cada informe epidemiológico.  
    - Fuente: Ministerio de Ciencia - [Producto 16](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto16).
    ''')

    df = get_data()
    st.sidebar.markdown('---')
    start = st.sidebar.date_input('Fecha de inicio', value=df['Fecha'].loc[0])
    end = st.sidebar.date_input('Fecha de término', value=df['Fecha'].loc[df.shape[0]-1])

    if start > end:
        st.sidebar.error('Error: La fecha de término debe ser después de la fecha de inicio.')

    else:
        fig = my_plot(df, start, end)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()