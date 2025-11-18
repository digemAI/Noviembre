import streamlit as st
import random
from utils.db import init_db  # lo dejamos por compatibilidad con las otras páginas

# ------------------ CONFIG BÁSICA ------------------

st.set_page_config(page_title="Noviembre", page_icon="🟣")
init_db()

# ------------------ ESTADO INICIAL ------------------

if "nombre" not in st.session_state:
    st.session_state["nombre"] = None

if "chat" not in st.session_state:
    # cada mensaje: {"role": "user"/"bot", "text": "...", "emotion": "alegria"/"tristeza"/...}
    st.session_state["chat"] = []

if "logo_icon" not in st.session_state:
    st.session_state["logo_icon"] = "🟣"  # neutro

if "turnos_usuario" not in st.session_state:
    st.session_state["turnos_usuario"] = 0

# ------------------ DETECCIÓN SENCILLA DE EMOCIÓN ------------------

def detectar_emocion(texto: str) -> str:
    t = texto.lower()

    palabras_alegria = [
        "feliz", "contento", "contenta", "alegre", "me emociona", "emocionado",
        "emocionada", "me ilusiona", "ilusionado", "ilusionada", "enamorado",
        "enamorada", "me gusta", "me encanta", "gran día", "gran dia", "buen día", "buen dia"
    ]
    palabras_tristeza = [
        "triste", "lloré", "llore", "llorando", "me duele", "muerte", "murió",
        "murio", "perdí", "perdi", "extraño", "extranio", "lo extraño", "la extraño",
        "vacío", "vacio", "nostalgia", "solo", "sola", "soledad"
    ]
    palabras_ira = [
        "enojo", "enojado", "enojada", "odio", "coraje", "harto", "harta",
        "molesto", "molesta", "rabia"
    ]
    palabras_reflexion = [
        "he estado pensando", "he pensado", "me doy cuenta", "creo que",
        "reflexionando", "me puse a pensar"
    ]
    palabras_metas = [
    "quiero lograr",
    "mi objetivo",
    "mi meta",
    "meta es",
    "planeo",
    "planeo hacer",
    "quiero hacer",
    "quiero ganar",
    "quiero ahorrar",
    "pienso ahorrar",
    "de aquí a fin de año",
    "de aqui a fin de año",
    "de aqui a fin de mes",
    "ahorrar 100 mil",
    "hacer 100 mil",
    "juntar 100 mil",
    "ahorrar cien mil",
    ]
    palabras_momento = [
        "hoy pasó", "hoy paso", "ayer fue", "me marcó", "me marco",
        "me sorprendió", "me sorprendio", "pasó algo", "paso algo"
    ]

    # prioridad de detección
    for w in palabras_ira:
        if w in t:
            return "ira"
    for w in palabras_tristeza:
        if w in t:
            return "tristeza"
    for w in palabras_alegria:
        if w in t:
            return "alegria"
    for w in palabras_metas:
        if w in t:
            return "meta"
    for w in palabras_reflexion:
        if w in t:
            return "reflexion"
    for w in palabras_momento:
        if w in t:
            return "momento"

    return "neutral"


def emocion_a_icono(emocion: str) -> str:
    mapa = {
        "alegria": "🟡",
        "tristeza": "🔵",
        "ira": "🔴",
        "reflexion": "🟠",
        "meta": "🟢",
        "momento": "🟣",   # momento importante / recuerdo
        "neutral": "🟣"
    }
    return mapa.get(emocion, "🟣")


# ------------------ RESPUESTAS HUMANAS ------------------

def construir_respuesta(texto_usuario: str, nombre: str, emocion: str, turno: int):
    # Primer mensaje: abrir espacio
    if turno == 1:
        if nombre:
            return (
                f"¿Quieres contarme un poco más sobre eso, {nombre}? "
                "Podemos irlo desmenuzando sin prisa.",
                "neutral",
            )
        else:
            return (
                "¿Quieres contarme un poco más sobre eso? "
                "Podemos irlo desmenuzando sin prisa.",
                "neutral",
            )

    # Alegría / enamoramiento
    if emocion == "alegria":
        opciones = [
            "Suena a que algo bonito pasó hoy. Me da gusto por ti. "
            "Si quieres seguimos hablando de eso, o me puedes contar qué fue lo que más te gustó del momento.",
            "Se siente mucha luz en lo que escribes. "
            "Si te nace, cuéntame un detalle que quieras guardar de este día.",
        ]
        return random.choice(opciones), "alegria"

    # Tristeza / nostalgia
    if emocion == "tristeza":
        opciones = [
            "Lo que me cuentas se siente pesado, como algo que todavía duele. "
            "No estás solo en esto, aunque sea a través de una pantalla. "
            "Si te ayuda, podemos ir hablando de a pedacitos.",
            "Parece que esto te toca profundo. "
            "Podemos quedarnos aquí un rato, sin prisa, si quieres seguir contándolo.",
        ]
        return random.choice(opciones), "tristeza"

    # Ira – solo contener, no sugerir guardar
    if emocion == "ira":
        opciones = [
            "Se nota que esto te molesta bastante. Es válido sentirlo. "
            "Si quieres, podemos ir sacando el enojo poco a poco para que no se quede atorado.",
            "Suena a que fue un momento muy frustrante. "
            "Puedes soltarlo aquí sin filtros si eso te ayuda.",
        ]
        return random.choice(opciones), "ira"

    # Metas / objetivos
    if emocion == "meta":
        opciones = [
            "Eso que dices suena a una meta importante para ti. "
            "Podemos irla bajando a pasos pequeños si te late.",
            "Me gusta cómo lo planteas, se siente como un objetivo claro. "
            "¿Te gustaría desmenuzarlo en pasos sencillos?",
        ]
        return random.choice(opciones), "meta"

    # Reflexiones
    if emocion == "reflexion":
        opciones = [
            "Me gusta cómo lo estás mirando, se nota que has estado pensando en esto. "
            "Si quieres seguimos profundizando un poco más.",
            "Eso que escribes suena a una buena reflexión. "
            "Podemos intentar poner en palabras qué te estás llevando de todo esto.",
        ]
        return random.choice(opciones), "reflexion"

    # Momentos importantes
    if emocion == "momento":
        opciones = [
            "Parece que lo que pasó dejó marca en tu día. "
            "Si quieres, podemos detenernos en ese momento y verlo con más calma.",
            "Suena a uno de esos momentos que se quedan dando vueltas en la cabeza. "
            "Si te ayuda, cuéntame qué fue lo que más te movió.",
        ]
        return random.choice(opciones), "momento"

    # Neutro / sin categoría clara
    opciones = [
        "Te leo. Si quieres, dime un poco más para entender mejor lo que estás viviendo.",
        "Gracias por compartirlo. Si te nace, podemos ir profundizando un poquito más.",
    ]
    return random.choice(opciones), "neutral"


# ------------------ ESTILOS (Burbujas y tarjeta flotante) ------------------

st.markdown(
    """
<style>
.chat-container {
    margin-top: 2rem;
}

/* burbuja base */
.bubble {
    padding: 0.7rem 1rem;
    border-radius: 1rem;
    margin: 0.3rem 0;
    max-width: 70%;
    font-size: 0.95rem;
}

/* usuario */
.user-bubble {
    background-color: #3a3a3a;
    margin-left: auto;
    text-align: right;
}

/* Noviembre (bot) por emoción */
.bot-neutral {
    background-color: #2f3136;
}

.bot-alegria {
    background-color: #f7d34a;
    color: #000000;
}

.bot-tristeza {
    background-color: #1f3b57;
}

.bot-ira {
    background-color: #5c1f1f;
}

.bot-reflexion {
    background-color: #b96b2c;
}

.bot-meta {
    background-color: #276749;
}

.bot-momento {
    background-color: #553c9a;
}

/* tarjeta flotante (para futuros recordatorios / sugerencias) */
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
    if role == "user":
        css_class = "bubble user-bubble"
    else:
        css_class = f"bubble bot-{emocion}"
    st.markdown(f"<div class='{css_class}'>{texto}</div>", unsafe_allow_html=True)


# ------------------ PANTALLA: PREGUNTAR NOMBRE ------------------

if st.session_state["nombre"] is None:
    # encabezado neutro
    st.markdown(
        """
        <div style='text-align:center; margin-top: 3rem;'>
            <span style='font-size:3rem;'>🟣</span>
            <span style='font-size:3rem; font-weight:700; margin-left:0.4rem;'>Noviembre</span>
            <p style='margin-top:0.5rem; color:#cccccc;'>Bienvenido. Antes de empezar, ¿cómo te llamas?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("nombre_form"):
        nombre_input = st.text_input("¿Cómo te llamas?")
        continuar = st.form_submit_button("Continuar")

    if continuar and nombre_input.strip():
        st.session_state["nombre"] = nombre_input.strip().title()
        st.rerun()

    st.stop()

# ------------------ PANTALLA PRINCIPAL DE CHAT ------------------

nombre = st.session_state["nombre"]
icono_actual = st.session_state["logo_icon"]

subtitle = f"{nombre}, me alegra verte de nuevo por aquí. ¿Cómo estuvo tu día?"

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

# historial de mensajes
for msg in st.session_state["chat"]:
    if msg["role"] == "user":
        mostrar_burbuja(msg["text"], "user")
    else:
        mostrar_burbuja(msg["text"], "bot", msg.get("emotion", "neutral"))

st.markdown("</div>", unsafe_allow_html=True)

# ------------------ FORMULARIO DE ENTRADA (ENTER = enviar) ------------------

with st.form("chat_form", clear_on_submit=True):
    texto_usuario = st.text_input(
        label="",
        placeholder="Escribe aquí lo que quieras compartir...",
        label_visibility="collapsed",
    )
    enviado = st.form_submit_button("➤")

if enviado and texto_usuario.strip():
    contenido = texto_usuario.strip()

    # guardamos mensaje del usuario en el historial (solo en sesión)
    st.session_state["chat"].append(
        {"role": "user", "text": contenido, "emotion": None}
    )

    st.session_state["turnos_usuario"] += 1

    # detectar emoción e actualizar color del puntito
    emocion_detectada = detectar_emocion(contenido)
    st.session_state["logo_icon"] = emocion_a_icono(emocion_detectada)

    # construir respuesta humana
    respuesta, emocion_respuesta = construir_respuesta(
        contenido,
        nombre,
        emocion_detectada,
        st.session_state["turnos_usuario"],
    )

    # añadimos respuesta de Noviembre
    st.session_state["chat"].append(
        {
            "role": "bot",
            "text": respuesta,
            "emotion": emocion_respuesta,
        }
    )

    # recargar para ver el nuevo mensaje
    st.rerun()



