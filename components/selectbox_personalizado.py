import streamlit as st

def mostrar_selectbox():
    st.markdown("""
        <style>
        /* Etiqueta del selectbox */
        .stSelectbox > label {
            color: black !important;
            font-weight: bold;
        }

        /* Contenedor del input del selectbox */
        div[data-baseweb="select"] {
            background-color: #1e3a8a !important;
            border-radius: 10px !important;
        }

        /* Texto dentro del selectbox */
        div[data-baseweb="select"] * {
            color: black !important;
        }

        /* Icono (flecha) */
        div[data-baseweb="select"] svg {
            fill: black !important;
        }

        /* Menú desplegable */
        div[data-baseweb="popover"] {
            background-color: #1e40af !important;
            color: white !important;
            border-radius: 10px;
        }

        /* Opciones del menú */
        div[data-baseweb="option"] {
            color: white !important;
            background-color: #1e40af !important;
        }

        /* Texto seleccionado (opcional, más específico aún) */
        div[data-baseweb="selected"] {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    return st.selectbox(
        'Selecciona la vista',
        ['Home','Analisis Univariado', 'Regresión Simple', 'Regresión Múltiple', 'Regresión Logística']
    )

