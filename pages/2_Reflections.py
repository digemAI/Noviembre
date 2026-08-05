import streamlit as st
import random
from utils.sqlite_store import insertar
from utils.nov_memory import append_entry
from utils.nov_memory import get_last_entry

# Page title
st.title("💭 Reflections")

# Main input plus an optional tag for the reflection
texto = st.text_area("What have you been thinking about lately?")
extra = st.text_input("If you'd like, add a keyword or topic (optional)")

# Warm, randomized companion message shown above the save button
st.info(random.choice([
    "A free mind is easier to carry.",
    "Giving your thoughts a voice is a great first step.",
    "Exploring your ideas is how the mind understands itself.",
    "Sometimes just putting it into words brings clarity.",
    "Your thoughts matter, even the ones that feel confusing.",
    "The mind is a garden; exploring it is caring for it.",
    "There's no right or wrong thought here.",
    "I'd like to hear what's on your mind, in your own words.",
    "Every reflection is part of your path.",
    "Allowing yourself this space is a gift you give yourself.",
]))

# Persist the entry to SQLite and to the JSON memory on save
if st.button("Save"):
    if texto.strip() == "":
        st.warning("Write at least one reflection so you can save it.")
    else:

        # Save to SQLite as historial
        insertar("reflection", texto, extra)
        append_entry(
            {
                "section": "reflections",
                "text": texto.strip(),
                "tags": [extra.strip()] if extra.strip() else [],
                "mode": "normal",
            }
        )

        # Confirm the save and flag the last entry for display below
        st.success("Got it — thank you for putting this into words.")
        st.session_state["show_last_saved"] = True

# Show a short preview of the last saved entry, if any
if st.session_state.get("show_last_saved"):
    last = get_last_entry()
    if last:
        texto_last = last.get("text", "").strip()
        categoria = last.get("section", "entry")

        # Trim the preview text to keep the caption short
        if texto_last:
            st.caption(
                f"Last entry ({categoria}): "
                f"{texto_last[:120]}{'...' if len(texto_last) > 120 else ''}"
            )

    # Reset the flag so the preview only shows right after saving
    st.session_state["show_last_saved"] = False