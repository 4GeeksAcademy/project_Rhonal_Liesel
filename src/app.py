import pickle
from pickle import load
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


with open("/workspaces/project_Rhonal_Liesel/src/modelo.pkl", "rb") as f:
    rf_model = pickle.load(f)

    #----------------------------------------------------------------------------------------------------------------------------------------------------

    import streamlit as st

    st.set_page_config(
    page_title="Predicción RUL - Turbofan",
    page_icon="🛠️",
    layout="wide"
)

    st.title("Predicción de Vida Útil Remanente (RUL) — NASA CMAPSS")
    st.write("Usa el menú lateral para navegar entre las secciones.")

    st.title("Introducción al Proyecto")
st.write("""
Este proyecto utiliza el dataset **NASA CMAPSS** para predecir la **vida útil remanente (RUL)** de motores turbofán.
""")

st.subheader("¿Qué es el RUL?")
st.write("""
El **Remaining Useful Life (RUL)** indica cuántos ciclos le quedan a un motor antes de fallar.
""")

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/5/5f/Diagrama_de_un_motor_Propfan.jpg",
    caption="Diagrama de un motor Propfan",
    width=500  
)
st.subheader("Características del dataset")
st.write("""
- 160,359 registros  
- 4 subconjuntos: FD001, FD002, FD003, FD004  
- 21 sensores + 3 configuraciones de operación  
- Dataset real de motores aeronáuticos  
""")
#-----------------------------------------------------------------------------------------------------------------
st.title("📊 Exploración del Dataset")

df = pd.read_csv("/workspaces/project_Rhonal_Liesel/notebook/data/dataset.csv")

subset = st.selectbox("Selecciona un subconjunto", ["FD001", "FD002", "FD003", "FD004"])
df_sub = df[df["dataset"] == subset]


st.subheader("Distribución del RUL")
fig, ax = plt.subplots(figsize=(2, 2))
sns.histplot(df_sub["RUL"], bins=40, ax=ax)
st.pyplot(fig, use_container_width=False)

#-------------------------------------------------------------------------------------------------------------------
st.title("⭐ Predicción en Tiempo Real del RUL")


        #-----------------------------------------------------------------------------------------------------------------------

# Columnas usadas para entrenar
feature_cols = [c for c in df.columns if c not in ["RUL", "dataset"]]

st.title("Predicción de RUL en tiempo real")

st.subheader("Introduce los valores de los sensores")

inputs = {}

for col in feature_cols:
    min_val = float(df[col].min())
    max_val = float(df[col].max())
    default = float(df[col].median())

    inputs[col] = st.slider(col, min_val, max_val, default)

# Convertir a vector
X = np.array([inputs[col] for col in feature_cols]).reshape(1, -1)

    # Si usas scaler:
# X = scaler.transform(X)

if st.button("Predecir RUL"):
    pred = rf_model.predict(X)[0]
    st.metric("RUL estimado (ciclos)", f"{pred:.1f}")

    if pred > 100:
        st.success("🟢 Estado: SEGURO")
    elif pred > 50:
        st.warning("🟡 Estado: ATENCIÓN")
    else:
        st.error("🔴 Estado: CRÍTICO")
