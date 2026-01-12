import streamlit as st
import random
from utils.db import insertar
from utils.nov_memory import append_entry

# Titulo
st.title("🫣 Emociones")

# Elige una opcion 
emocion = st.selectbox(
    "¿Cómo te sientes hoy?",
    ["Feliz", "Triste", "Ansioso", "En paz", "Confundido", "Motivado", "Cansado"],
)

# salto de linea
texto = st.text_area("Cuéntame lo que quieras...")


# Opciones aleatorias
st.info(random.choice([
    "Tomate el tiempo que necesites.", 
    "Quiero escucharte", 
    "Estoy aquí para ti", 
    "Cuéntame más, si quieres",  
    "Es normal sentirse así a veces.", 
    "Gracias por compartirlo conmigo.", 
    "¿Hay algo en lo que pueda ayudarte?", 
    "No estás solo/a en esto", 
    "Podemos hablar de lo que necesites.", 
    "Si prefieres cambiar de tema, también está bien.", 
]))

# Guardamos la informacion
if st.button("Guardar"):
    if texto.strip() == "":
        st.warning("Escribe al menos una oración para poder guardarlo.")
    else:
        insertar("emocion", texto, emocion)
        append_entry(
            "data/nov_memory.json",
            {
                "section": "emociones",
                "text": texto.strip(),
                "detected_emotion": emocion.lower(),
                "tags": [],
                "mode": "normal",
            },
        )

        st.success("Gracias por compartir. Lo registré.")
