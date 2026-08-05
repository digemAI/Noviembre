import streamlit as st
import random
from utils.sqlite_store import insertar
from utils.nov_memory import append_entry

# Page title
st.title("🫣 Emotions")

# Emotion selector for the current entry
emocion = st.selectbox(
    "How are you feeling today?",
    ["Happy", "Sad", "Anxious", "At peace", "Confused", "Motivated", "Tired"],
)

# Free-text space for the user to expand on how they feel
texto = st.text_area("Tell me whatever you want...")

# Warm, randomized companion message shown above the save button
st.info(random.choice([
    "Take all the time you need with this.",
    "I want to hear it, however it comes out.",
    "I'm right here with you on this one.",
    "Whatever this is, it's welcome here.",
    "It's okay to feel this way — no need to explain it perfectly.",
    "Thank you for trusting me with this.",
    "This doesn't have to be tidy to matter.",
    "You're not carrying this alone.",
    "No rush — write it the way it actually feels.",
    "This is your space, however you want to fill it today.",
]))

# Persist the entry to SQLite and to the JSON memory on save
if st.button("Save"):
    if texto.strip() == "":
        st.warning("Write at least one sentence so I can save it.")
    else:
        insertar("emotion", texto, emocion)
        append_entry(
            {
                "section": "emotions",
                "text": texto.strip(),
                "detected_emotion": emocion.lower(),
                "tags": [],
                "mode": "normal",
            }
        )

        st.success("Got it — thank you for letting me in on this.")