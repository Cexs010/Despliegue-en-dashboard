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

def ShowRegresiónSimple():
    st.divider()
    st.title("Regresión Simple")

    # Aplicamos estilos del sidebar
    sidebarStyle()

    #Opciones de DataSets
    datasets = cargar_datasets()

     # Sidebar con controles
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

        # Obtenemos la variable independiente
        variable_independiente = st.selectbox(
            "Selecciona la variable independiente",
            options = df.columns.tolist(),
            index=None,
            placeholder="Selecciona una variable..." 
        )

        #Colores a seleccionar del grafico
        datosRealesColor = st.color_picker("Selecciona un color para los datos reales", "#00f900")
        prediccionesColor = st.color_picker("Selecciona un color para la predicción", "#f90000")

    #Contenido fuera del sidebar

    # Validación ANTES de cualquier operación con las variables
    if variable_independiente is None or variable_dependiente is None:
        st.warning("⚠️ Selecciona ambas variables para continuar")
        return  # Sale de la función sin ejecutar el resto del código

    #Datos selecciononados
    st.write(f"Dataset seleccionado: **{dataset_seleccionado}**")
    st.write(f"Variable independiente seleccionada: **{variable_independiente}**")
    st.write(f"Variable dependiente seleccionada: **{variable_dependiente}**")

    #######Procesamiento#######

    #Declaramos variables dependientes e independientes para la regresión lineal
    Vars_Indep = df[[variable_independiente]]
    Var_Dep = df[[variable_dependiente]]

    # Ajustar el modelo
    model.fit(X=Vars_Indep, y=Var_Dep)

    #Predecimos los valores del total de la variable independiente
    y_predic = model.predict(Vars_Indep)
    head_predicciones = y_predic[:5]
    
    #Insertamos Predicciones en el DataFrame
    df.insert(0, 'Predicciones', y_predic)
    
    #Corroboramos cual es el coeficiente de determinación de nuestro modelo
    coef_Deter = model.score(Vars_Indep,Var_Dep)

    #Corroboramos cual es el coeficiente de Correlación de nuestro modelo
    coef_Correl = np.sqrt(coef_Deter)

    st.markdown("<br>", unsafe_allow_html=True) #Salto de linea

    #mostramos Datos obtenidos en la regresión simple
    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        st.write(f"Primeras 5 predicciones")
        st.dataframe(
        head_predicciones,
        column_config={"value": "Predicciones"},  
    )
    with col2:
        st.write(f"Coeficiente de determinación del modelo")
        st.metric(
        label="Coeficiente de determinación (R²)",
        value=f"{coef_Deter:.4f}",  # Formato de 4 decimales
        help="Indica qué porcentaje de la variabilidad de Y es explicada por X"
    )
    with col3:
        st.write(f"Coeficiente de Correlación del modelo")
        st.metric(
        label="Coeficiente de Correlación (R)",
        value=f"{coef_Correl:.4f}",  # Formato de 4 decimales
        help="Indica la fuerza y dirección de la relación entre X e Y"
    )
    
    st.divider()
    st.markdown(" **Grafica de Disperción** ")

    # Gráfico con línea de regresión visible
    fig = px.scatter(
        df,
        x=variable_independiente,
        y=variable_dependiente,
        color_discrete_sequence=[datosRealesColor],
        opacity=0.6,
        title=f"Regresión: {variable_dependiente} vs {variable_independiente}"
    ).update_traces(
        name='Datos Reales',  
        showlegend=True 
    )


    # Línea de regresión 
    fig.add_trace(
        go.Scatter(
            x=df[variable_independiente],
            y=df['Predicciones'],
            mode='lines',
            line=dict(color=prediccionesColor, width=3),
            name='Línea de Regresión'
        )
    )

    # Puntos predichos
    fig.add_trace(
        go.Scatter(
            x=df[variable_independiente],
            y=df['Predicciones'],
            mode='markers',
            marker=dict(color=prediccionesColor, opacity=1, size=8),
            name='Predicciones'
        )
    )

    st.plotly_chart(fig)
