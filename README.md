Noviembre

An emotional journaling companion built with Streamlit — it listens, remembers, and helps the user understand what they're going through, one entry at a time.

What it does today


Structured journaling across four entry types — emotions, reflections, goals, and important moments — each with its own guided prompts and a warm, non-generic response.

Freeform conversational chat with lightweight keyword-based emotion detection (joy, sadness, anger, reflection, goal, moment) that adapts the reply and the UI's color accent in real time.

Persistent memory on two layers: every entry is written to SQLite as a flat history log, and to a structured JSON memory file with timestamps and categories — the app remembers across sessions, not just within one.

A calm, consistent visual identity (color-coded chat bubbles per detected emotion, minimal UI) that reinforces the product's tone: presence over productivity.


Where it's going

This is V1 of a 9-stage roadmap — the foundation, not the finished product. Noviembre is under active development: future versions deepen the conversational tone, add real pattern recognition across entries, and move from keyword matching toward genuine NLP-based interpretation, while staying true to what it's meant to be — presence, not productivity.

Architecture

Nov.py                 # Main chat screen — keyword-based emotion detection, conversational replies
pages/
  1_Emotions.py          # Structured emotion entry
  2_Reflections.py       # Structured reflection entry
  3_Goals.py              # Goal entry with target date
  4_Moments.py             # Important-moment entry with impact rating
utils/
  sqlite_store.py       # SQLite persistence layer
  nov_memory.py          # JSON-based long-term memory (append_entry, get_entries, get_last_entry)