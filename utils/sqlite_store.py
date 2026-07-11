import sqlite3

DB_NAME = "database.db"


def init_db():
    """Create the registros table if it doesn't exist yet."""
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
    """Insert a new record into the registros table as historial."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO registros (tipo, contenido, extra)
        VALUES (?, ?, ?)
    """, (tipo, contenido, extra))
    conn.commit()
    conn.close()


def leer_todo():
    """Return every stored record ordered from oldest to newest."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM registros ORDER BY fecha ASC")
    data = c.fetchall()
    conn.close()
    return data
