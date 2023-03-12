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



st.set_page_config(page_title="Panel General", page_icon=":📈", layout="wide")

st.title(":mag_right: Proyecto MARKETING - Visualización de Datos Generales")
st.text("A continuación se observara los resultados del análisis")
st.markdown("---")

st.sidebar.header("Panel General")
st.sidebar.write(
    """El panel general contiene información sobre el comportamiento general del dataset, 
. """
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