import streamlit as st
from utils.db import insertar

st.title("😊 Emociones")

emocion = st.selectbox(
    "¿Cómo te sientes hoy?",
    ["Feliz", "Triste", "Ansioso", "En paz", "Confundido", "Motivado", "Cansado"],
)

texto = st.text_area("Cuéntame lo que quieras...")

if st.button("Guardar"):
    if texto.strip() == "":
        st.warning("Escribe al menos una oración para poder guardarlo.")
    else:
        insertar("emocion", texto, emocion)
        st.success("Gracias por compartir. Lo registré.")
