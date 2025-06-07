import sqlite3
import os

DATABASE_FILE = "psych_assistant_mvp.db"

def connect_db():
    """Connects to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
    return conn

def create_tables():
    """Creates the necessary database tables if they don't exist."""
    conn = connect_db()
    cursor = conn.cursor()

    # Create patients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE NOT NULL,
        name TEXT, -- Optional for MVP, but useful
        condition TEXT, -- Simplified description
        medication TEXT -- Simplified description
    );
    """)

    # Create mood_history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mood_history (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        mood_scale INTEGER, -- e.g., 1-5 scale
        mood_description TEXT, -- User's text description
        sentiment_analysis TEXT, -- Result from LLM (e.g., 'Positive', 'Negative', 'Neutral')
        FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
    );
    """)

    conn.commit()
    conn.close()
    print(f"Database tables checked/created in {DATABASE_FILE}")

if __name__ == "__main__":
    # Ensure the database file is created in the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    create_tables()

