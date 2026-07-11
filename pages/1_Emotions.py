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
    "Take all the time you need.",
    "I want to listen to you",
    "I'm here for you",
    "Tell me more, if you want",
    "It's normal to feel this way sometimes.",
    "Thank you for sharing this with me.",
    "Is there something I can help with?",
    "You're not alone in this",
    "We can talk about whatever you need.",
    "If you'd rather change the topic, that's fine too.",
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

        st.success("Thanks for sharing. I've noted it.")
