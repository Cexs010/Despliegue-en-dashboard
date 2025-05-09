# Importamos las librerías necesarias
import streamlit as st
from components.selectbox_personalizado import mostrar_selectbox
from views.AnalisisUnivariado import univariate_analysis
from views.landingPage import ShowLandingPage
from views.RegresiónSimple import ShowRegresiónSimple
from views.RegresiónMultiple import ShowRegresiónMultiple
from views.RegresiónLogistica import ShowRegresiónLogistica

# Configuración de la página
st.set_page_config(layout="wide")

col1, col2 = st.columns([1, 4])
with col1:
    st.markdown('<div class="padding:10px;">', unsafe_allow_html=True)
    st.image("helpers/tasmania.webp", width=150)
with col2:
    # Usas el componente
    vista_seleccionada = mostrar_selectbox()


############################
#Cargar vistas dinamicamente
############################
if vista_seleccionada == "Home":
    ShowLandingPage()
if vista_seleccionada == "Analisis Univariado":
    univariate_analysis()
if vista_seleccionada == "Regresión Simple":
    ShowRegresiónSimple()
if vista_seleccionada == "Regresión Múltiple":
    ShowRegresiónMultiple()
if vista_seleccionada == "Regresión Logística":
    ShowRegresiónLogistica()