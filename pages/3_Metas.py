import streamlit as st
import random
from utils.db import insertar
from utils.nov_memory import append_entry
from utils.nov_memory import get_last_entry

# Titulo
st.title("🎯 Metas")

meta = st.text_input("¿Cuál es la meta que deseas lograr?")
fecha = st.date_input("¿Para cuándo deseas lograrla?")
razon = st.text_area("¿Por qué quieres lograr esta meta? (opcional)")

# Opciones aleatorias
st.info(random.choice([
    "La sensacion de cumplir lo que te propones es increibe.", 
    "Todo gran logro comienza con la decisión de intentarlo", 
    "Celebrar cada paso pequeño es lo que construye el camino", 
    "El simple hecho de tener una meta ya habla de tu determinación", 
    "El viaje hacia tu meta también te transformará", 
    "No importa si la meta es grande o pequeña; lo que importa es que es tuya", 
    "Compartir tu objetivo es una forma poderosa de darle vida", 
    "Las metas son la brújula que da dirección a nuestros días", 
    "Confío en que tienes lo necesario para perseguirla", 
    "Esa meta es un reflejo de lo que es importante para ti", 
]))

if st.button("Guardar"):

     # Validamos que haya escrito una meta
    if meta.strip() == "":
        st.warning("Escribe la meta para poder guardarla.")
    else:

        # Texto con fecha y raxon 
        extra = f"{fecha} | {razon}"

        # Guardamos en la base de datos y en la memoria 
        insertar("meta", meta, extra)
        append_entry(
            "data/nov_memory.json",
            {
                "section": "metas",
                "text": meta.strip(),
                "tags": [],
                "mode": "normal",
                "extra": extra,
            },
        )

        # Confirmacion visual y ultimo registro
        st.success("Meta guardada. Vamos por ella 💪")
        st.session_state["show_last_saved"] = True

# Mostramos el ultimo registro guardado
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
