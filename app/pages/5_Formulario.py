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
#----------------------------------------------------------------------------------------------#
st.set_page_config(page_title="Panel General", page_icon=":📈", layout="wide")
#----------------------------------------------------------------------------------------------#
st.title(":mag_right: Proyecto FORMULARIO - Registro de Usuarios")
st.text("A continuación se crea un formulario para el registro")
st.markdown("---")
st.markdown("<h1 style='text-align: center;'>Registro de Usuarios</h1>", unsafe_allow_html=True)
#----------------------------------------------------------------------------------------------#

tab_1, tab_2, tab_3 = st.tabs(["Formulario Registro", "Formulario Calculadora", "Otro"])
#----------------------------------------------------------------------------------------------#
with tab_1:
    with st.form("Form 1", clear_on_submit=True):
        col1, col2 =st.columns(2)
        f_name = col1.text_input("Nombres")
        l_name = col2.text_input("Apellidos")
        e_mail = st.text_input("Email Address")
        p_assword = st.text_input("Password", value="", type="password")
        p_assword_c = st.text_input("Confirm Password", type="password")
        day,month,year = st.columns(3)
        d_ay = day.text_input("Day")
        m_onth = month.text_input("Month")
        y_ear = year.text_input("Year")
        s_state = st.form_submit_button("Submit")

    
        if s_state:
            if f_name == "" and l_name == "" :
                st.warning("Por favor llene los campos arriba")
        else:
            st.success("Formulario enviado exitosamente {}".format(f_name))

            df = pd.read_csv('D:/Streamlit_projects/Datasets/formulario_registro.csv')
            # separador = ';' aqui omitimos esta sentencia y la utilizaremos mas adelante
            data = pd.DataFrame([{'nombres':f_name,
                               'apellidos':l_name,
                               'email':e_mail,
                               'password':p_assword,
                               'confirmar':p_assword_c,
                               'anio':y_ear,
                               'mes':m_onth,
                               'dia':d_ay
            }])
            df = df.append(pd.DataFrame(data=data)) 
            df.to_csv('D:/Streamlit_projects/Datasets/formulario_registro.csv', index = False)
        

    
           
           
#----------------------------------------------------------------------------------------------#

with tab_2:
    
    with st.form(key="Salary Form"):
        col1, col2, col3 = st.columns([3,2,1])
        with col1:
         amount = st.number_input("Valor Hora $")

        with col2:
         hour_per_week = st.number_input("Horas por semana",1,120)

        with col3:
            st.text("Salary")
            submit_salary = st.form_submit_button(label = "Calcular")

    if submit_salary:
        with st.expander("Resultado"):
            daily = [amount * 8]
            weekly = [amount * hour_per_week]
            df_2 = pd.DataFrame({'hourly':amount, 'daily': daily, 'weekly':weekly})
            st.dataframe(df_2)

    
    with st.form(key="Form2"):
        fi_name = col1.text_input("Nombres")
        la_name = col2.text_input("Apellidos")
        d_ob = st.date_input("Fecha de Nacimiento")
        em_ail = st.text_input("Email Address")   
     
        s1_state = st.form_submit_button(label="Registro")

        if s1_state:
            st.success("Usted {} se ha registrado".format(fi_name))

            daily = amount * 8
            weekly = amount * hour_per_week
            
            df_1 = pd.read_csv('D:/Streamlit_projects/Datasets/formu_calcular.csv')
            data1 = pd.DataFrame([{'nombres':fi_name,
                               'apellidos':la_name,
                               'fecha_nacimiento':d_ob,
                               'email':em_ail,
                               'amount':amount,
                               'hours':hour_per_week,
                               'daily':daily,
                               'weekly':weekly
                               
            }])
            df_1 = df_1.append(pd.DataFrame(data=data1)) 
            df_1.to_csv('D:/Streamlit_projects/Datasets/formu_calcular.csv', index = False)

            
    

with tab_3:
    form2 = st.form(key="Form3", clear_on_submit=True)
    username = form2.text_input("Nombre de Usuario")
    jobtype = form2.selectbox("Profesion", ["Developer", "Data Scientisi", "Doctor"])

    s2_state = form2.form_submit_button("Login")

    if s2_state:
        st.write(username.upper())


                


                
            


            






