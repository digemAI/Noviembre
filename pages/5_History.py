import streamlit as st
from utils.nov_memory import get_entries

# Page title
st.title("🗂️ History")

st.write("Look back at what you've shared with Noviembre, organized the way you want to read it.")

# Let the person choose which kind of entry they want to revisit
filtro = st.selectbox(
    "What would you like to revisit?",
    ["Everything", "Emotions", "Reflections", "Goals", "Moments", "Chat"],
)

mapa_filtro = {
    "Everything": None,
    "Emotions": "emotions",
    "Reflections": "reflections",
    "Goals": "goals",
    "Moments": "moments",
    "Chat": "chat",
}

section = mapa_filtro[filtro]
entradas = get_entries(section)

# Show the most recent entries first so it's easy to pick up where you left off
entradas = sorted(entradas, key=lambda e: e.get("timestamp", ""), reverse=True)

if not entradas:
    st.info("Nothing here yet — once you start writing, it'll show up in this timeline.")
else:
    ultimo_dia = None
    for entrada in entradas:
        timestamp = entrada.get("timestamp", "")
        fecha = timestamp.split("T")[0] if "T" in timestamp else timestamp
        hora = timestamp.split("T")[1] if "T" in timestamp else ""

        # Group entries under a date header whenever the day changes,
        # so loose memories read as a personal timeline instead of a flat list
        if fecha != ultimo_dia:
            st.subheader(fecha)
            ultimo_dia = fecha

        etiqueta_seccion = entrada.get("section", "entry").capitalize()
    
        texto = entrada.get("text", "")
        if not isinstance(texto, str):
            texto = str(texto)
        texto = texto.strip()

        with st.container():
            st.markdown(f"**{etiqueta_seccion}** · {hora}")
            st.write(texto)

            # Surface whatever extra context this entry was saved with,
            # so the reader connects the feeling to what was going on
            emocion = entrada.get("detected_emotion") or entrada.get("mood")
            tags = entrada.get("tags")
            importancia = entrada.get("importance")

            detalles = []
            if emocion:
                detalles.append(f"feeling: {emocion}")
            if tags:
                detalles.append(f"tags: {', '.join(tags)}")
            if importancia is not None:
                detalles.append(f"importance: {importancia}/10")

            if detalles:
                st.caption(" · ".join(detalles))

            st.divider()