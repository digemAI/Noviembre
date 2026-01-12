import json
import os
from datetime import datetime
from pathlib import Path

# Carpeta donde se guarda la memoria
BASE_PATH = "Data"

# Lo que recuerda Noviembre
MEMORY_FILE = os.path.join(BASE_PATH, "noviembre_memory.json")

# Fecha y hora actual en formato texto
def _now():
    return datetime.now().isoformat(timespec="seconds")

# Se asegura de que exista la carpeta Data 
def ensure_storage():
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)

    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"entries": []}, f, indent=2, ensure_ascii=False)

# Memoria actualizada en disco como JSON
def load_memory():
    ensure_storage()
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
# Se guarda memoria en json
def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def backup_if_exists():
    if os.path.exists(MEMORY_FILE):
        backup_name = f"noviembre_memory_backup_{_now().replace(':','-')}.json"
        backup_path = os.path.join(BASE_PATH, backup_name)

        # Copiamos el archivo actual a un backup
        with open(MEMORY_FILE, "r", encoding="utf-8") as src:
            with open(backup_path, "w", encoding="utf-8") as dst:
                dst.write(src.read())

# Entrada a memoria (category, text, mood) con backup previo
def append_entry(category, text, mood=None):
    backup_if_exists()
    data = load_memory()

    entry = {
        "timestamp": _now(),
        "category": category,
        "text": text,
        "mood": mood
    }

 # Agregamos a la lista de recuerdos y guardamos todo de nuevo en el archivo JSON
    data["entries"].append(entry)
    save_memory(data)

# Devolvemos los recuerdos o solo los de una categoría
def get_entries(category=None):
    data = load_memory()
    if category:
        return [e for e in data["entries"] if e["category"] == category]
    return data["entries"]

# Último recuerdo guardado
def get_last_entry():
    data = load_memory()
    if "entries" in data and len(data["entries"]) > 0:
        return data["entries"][-1]
    return None
