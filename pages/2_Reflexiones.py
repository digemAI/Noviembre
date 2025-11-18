import streamlit as st
from utils.db import insertar

st.title("💭 Reflexiones")

texto = st.text_area("¿Qué has estado pensando últimamente?")

extra = st.text_input("Si lo deseas, agrega una palabra clave o tema (opcional)")

if st.button("Guardar"):
    if texto.strip() == "":
        st.warning("Escribe al menos una reflexión para guardarla.")
    else:
        insertar("reflexion", texto, extra)
        st.success("Lo registré. Gracias por compartir.")
