import json
import os
from datetime import datetime
from pathlib import Path

# Folder where persistent memory lives
BASE_PATH = "Data"

# File that holds what Noviembre remembers
MEMORY_FILE = os.path.join(BASE_PATH, "noviembre_memory.json")


def _now():
    """Return the current timestamp as an ISO-formatted string."""
    return datetime.now().isoformat(timespec="seconds")


def ensure_storage():
    """Create the Data folder and memory file if they don't exist."""
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)

    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"entries": []}, f, indent=2, ensure_ascii=False)


def load_memory():
    """Load and return the current memory state from disk."""
    ensure_storage()
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(data):
    """Persist the given memory state to the JSON file on disk."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def backup_if_exists():
    """Back up the current memory file before it gets overwritten."""
    if os.path.exists(MEMORY_FILE):
        backup_name = f"noviembre_memory_backup_{_now().replace(':','-')}.json"
        backup_path = os.path.join(BASE_PATH, backup_name)

        # Copy current file content into a timestamped backup
        with open(MEMORY_FILE, "r", encoding="utf-8") as src:
            with open(backup_path, "w", encoding="utf-8") as dst:
                dst.write(src.read())


def append_entry(entry):
    """Stamp the given entry dict with a timestamp and store it in memory."""
    backup_if_exists()
    data = load_memory()

    # Copy so the caller's dict isn't mutated, then stamp the time
    entry = dict(entry)
    entry["timestamp"] = _now()

    # Add the new entry and persist the full memory back to disk
    data["entries"].append(entry)
    save_memory(data)


def get_entries(section=None):
    """Return all entries, optionally filtered by section."""
    data = load_memory()
    if section:
        return [e for e in data["entries"] if e.get("section") == section]
    return data["entries"]


def get_last_entry():
    """Return the most recently saved memory entry, if any exists."""
    data = load_memory()
    if "entries" in data and len(data["entries"]) > 0:
        return data["entries"][-1]
    return None
