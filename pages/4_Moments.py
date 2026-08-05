import streamlit as st
import random
from utils.sqlite_store import insertar
from utils.nov_memory import append_entry
from utils.nov_memory import get_last_entry

# Page title
st.title("📌 Important moments")

# Title, description, and a 0-10 impact rating for the moment
momento = st.text_input("Give the moment a title")
descripcion = st.text_area("Tell me what happened")
importancia = st.slider("How much did this moment affect you? (0 to 10)", 0, 10, 5)

# Warm, randomized companion message shown above the save button
st.info(random.choice([
    "I'm glad you're bringing this here.",
    "Thank you for sharing something so personal with me.",
    "Your moment and its intensity are completely valid.",
    "Would you like to tell me more about that title or that number?",
    "Naming and measuring our moments is a brave act of self-knowledge.",
    "This is a safe space for everything this moment makes you feel.",
    "Keeping a moment like this matters. Thank you for letting me see it.",
    "You're not alone in how experiences affect you.",
    "If you want, we can just stay here with that feeling for a bit.",
    "Your story and its moments matter. I'm still here for whatever you need.",
    ]))

# Persist the entry to SQLite and to the JSON memory on save
if st.button("Save"):

    # Require both title and description before saving
    if momento.strip() == "" or descripcion.strip() == "":
        st.warning("Write at least a title and description to save it.")
    else:
        extra = f"Importance: {importancia}"
        insertar("moment", descripcion, extra)

        # Store the moment with its title as a tag and its importance score
        append_entry(
            {
                "section": "moments",
                "text": descripcion.strip(),
                "tags": [momento.strip()] if momento.strip() else [],
                "mode": "normal",
                "importance": int(importancia),
            }
        )
        st.success("Moment saved. Thanks for sharing it ✨")
        st.session_state["show_last_saved"] = True

# Show a short preview of the last saved entry, if any
if st.session_state.get("show_last_saved"):
    last = get_last_entry()
    if last:
        texto_last = last.get("text", "").strip()
        categoria = last.get("section", "entry")
        if texto_last:
            st.caption(
                f"Last entry ({categoria}): "
                f"{texto_last[:120]}{'...' if len(texto_last) > 120 else ''}"
            )
    st.session_state["show_last_saved"] = False