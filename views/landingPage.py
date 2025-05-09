import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def cargar_dataset():
    columnas_necesarias = ["latitude", "longitude", "room_type"]
    df = pd.read_csv('./db/Tasmania_datos_limpios.csv', usecols=columnas_necesarias, encoding='latin1')
    return df

def ShowLandingPage():
    ####################################
    #Landing Page
    ####################################
    st.write("")
    st.divider()
    # Fondo tipo banner
    st.markdown("<h1 style='text-align: center;'>Bienvenido al Dashboard de Tasmania</h1>", unsafe_allow_html=True)
    st.image("./helpers/hobart - beach.webp", use_container_width=True)

    st.divider()
    st.markdown("<h3 style='text-align: center; '>Conoce algunos de los datos importantes de Tasmania</h3>", unsafe_allow_html=True)
    # Tres columnas para tarjetas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("./helpers/demonio-de-tasmania.webp")
        st.markdown("""
        <div style="background-color: #2a4ba0; color: white; padding: 10px; border-radius: 10px;">
        <strong>Fauna Única</strong><br>
        <div style="font-size: 14px;">
        Tasmania es hogar del emblemático demonio de Tasmania, un marsupial carnívoro conocido por sus potentes gruñidos y su aspecto peculiar. Actualmente solo se encuentra en estado salvaje en Tasmania, ya que desapareció del continente australiano hace siglos. A pesar de su fama, enfrenta un grave riesgo de extinción , lo que ha motivado numerosos esfuerzos de conservación.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image("./helpers/tasmania-hobart-city-view.webp")
        st.markdown("""
        <div style="background-color: #2a4ba0; color: white; padding: 10px; border-radius: 10px;">
        <strong>Población y Estilo de Vida</strong><br>
        <div style="font-size: 14px;">
        Con alrededor de 541,000 habitantes, Tasmania ofrece un estilo de vida relajado en armonía con la naturaleza. Hobart, su capital y ciudad principal, combina una vibrante vida cultural con un ambiente tranquilo. La baja densidad poblacional de la isla contribuye a preservar sus extensos paisajes naturales, haciendo de Tasmania un lugar ideal para quienes buscan calidad de vida y contacto con el medio ambiente.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.image("./helpers/Park.webp")
        st.markdown("""
        <div style="background-color: #2a4ba0; color: white; padding: 10px; border-radius: 10px;">
        <strong>Belleza Natural</strong><br>
        <div style="font-size: 14px;">
        Más del 40% del territorio de Tasmania está protegido en parques nacionales y reservas naturales, lo que garantiza la conservación de su impresionante biodiversidad. Destinos como el Parque Nacional Cradle Mountain-Lake St Clair y la Bahía de los Fuegos ofrecen paisajes inigualables, atrayendo a visitantes que buscan aventuras al aire libre, experiencias culturales únicas y una profunda conexión con la naturaleza.
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    # Mapa con la ubicación de Tasmania
    df = cargar_dataset()  
    st.markdown("<h3 style='text-align: center; '>Mapa de Tasmania</h3>", unsafe_allow_html=True)
    
    # Crear el mapa 
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="room_type",  
        zoom=6,  
        height=600,  # Altura del mapa
        hover_name="room_type",  
        title="Tipos de Alojamientos en Tasmania"
    )

    # Estilo del mapa 
    fig.update_layout(mapbox_style="open-street-map")

    # Mostrar 
    st.plotly_chart(fig, use_container_width=True)