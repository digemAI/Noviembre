import sqlite3

DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            contenido TEXT,
            extra TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insertar(tipo, contenido, extra=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO registros (tipo, contenido, extra)
        VALUES (?, ?, ?)
    """, (tipo, contenido, extra))
    conn.commit()
    conn.close()

def leer_todo():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM registros ORDER BY fecha ASC")
    data = c.fetchall()
    conn.close()
    return data
