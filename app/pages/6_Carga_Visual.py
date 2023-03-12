import sqlalchemy as sql
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import pydeck as pdk
import pymysql
from datetime import datetime
import datetime
from PIL import Image
import altair as alt
from datetime import datetime
import os
import subprocess
import time
#-------------------------------------------------------------------------------------#

st.set_page_config(page_title="Panel General", page_icon=":📈", layout="wide")
#-------------------------------------------------------------------------------------#

st.title(":mag_right: Proyecto DATA SCIENCE - Aplicación para pymes")
st.text("A continuación la aplicación permite cargar datos (.csv) para realizar visualizaciones")
st.text("Los datos ya deben haber pasado por el proceso de ETL")
st.markdown("---")
st.markdown("<h1 style='text-align: center;'>Carga de Datos</h1>", unsafe_allow_html=True)
#-------------------------------------------------------------------------------------#
# NAVEGADOR DE OPCIONES CON LA CARGA DE DATASET
st.sidebar.title('Navegador de Opciones')
uploaded_file = st.sidebar.file_uploader('Cargue su DATASET aqui(Opcional)')

options = st.sidebar.radio('Paginas', options=['Home', 'Panel General', 'Mapa'


])

my_bar = st.progress(0)

for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)
#---------------------------------------------------------------------------------------#
with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')
#---------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#DATE_COLUMN = 'date/time'
#DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#--------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
# CARGA DE DATASET A DATAFRAME

if uploaded_file:
    #dataset = pd.read_csv(uploaded_file)
    dataset = pd.read_csv(uploaded_file, sep=',', encoding='latin-1')
    #pd.read_csv('D:\Python\MODULO-3-DATA ENGINEER-1\CLASE1-DATA DESCRIPTION\Homework\Clientes.csv', sep=';', encoding='UTF-8')
#--------------------------------------------------------------------------------------#
st.header("Dataset Cargado")
#st.dataframe(dataset)

edited_df = st.experimental_data_editor(dataset, num_rows="dynamic")

favorite_command = edited_df.loc[edited_df["Puntuación"].idxmax()]["Nombres"]
st.markdown(f"El Vendedor con mayor puntuación es: **{favorite_command}** 🎈")

ciudad = st.sidebar.selectbox(
            'Seleccione ciudad 👉', dataset['Ciudad'].unique()
            )

#-------------------------------------------------------------------------------------#
# FUNCIONES PRINCIPALES
@st.cache_data
def General(dataset):
    st.header('Dataset')
    
    # En esta linea de codigo dividimos la columna (duration) en 2 tipos, una tipo numerica y otra string
    #dataset[['simbolo','Facturado_1']] = dataset['Facturado'].str.split(expand=True)
    # La columna (min) de tipo string(str) se convierte a entero(int)
    #dataset['Facturado'] = dataset['Facturado'].astype(int)
    dataciudad = (dataset.groupby(by=['Ciudad']).sum()[['Facturado']].sort_values(by='Facturado'))
    
    col_1, col_2 = st.columns(2)
    
    with col_1:
        fig_vendedores = px.bar(
        dataset,
        x = 'Facturado',
        y = 'Nombres',
        orientation="h",
        title="Facturado por Vendedores",
        #color = 'Nombres',
        color_discrete_sequence=["#33E3FF"] * len(dataset),
        template='plotly_white',
        #text_auto=True
    )
    fig_vendedores.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )

    with col_2:
        
        fig_ciudades = px.bar(
        dataciudad,
        x = dataciudad.index,
        y = 'Facturado',
        #orientation="h",
        title="Facturado por Ciudad",
        color = dataciudad.index,
        #color_discrete_sequence=["#5EFF33"] * len(dataset),
        template='plotly_white',
        hover_data = ['Facturado'],
        #labels = { 'Nombres' : 'population of Canada' }
        text_auto=True

        )
        fig_ciudades.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False),
        
        )

#-----------------------------------------------------------------------------#
        
        fig_ciudades_2 = px.bar(
        #data_frame = dataset.groupby(by=['Ciudad']).sum()[['Facturado']].sort_values(by='Facturado'),
        data_frame=dataset[dataset["Ciudad"] == ciudad],
        y = 'Facturado',
        #orientation="h",
        title="Facturado por Ciudad",
        color_discrete_sequence=["#5EFF33"] * len(dataset),
        template='plotly_white',
        hover_data = ['Ciudad', 'Facturado'],
        )
        fig_ciudades_2.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )        

        st.plotly_chart(figure_or_data=fig_ciudades_2, use_container_width=True)
#-----------------------------------------------------------------------------#
        filter_ciudad = dataset[dataset.Ciudad == ciudad]
        new_df = pd.melt(filter_ciudad, id_vars=['Ciudad'], var_name="feature", value_vars=['Facturado'])
        

        fig_ciudades_3 = px.bar(
        new_df,
        x = 'feature',
        y = 'value',
        #orientation="h",
        title="Ciudad",
        color_discrete_sequence=["#5EFF33"] * len(dataset),
        template='plotly_white',
        )
        fig_ciudades_2.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )        

        st.plotly_chart(figure_or_data=fig_ciudades_3, use_container_width=True)





#-----------------------------------------------------------------------------#
    left_column, right_column = st.columns(2)

    left_column.plotly_chart(fig_vendedores, use_container_width=True)
    right_column.plotly_chart(fig_ciudades, use_container_width=True)

#-------------------------------------------------------------------------------#
@st.cache_data
def Mapa():
    st.header('Geo Map')
    #data_ciudad = (dataset[['Latitud','Longitud']].groupby(['Ciudad']).sum()[['Facturado']].sort_values(by='Facturado'))


    data_city = pd.DataFrame({
    'ciudades' : ['Bucaramanga', 'Barrancabermeja', 'Cucuta', 'Sangil', 'Medellin'],
    'lat' : [7.1186, 7.0675,  7.9075, 6.555, 6.2447],
    'lon' : [-73.1161, -73.8472, -72.5047, -73.1336, -75.5748]
})
    #dataset['Latitud']=pd.to_numeric(dataset['Latitud']) 
    #dataset['Longitud']=pd.to_numeric(dataset['Longitud'])    
    #dataset['Longitud'] = dataset['Longitud'].astype(int)
    #dataset.rename(columns={'Latitude':'lat',  # renombra las columnas del DataFrame
    #                        'Longitud':'lon'}, 
    #                        inplace=True)
    df = pd.DataFrame(data_city, columns=['lat', 'lon'])

    st.map(df)
    
    

#-------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
# AREA DE OPCIONES PARA EJECUTAR LAS FUNCIONALIDADES y DE NAVEGACION
if options == 'Panel General':
    st.text('Podemos Observar el Dataset')
    General(dataset)
elif options == 'Mapa':
    st.text('Mapa Geográfico')
    Mapa()

#--------------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------------#




#-------------------------------------------------------------------------------------#
