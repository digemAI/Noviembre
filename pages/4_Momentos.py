import streamlit as st
import random
from utils.db import insertar
from utils.nov_memory import append_entry
from utils.nov_memory import get_last_entry

# Titulo
st.title("📌 Momentos importantes")

momento = st.text_input("Ponle un título al momento")
descripcion = st.text_area("Cuéntame qué pasó")
importancia = st.slider("¿Qué tanto te marcó este momento? (0 a 10)", 0, 10, 5)

# Opciones aleatorias
st.info(random.choice([
    "Estoy aqui para ayudarte.", 
    "Gracias por compartir algo tan personal conmigo", 
    "Tu momento y su intensidad son completamente válidos", 
    "¿Te gustaría contarme más sobre ese título o ese número?", 
    "Nombrar y medir nuestros momentos es un acto de autoconocimiento valiente", 
    "Este es un espacio seguro para todo lo que ese momento te hace sentir", 
    "Guardar un momento así en la memoria es importante. Gracias por dejarme verlo", 
    "No estás solo/a en cómo te afectan las experiencias", 
    "Si quieres, podemos quedarnos aquí con ese sentimiento", 
    "Tu historia y sus momentos son importantes. Sigo aquí para lo que necesites", 
    ]))

# Boton de guardar 
if st.button("Guardar"):

    # Titulo y descripcion
    if momento.strip() == "" or descripcion.strip() == "":
        st.warning("Escribe al menos título y descripción para guardarlo.")
    else:
        extra = f"Importancia: {importancia}"
        insertar("momento", descripcion, extra)

    # Guardamos en la memoria 
        append_entry(
            "data/nov_memory.json",
            {
                "section": "momentos",
                "text": descripcion.strip(),
                "tags": [momento.strip()] if momento.strip() else [],
                "mode": "normal",
                "importance": int(importancia),
            },
        )
        st.success("Momento guardado. Gracias por compartirlo ✨")
        st.session_state["show_last_saved"] = True

 # Validamos que haya escrito una meta
if st.session_state.get("show_last_saved"):
    last = get_last_entry()
    if last:
        texto_last = last.get("text", "").strip()
        categoria = last.get("section", "registro")
        if texto_last:
            st.caption(
                f"Último registro ({categoria}): "
                f"{texto_last[:120]}{'...' if len(texto_last) > 120 else ''}"
            )
    st.session_state["show_last_saved"] = False
