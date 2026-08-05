import streamlit as st
import random
from utils.sqlite_store import init_db, insertar
from utils.nov_memory import append_entry


# Set page title, icon, and prepare the SQLite database
st.set_page_config(page_title="Noviembre", page_icon="🟣")
init_db()

# Store the user's name, chat history, header icon, and turn count
if "nombre" not in st.session_state:
    st.session_state["nombre"] = None

if "chat" not in st.session_state:
    st.session_state["chat"] = []

if "logo_icon" not in st.session_state:
    st.session_state["logo_icon"] = "🟣"

if "turnos_usuario" not in st.session_state:
    st.session_state["turnos_usuario"] = 0

if "last_emotion" not in st.session_state:
    st.session_state["last_emotion"] = None


def detectar_emocion(texto: str) -> str:
    """Classify free text into an emotion category using keyword matching."""
    t = texto.lower()

    palabras_alegria = [
        "happy", "glad", "cheerful", "excited", "thrilled", "in love",
        "i love", "i like", "great day", "good day", "wonderful day"
    ]
    palabras_tristeza = [
        "sad", "cried", "crying", "hurts", "death", "died", "lost", "i lost",
        "i miss", "missing", "empty", "nostalgia", "alone", "lonely", "loneliness"
    ]
    palabras_ira = [
        "angry", "mad", "hate", "furious", "fed up", "annoyed", "rage", "pissed off"
    ]
    palabras_reflexion = [
        "i've been thinking", "i have been thinking", "i realize", "i think that",
        "reflecting", "i started thinking", "it made me think"
    ]
    palabras_metas = [
    "i want to achieve",
    "my objective",
    "my goal",
    "goal is",
    "i plan to",
    "i'm planning to",
    "i want to do",
    "i want to earn",
    "i want to save",
    "planning to save",
    "by the end of the year",
    "by the end of the month",
    "save 100k",
    "make 100k",
    "put together 100k",
    "save a hundred thousand",
    ]
    palabras_momento = [
        "today something happened", "yesterday was", "it marked me",
        "it surprised me", "something happened", "happened today"
    ]

    # Check categories in priority order, most emotionally urgent first
    for w in palabras_ira:
        if w in t:
            return "anger"
    for w in palabras_tristeza:
        if w in t:
            return "sadness"
    for w in palabras_alegria:
        if w in t:
            return "joy"
    for w in palabras_metas:
        if w in t:
            return "goal"
    for w in palabras_reflexion:
        if w in t:
            return "reflection"
    for w in palabras_momento:
        if w in t:
            return "moment"

    return "neutral"


def emocion_a_icono(emocion: str) -> str:
    """Map a detected emotion to its header icon color."""
    mapa = {
        "joy": "🟡",
        "sadness": "🔵",
        "anger": "🔴",
        "reflection": "🟠",
        "goal": "🟢",
        "moment": "🟣",   # important moment / memory
        "neutral": "🟣"
    }
    return mapa.get(emocion, "🟣")


def construir_respuesta(texto_usuario: str, nombre: str, emocion: str, turno: int, continuidad: bool = False):
    """Build a warm, natural reply that deepens the conversation and, when the same
    feeling resurfaces within this chat, acknowledges the thread instead of resetting."""

    # Occasionally use the person's name past the opening turn so it reads
    # like a friend talking, not a form addressing a user
    usar_nombre = nombre and (turno == 1 or random.random() < 0.35)
    nombre_frase = f", {nombre}" if usar_nombre else ""

    # First turn always opens space rather than reacting to emotion
    if turno == 1:
        return (
            f"Would you like to tell me a bit more about that{nombre_frase}? "
            "We can take it apart slowly, no rush.",
            "neutral",
        )

    respuestas = {
        "joy": [
            f"Sounds like something good happened today{nombre_frase}. I'm glad for you.",
            "There's a lot of light in what you're writing. It's nice to sit in this with you for a second.",
            f"I can feel the good mood in this{nombre_frase} — thank you for bringing it here.",
            "This is the kind of thing worth pausing on. It matters that you wanted to share it.",
        ],
        "sadness": [
            "What you're telling me feels heavy, like something that still hurts. You're not alone in this, even through a screen.",
            "This seems to touch you deeply. We can sit with it for a while, no rush.",
            f"I hear how much this weighs on you{nombre_frase}. I'm not going anywhere.",
            "Some things don't need fixing right away — just someone to hold them with you for a bit.",
        ],
        "anger": [
            "I can tell this is really bothering you. It's valid to feel that.",
            "Sounds like a really frustrating moment. You can let it out here without holding back.",
            f"This clearly got to you{nombre_frase}, and that's fair. Say whatever you need to.",
            "No need to soften it for me. Whatever this brought up, it can land here.",
        ],
        "goal": [
            "What you're saying sounds like an important goal for you.",
            f"I like how you're putting it{nombre_frase}, it feels like a clear objective.",
            "There's real intention behind this. It's good to hear you naming it out loud.",
            "This sounds like something you've actually been carrying for a while, not just a passing idea.",
        ],
        "reflection": [
            "I like how you're looking at this, you've clearly been thinking about it.",
            "What you're writing sounds like a solid reflection.",
            f"You're really turning this over, aren't you{nombre_frase}? I like following your thinking here.",
            "This sounds like one of those thoughts that keeps circling back until it's said out loud.",
        ],
        "moment": [
            "Seems like what happened left a mark on your day.",
            "Sounds like one of those moments that keeps replaying in your mind.",
            f"This clearly stuck with you{nombre_frase} — thank you for bringing it here instead of letting it just pass.",
            "There's something about this moment you're still holding onto. I'm glad you're telling me.",
        ],
        "neutral": [
            "I hear you. Whatever this is, I'm listening.",
            "Thanks for sharing this with me.",
            f"I'm here{nombre_frase}, whatever this ends up being about.",
            "Take your time with this — there's no rush to make it make sense right away.",
        ],
    }

    # Optional follow-up question that invites the person to go deeper,
    # never forced onto anger — that moment needs room, not more questions
    preguntas = {
        "joy": "What was the best part of it for you?",
        "sadness": "Is there a piece of this you'd like to stay with a little longer?",
        "goal": "What would the very first step toward it look like?",
        "reflection": "What do you think this is trying to tell you?",
        "moment": "What do you think you'll remember most about it?",
        "neutral": "What's sitting with you the most right now?",
    }

    frases_continuidad = [
        "This isn't the first time this has come up today — I'm glad you keep coming back to it with me.",
        "We keep circling back to this, and that's okay. I'm still here for it.",
        "This feels like something asking for more space today. Let's stay with it a little longer.",
    ]

    base = random.choice(respuestas.get(emocion, respuestas["neutral"]))

    # Layer in continuity if the same feeling resurfaced, otherwise sometimes
    # invite the person to go a little deeper into what they just shared
    if continuidad:
        base += " " + random.choice(frases_continuidad)
    elif preguntas.get(emocion) and random.random() < 0.5:
        base += " " + preguntas[emocion]

    return base, emocion


# Chat bubble and floating card styles
st.markdown(
    """
<style>
.chat-container {
    margin-top: 2rem;
}

/* base bubble */
.bubble {
    padding: 0.7rem 1rem;
    border-radius: 1rem;
    margin: 0.3rem 0;
    max-width: 70%;
    font-size: 0.95rem;
}

/* user */
.user-bubble {
    background-color: #3a3a3a;
    margin-left: auto;
    text-align: right;
}

/* Noviembre (bot) by emotion */
.bot-neutral {
    background-color: #2f3136;
}

.bot-joy {
    background-color: #f7d34a;
    color: #000000;
}

.bot-sadness {
    background-color: #1f3b57;
}

.bot-anger {
    background-color: #5c1f1f;
}

.bot-reflection {
    background-color: #b96b2c;
}

.bot-goal {
    background-color: #276749;
}

.bot-moment {
    background-color: #553c9a;
}

/* floating card (for future reminders / suggestions) */
.floating-card {
    margin-top: 1rem;
    padding: 0.8rem 1rem;
    border-radius: 0.8rem;
    background-color: #202225;
    border: 1px solid #444;
    font-size: 0.9rem;
}
</style>
""",
    unsafe_allow_html=True,
)


def mostrar_burbuja(texto: str, role: str, emocion: str = "neutral"):
    """Render a single chat bubble styled by role and emotion."""
    if role == "user":
        css_class = "bubble user-bubble"
    else:
        css_class = f"bubble bot-{emocion}"
    st.markdown(f"<div class='{css_class}'>{texto}</div>", unsafe_allow_html=True)


# Ask for the user's name first if we don't have it yet
if st.session_state["nombre"] is None:

    # Neutral welcome header
    st.markdown(
        """
        <div style='text-align:center; margin-top: 3rem;'>
            <span style='font-size:3rem;'>🟣</span>
            <span style='font-size:3rem; font-weight:700; margin-left:0.4rem;'>Noviembre</span>
            <p style='margin-top:0.5rem; color:#cccccc;'>Welcome. Before we begin, what's your name?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("nombre_form"):
        nombre_input = st.text_input("What's your name?")
        continuar = st.form_submit_button("Continue")

    if continuar and nombre_input.strip():
        st.session_state["nombre"] = nombre_input.strip().title()
        st.rerun()

    st.stop()

# Render the header and chat history once the name is known
nombre = st.session_state["nombre"]
icono_actual = st.session_state["logo_icon"]

subtitle = f"{nombre}, it's good to see you again. How was your day?"

st.markdown(
    f"""
    <div style='text-align:center; margin-top: 2rem;'>
        <span style='font-size:3rem;'>{icono_actual}</span>
        <span style='font-size:3rem; font-weight:700; margin-left:0.4rem;'>Noviembre</span>
        <p style='margin-top:0.5rem; color:#cccccc;'>{subtitle}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Replay the full chat history as bubbles
for msg in st.session_state["chat"]:
    if msg["role"] == "user":
        mostrar_burbuja(msg["text"], "user")
    else:
        mostrar_burbuja(msg["text"], "bot", msg.get("emotion", "neutral"))

st.markdown("</div>", unsafe_allow_html=True)

# Message input
with st.form("chat_form", clear_on_submit=True):
    texto_usuario = st.text_input(
        label="",
        placeholder="Write here whatever you'd like to share...",
        label_visibility="collapsed",
    )
    enviado = st.form_submit_button("➤")

# Append the user turn, detect the reply and icon, then rerun
if enviado and texto_usuario.strip():
    contenido = texto_usuario.strip()

    # Log the user's message in the session chat history
    st.session_state["chat"].append(
        {"role": "user", "text": contenido, "emotion": None}
    )

    st.session_state["turnos_usuario"] += 1

    # Detect the emotion and update the header icon color
    emocion_detectada = detectar_emocion(contenido)
    st.session_state["logo_icon"] = emocion_a_icono(emocion_detectada)

    # Check whether the same feeling is resurfacing within this chat session
    continuidad = (
        st.session_state["turnos_usuario"] > 1
        and st.session_state["last_emotion"] == emocion_detectada
    )
    st.session_state["last_emotion"] = emocion_detectada

    # Build Noviembre's reply for this turn
    respuesta, emocion_respuesta = construir_respuesta(
        contenido,
        nombre,
        emocion_detectada,
        st.session_state["turnos_usuario"],
        continuidad,
    )

    # Log Noviembre's reply in the session chat history
    st.session_state["chat"].append(
        {
            "role": "bot",
            "text": respuesta,
            "emotion": emocion_respuesta,
        }
    )

    # Persist this turn to SQLite and to the JSON memory
    insertar("chat", contenido, respuesta)
    append_entry(
        {
            "section": "chat",
            "text": contenido,
            "detected_emotion": emocion_detectada,
            "reply": respuesta,
            "reply_emotion": emocion_respuesta,
            "tags": [],
            "mode": "normal",
        }
    )

    # Rerun to display the new messages
    st.rerun()