import streamlit as st
import random
from utils.sqlite_store import insertar
from utils.nov_memory import append_entry
from utils.nov_memory import get_last_entry

# Page title
st.title("🎯 Goals")

# Goal, target date, and optional motivation behind it
meta = st.text_input("What goal do you want to achieve?")
fecha = st.date_input("When would you like to achieve it by?")
razon = st.text_area("Why do you want to achieve this goal? (optional)")

# Warm, randomized companion message shown above the save button
st.info(random.choice([
    "The feeling of accomplishing what you set out to do is incredible.",
    "Every great achievement begins with the decision to try.",
    "Celebrating each small step is what builds the path.",
    "Simply naming a goal already says something about you.",
    "The journey there will change you too, not just the outcome.",
    "It doesn't matter if the goal is big or small — it's yours, and that's enough.",
    "I like that you're putting this into words instead of just carrying it around.",
    "Whatever this goal means to you, I'd like to understand it.",
    "I trust you have what it takes to pursue this.",
    "This goal says something about what actually matters to you.",
]))

if st.button("Save"):

    # Require at least the goal text before saving
    if meta.strip() == "":
        st.warning("Write the goal so you can save it.")
    else:

        # Bundle date and reason into a single extra field
        extra = f"{fecha} | {razon}"

        # Persist the entry to SQLite and to the JSON memory
        insertar("goal", meta, extra)
        append_entry(
            {
                "section": "goals",
                "text": meta.strip(),
                "tags": [],
                "mode": "normal",
                "extra": extra,
            }
        )

        # Confirm the save and flag the last entry for display below
        st.success("Goal saved. Let's go for it 💪")
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