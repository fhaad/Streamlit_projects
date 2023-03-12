import sqlalchemy as sql
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import pydeck as pdk
import pymysql
import datetime
from PIL import Image
import altair as alt

st.set_page_config(page_title="Panel General", page_icon=":📈", layout="wide")

st.title(":mag_right: Proyecto - Visualización de Datos Generales")
st.text("A continuación se observara los resultados del análisis")
st.markdown("---")

st.sidebar.header("Panel General")
st.sidebar.write(
    """El panel general contiene información sobre la evolución del proyecto. Utilizaremos un dataset propio de plotly
 """
)
# Conexion al DATAWAREHOUSE de los datos
engine = sql.create_engine(
    "mysql+pymysql://root:password@localhost:3307/data_warehouse_olist?charset=utf8mb4"  #esta es la conexion al contenedor de docker
)

engine1 = sql.create_engine(
    "mysql+pymysql://root:password@localhost:3307/data_warehouse_olist?charset=utf8mb4"  #esta es la conexion local con streamlit
)

engine2 = sql.create_engine(
    "mysql+pymysql://root:Haad91280567#@localhost:3306/marketing?charset=utf8mb4"     #esta es la conexion local con my workbench mysql
) 


#------------------------------------------------------------------------------------------#
df = px.data.gapminder()  #Dataset origen from plotly

tab_1, tab_2 = st.tabs(["Grafico GDP PerCapita", "New Cases Covid19"])

with tab_1:

    year_options = df['year'].unique().tolist()
    year = st.sidebar.selectbox("Que año desea observar", year_options, 0)
    #df = df[df['year']==year]

    fig = px.scatter(df, x="gdpPercap", y="lifeExp",
            size="pop", color="continent", hover_name="continent",
            log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90],
            animation_frame="year", animation_group="country" 
    )

    fig.update_layout(width=800)

    st.write(fig)

with tab_2:
    covid = pd.read_csv("https://raw.githubusercontent.com/shinokada/covid-19-stats/master/data/daily-new-confirmed-cases-of-covid-19-tests-per-case.csv")
    covid.columns = ['Country', 'Code', 'Date', 'Confirmed','Days since confirmed']
    covid['Date'] = pd.to_datetime(covid['Date']).dt.strftime('%Y-%m-%d')

    #st.write(covid)

    country_options = covid['Country'].unique().tolist()
    date_options = covid['Date'].unique().tolist()

    date = st.sidebar.selectbox("Fecha que desea observar?", date_options, 100)
    country = st.sidebar.multiselect("País que desea ver?", country_options, ['Brazil'])

    covid = covid[covid['Country'].isin(country)]
    #covid = covid[covid['Date']==fecha]

    fig2 = px.bar(covid, x="Country", y="Confirmed", color="Country", range_y=[0,35000],
                animation_frame="Date", animation_group="Country")

    fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
    fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5

    fig2.update_layout(width=900)

    st.write(fig2)











