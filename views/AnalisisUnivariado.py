import streamlit as st
import plotly.express as px
import pandas as pd
from styles.sidebarStyle import sidebarStyle

@st.cache_resource
def load_data():
    return pd.read_csv('db/Tasmania_datos_limpios.csv', encoding='latin1')

def univariate_analysis():
    st.divider()
    st.title("Análisis Univariado")

    # Cargar datos
    df = load_data()
    df = df[['room_type', 'host_response_time', 'host_verifications', 'property_type', 'license']]

    # Aplicamos estilos del sidebar
    sidebarStyle()

    # Sidebar con controles
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: white; font-weight: bold;'>Controles del gráfico</h1>", unsafe_allow_html=True)
        variable = st.selectbox(
            "Selecciona la variable a analizar",
            df.columns.tolist()
        )

        tipo_grafico = st.radio(
            "Tipo de gráfico",
            ["Barras", "Pastel"],
            horizontal=False,
        )

    # Procesamiento
    counts = df[variable].value_counts().reset_index()
    counts.columns = ['Categoría', 'Cantidad']

    # Gráfico
    if tipo_grafico == "Barras":
        fig = px.bar(
            counts,
            x='Categoría',
            y='Cantidad',
            title=f"Distribución de {variable}",
            color='Categoría',
            text='Cantidad'
        )
        fig.update_layout(showlegend=False)
    else:
        fig = px.pie(
            counts,
            names='Categoría',
            values='Cantidad',
            title=f"Distribución de {variable}",
            hole=0.3 if len(counts) > 5 else 0
        )

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**Frecuencia de la variable categórica**")
    with st.expander("Ver datos tabulares"):
        st.dataframe(counts.sort_values('Cantidad', ascending=False))
