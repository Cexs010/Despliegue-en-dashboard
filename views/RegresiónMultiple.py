import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from styles.sidebarStyle import sidebarStyle
from sklearn.linear_model import LinearRegression
model = LinearRegression()
import plotly.graph_objects as go

@st.cache_data
def cargar_datasets():
    return {
        "Casa o Apartamento Entero": pd.read_csv('./db/Tasmania_Entire_Home_Apt.csv'),
        "Cuarto Privado": pd.read_csv('./db/Tasmania_Private_Room.csv'),
        "Habitación Compartida": pd.read_csv('./db/Tasmania_Shared_Room.csv'),
        "Cuarto de Hotel": pd.read_csv('./db/Tasmania_Hotel_Room.csv'),
    }


def ShowRegresiónMultiple():
    st.divider()
    st.title("Regresión Multiple")

    # Aplicamos estilos del sidebar
    sidebarStyle()

    #Opciones de DataSets
    datasets = cargar_datasets()

    #Creamos el sidebar
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: white; font-weight: bold;'>Controles del gráfico</h1>", unsafe_allow_html=True)

        #SelectBox con los datasets disponibles
        dataset_seleccionado = st.selectbox(
            "Selecciona el dataset a utilizar",
            options=list(datasets.keys())
        )

        # Obtenemos el DataFrame correspondiente al dataset elegido
        df = datasets[dataset_seleccionado]
        #Filtramos a variebles numericas
        df = df.select_dtypes(include=['int64', 'float64'])

        # Obtenemos la variable dependiente
        variable_dependiente = st.selectbox(
            "Selecciona la variable dependiente",
            options = df.columns.tolist(),
            index=None,
            placeholder="Selecciona una variable..." 
        )

        variables_independientes = st.multiselect(
            "Selecciona una o más variables independientes",
            options=df.columns.tolist(),
            default=None,  
            placeholder="Elige las variables..."
        )

        #Colores a seleccionar del grafico
        datosRealesColor = st.color_picker("Selecciona un color para los datos reales", "#00f900")
        prediccionesColor = st.color_picker("Selecciona un color para la predicción", "#f90000")
    
    #Contenido fuera del sidebar

    # Validación ANTES de cualquier operación con las variables
    if len(variables_independientes) < 2 or variable_dependiente is None:
        st.warning("⚠️ Selecciona ambas variables para continuar")
        return  
    #Datos selecciononados
    st.write(f"Dataset seleccionado: **{dataset_seleccionado}**")
    st.write(f"Variables independientes seleccionadas: **{', '.join(variables_independientes)}**")
    st.write(f"Variable dependiente seleccionada: **{variable_dependiente}**")  

    #######Procesamiento#######

    # Declaramos variables
    Vars_Indep = df[variables_independientes]  
    Var_Dep = df[variable_dependiente]         


    #Ajustamos el modelo con las variables antes declaradas
    model.fit(X=Vars_Indep, y=Var_Dep)

    #Predecimos los valores con el modelo ajustado
    y_predic = model.predict(Vars_Indep)
    head_predicciones = y_predic[:5]

    #Insertamos Predicciones en el DataFrame
    df.insert(0, 'PrediccionesMultiples', y_predic)

    #Evaluamos la eficiencia del modelo obtenido por medio del coeficiente R Determinación
    coef_Correl = model.score(Vars_Indep,Var_Dep)

    st.markdown("<br>", unsafe_allow_html=True) #Salto de linea

    col1, col2 = st.columns([2,2])

    with col1:
        st.write(f"Primeras 5 predicciones")
        st.dataframe(
        head_predicciones,
        column_config={"value": "PrediccionesMultiples"}
        )
    with col2:
        st.write(f"Coeficiente de Correlación del modelo")
        st.metric(
        label="Coeficiente de Correlación (R)",
        value=f"{coef_Correl:.4f}",  # Formato de 4 decimales
        help="Indica la fuerza y dirección de la relación entre X e Y"
        )

    st.divider()
    st.markdown(" **Graficas de Disperción** ")

    
    #Ciclo for para cada grafica
    for i in range(len(variables_independientes)):
        # Gráfico de dispersión
        fig = px.scatter(
            df,
            x=variables_independientes[i],
            y=variable_dependiente,
            color_discrete_sequence=[datosRealesColor],
            opacity=0.6,
            title=f"Regresión: {variable_dependiente} vs {variables_independientes[i]}"
        ).update_traces(
            name='Datos Reales',  
            showlegend=True 
        )

        # Puntos predichos
        fig.add_trace(
         go.Scatter(
            x=df[variables_independientes[i]],
            y=df['PrediccionesMultiples'],
            mode='markers',
            marker=dict(color=prediccionesColor, opacity=1, size=8),
            name='Predicciones multiples'
        )
    )

        st.plotly_chart(fig)
