import streamlit as st
import random
from utils.db import insertar
from utils.nov_memory import append_entry
from utils.nov_memory import get_last_entry

# Titulo
st.title("💭 Reflexiones")

# Salto de linea
texto = st.text_area("¿Qué has estado pensando últimamente?")
extra = st.text_input("Si lo deseas, agrega una palabra clave o tema (opcional)")

# Opciones aleatorias
st.info(random.choice([
    "Una mente libre ayuda a la salud mental.", 
    "Dar voz a tus pensamientos es un gran primer paso", 
    "Explorar tus ideas es cómo la mente se entiende a sí misma", 
    "A veces, solo ponerlo en palabras ya trae claridad", 
    "Tus pensamientos son importantes, incluso los que parecen confusos", 
    "La mente es un jardín; explorarla es cuidarla", 
    "No hay pensamiento" "correcto" "o" "incorrecto" "aquí", 
    "compartas tu mundo interior conmigo", 
    "Cada reflexión es parte de tu camino", 
    "Permitirse este espacio es un regalo que te das", 
]))

# Guardamos la informacion
if st.button("Guardar"):
    if texto.strip() == "":
        st.warning("Escribe al menos una reflexión para guardarla.")
    else:

        # Guardamos en la base de datos (SQLite) como historial
        insertar("reflexion", texto, extra)
        append_entry(
            "data/nov_memory.json",
            {
                "section": "reflexiones",
                "text": texto.strip(),
                "tags": [extra.strip()] if extra.strip() else [],
                "mode": "normal",
            },
        )

        # Mensaje de confirmación y bandera para mostrar el último registro
        st.success("Lo registré. Gracias por compartir.")
        st.session_state["show_last_saved"] = True

# Si guardamos algo, mostramos el ultimo recuerdo
if st.session_state.get("show_last_saved"):
    last = get_last_entry()
    if last:
        texto_last = last.get("text", "").strip()
        categoria = last.get("section", "registro")

        # Versión corta del último texto
        if texto_last:
            st.caption(
                f"Último registro ({categoria}): "
                f"{texto_last[:120]}{'...' if len(texto_last) > 120 else ''}"
            )

    # Guardamos la reflexión en el historial
    st.session_state["show_last_saved"] = False
