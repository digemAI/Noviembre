import streamlit as st
from utils.db import insertar

st.title("🎯 Metas")

meta = st.text_input("¿Cuál es la meta que deseas lograr?")
fecha = st.date_input("¿Para cuándo deseas lograrla?")
razon = st.text_area("¿Por qué quieres lograr esta meta? (opcional)")

if st.button("Guardar"):
    if meta.strip() == "":
        st.warning("Escribe la meta para poder guardarla.")
    else:
        extra = f"{fecha} | {razon}"
        insertar("meta", meta, extra)
        st.success("Meta guardada. Vamos por ella 💪")
