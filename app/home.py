#----LIBRERIAS--------------------------------------------------------------------------------------#
import sqlalchemy as sql
import pandas as pd
import numpy as np
import streamlit as st
import datetime
from PIL import Image
import altair as alt
import pymysql
import time
#------------------------------------------------------------------------------------------#

st.set_page_config(page_title="Plus+BI - Data Insights", page_icon='🏠', layout="wide")
#------------------------------------------------------------------------------------------#
icons = ["🏠","📈","📊","💵","📦"]
#------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
# Logo
image = Image.open('D:/Streamlit_projects/src/PlusBi_logo.png')
st.image(image, caption='Logo', width=700)
#--------------------------------------------------------------------------------------#
st.title(":clipboard: BIENVENIDOS - PLUS BI - Dashboard") 
st.text('Sitio web para explorar la visualizacion de proyectos')
#--------------------------------------------------------------------------------------#
# Divido en 2 columnas el texto de la consultoria y objetivo general
left_column, right_column = st.columns(2)

st.markdown('***')
with left_column:
    st.markdown(f'<p style="color:#F3FF33;font-size:32px;border-radius:2%;">Consultoría</p>', unsafe_allow_html=True)
    st.markdown("""Plus+BI es el anlace entre los datos y lo que puedes hacer con ellos. Transformamos y potenciamos los datos 
                    de manera que te ayuden a tomar mejores decisiones y lograr alcanzar los objetivos de las empresas.
                    No te quedes atras y continua hacia adelante. El poder de la información esta en tus manos. 
    
    """)

with right_column:
    st.markdown(f'<p style="color:#F3FF33;font-size:32px;border-radius:2%;">Objetivo General</p>', unsafe_allow_html=True)
    st.markdown("""Plus+BI es una marca que tiene el potencial de extraer, transformar y visualizar los datos (Dashboard) 
                   para ayudar a proporcionar estrategias de mejoramiento en las pequeñas y medianas empresas.
                   Te damos información relevante para la toma de decisiones basada en inteligencia de negocios.""")

#-------------------POR EL MOMENTO NO SE VA A MOSTRAR---------------------------------#
#Video de Olist
st.header('Que es la Ciencia de Datos y que podemos hacer?')
video_file = open('D:/Streamlit_projects/video/Olist.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)

#--------------------------------------------------------------------------------------#
#DATE_COLUMN = 'date/time'
#DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#           'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#--------------------------------------------------------------------------------------#
my_bar = st.progress(0)

for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)
#---------------------------------------------------------------------------------------#
with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
st.sidebar.header("PLUS+BI")
st.sidebar.write(
    """Utilizamos Power BI y Streamlit para dar visualizacion a los datos.
        Da un paso adelante para sacar el mejor provecho de la información."""
)
#--------------------------------------------------------------------------------------#