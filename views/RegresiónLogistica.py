import streamlit as st
from styles.sidebarStyle import sidebarStyle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score, confusion_matrix, precision_score, accuracy_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

@st.cache_data
def cargar_dataset():
    df = pd.read_csv('./db/Tasmania_datos_limpios.csv', encoding='latin1')
    return df


def ShowRegresiónLogistica():
    st.divider()
    st.title("Regresión Logística")

    # Aplicamos estilos del sidebar
    sidebarStyle()

    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: white; font-weight: bold;'>Controles del gráfico</h1>", unsafe_allow_html=True)

        # Cargar dataset
        df = cargar_dataset()

        # Filtrar solo columnas con exactamente 2 valores únicos (variables dicotómicas)
        dicotomicas = df.select_dtypes(include=[np.number, 'object']).apply(lambda col: col.nunique() == 2)
        df_dicotomicas = df.loc[:, dicotomicas]

        # Select de variable dependiente
        variable_dependiente = st.selectbox(
            "Selecciona la variable dependiente",
            options=df_dicotomicas.columns.tolist(),
            index=None,
            placeholder="Selecciona una variable..."
        )

        # Versión corregida del multiselect
        variables_independientes = st.multiselect(
            "Selecciona una o más variables independientes",
            options=[col for col in df.columns 
                    if col != variable_dependiente 
                    and pd.api.types.is_numeric_dtype(df[col])],  # Solo numéricas
            default=None,
            placeholder="Elige variables numéricas..."
        )


    # Validación
    if variable_dependiente is None or len(variables_independientes) < 1:
        st.warning("⚠️ Selecciona una variable dependiente y al menos una independiente para continuar.")
        return

    st.write(f"Variables independientes seleccionadas: **{', '.join(variables_independientes)}**")
    st.write(f"Variable dependiente seleccionada: **{variable_dependiente}**")

    # Procesamiento
    Vars_Indep = df[variables_independientes].copy()
    Var_Dep = df[variable_dependiente].copy()

    # Convertir dicotómicas de texto a 0/1
    for col in Vars_Indep.columns:
        if Vars_Indep[col].dtype == 'object':
            uniques = Vars_Indep[col].unique()
            if len(uniques) == 2:
                Vars_Indep[col] = Vars_Indep[col].map({uniques[0]: 0, uniques[1]: 1})

    if Var_Dep.dtype == 'object':
        uniques = Var_Dep.unique()
        if len(uniques) == 2:
            Var_Dep = Var_Dep.map({uniques[0]: 0, uniques[1]: 1})

    X = Vars_Indep
    Y = Var_Dep

    # Dividir y escalar
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
    escalar = StandardScaler()
    X_train = escalar.fit_transform(X_train)
    X_test = escalar.transform(X_test)

    # Modelo
    modelo = LogisticRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    # Métricas
    precision_false = precision_score(y_test, y_pred, average="binary", pos_label=0)
    exactitud = accuracy_score(y_test, y_pred)
    sensibilidad_false = recall_score(y_test, y_pred, average="binary", pos_label=0)
    sensibilidad_true = recall_score(y_test, y_pred, average="binary", pos_label=1)
    precision_true = precision_score(y_test, y_pred, average="binary", pos_label=1)

    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        st.metric(
            label="Precisión del modelo en true",
            value=f"{precision_true:.4f}",
            help="Proporción de verdaderos positivos entre los elementos predichos como positivos."
        )
        st.metric(
            label="Precisión del modelo en false",
            value=f"{precision_false:.4f}",
            help="Proporción de verdaderos positivos entre los elementos predichos como positivos."
        )
    with col2:
        st.metric(
            label="Exactitud del modelo",
            value=f"{exactitud:.4f}",
            help="Porcentaje de predicciones correctas sobre el total de predicciones."
        )
    with col3:
        st.metric(
            label="Sensibilidad en true (Recall)",
            value=f"{sensibilidad_true:.4f}",
            help="Proporción de verdaderos positivos detectados sobre el total de casos positivos reales."
        )
        st.metric(
            label="Sensibilidad en false (Recall)",
            value=f"{sensibilidad_false:.4f}",
            help="Proporción de verdaderos positivos detectados sobre el total de casos positivos reales."
        )

    st.divider()
    st.markdown("### Matriz de confusión")
    matriz = confusion_matrix(y_test, y_pred)
    st.write(matriz)

    # Heatmap de la matriz de confusión
    st.markdown("### Heatmap de la matriz de confusión")
    fig, ax = plt.subplots()
    sns.heatmap(matriz, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                xticklabels=["Pred. Negativo", "Pred. Positivo"],
                yticklabels=["Real Negativo", "Real Positivo"])
    ax.set_xlabel("Predicción")
    ax.set_ylabel("Valor Real")
    st.pyplot(fig)
