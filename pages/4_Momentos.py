import streamlit as st
from utils.db import insertar

st.title("📌 Momentos importantes")

momento = st.text_input("Ponle un título al momento")
descripcion = st.text_area("Cuéntame qué pasó")
importancia = st.slider("¿Qué tanto te marcó este momento? (0 a 10)", 0, 10, 5)

if st.button("Guardar"):
    if momento.strip() == "" or descripcion.strip() == "":
        st.warning("Escribe al menos título y descripción para guardarlo.")
    else:
        extra = f"Importancia: {importancia}"
        insertar("momento", descripcion, extra)
        st.success("Momento guardado. Gracias por compartirlo ✨")
