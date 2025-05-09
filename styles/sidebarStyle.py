import streamlit as st

def sidebarStyle():
    st.markdown("""
        <style>
        /* Fondo del sidebar */
        section[data-testid="stSidebar"] {
            background-color: #798EB5 !important;
        }

        /* Texto y controles del sidebar */
        section[data-testid="stSidebar"] * {
            color: white ;
        }

        /* Etiquetas */
        section[data-testid="stSidebar"] label {
            color: red !important;
        }

        /* Opciones de selectbox y radio */
        .stSelectbox, .stRadio {
            color: blue !important;
        }
        </style>
    """, unsafe_allow_html=True)