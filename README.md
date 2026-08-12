# Noviembre

An emotional journaling companion built with Streamlit — it listens, remembers, and helps the user understand what they're going through, one entry at a time.
---

## The problem

Not everyone has someone who's always there — someone to tell everything to, who sticks around through the good moments and the hard ones, and who actually helps you get closer to what you're working toward. Most journaling apps just store text. They don't feel like anyone is listening.

---

## What it does today

- **Structured journaling** across four entry types — emotions, reflections, goals, and important moments — each with its own guided prompts and a warm, non-generic response.

- **Freeform conversational chat** with lightweight keyword-based emotion detection (joy, sadness, anger, reflection, goal, moment) that adapts the reply and the UI's color accent in real time. Replies vary by emotion, occasionally invite the person to go deeper, and recognize when the same feeling resurfaces within a conversation instead of resetting each turn.

- **Persistent memory on two layers**: every entry is written to SQLite as a flat history log, and to a structured JSON memory file with timestamps and categories — the app remembers across sessions, not just within one.
- A calm, consistent visual identity (color-coded chat bubbles per detected emotion, minimal UI) that reinforces the product's tone: presence over productivity.

- A **browsable History** view that groups everything you've shared by day and lets you filter by type (emotions, reflections, goals, moments, chat) — so loose entries read like a personal timeline instead of something you have to dig through.

---

## Where it's going

**V3 of 9.** I gave it a way to look back — because a friend who forgets
everything you've told them isn't a friend, they're a stranger with good manners.

---


## Why I built it

I built Noviembre to be that presence: not a tool you use, but a friend you open up to because you *want* to talk to them.