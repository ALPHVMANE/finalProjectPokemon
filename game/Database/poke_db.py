import sqlite3
import os

def get_db_conn():
    """Create a database connection and return connection and cursor"""
    conn = sqlite3.connect('poke.db')
    conn.row_factory = sqlite3.Row  # column access by name
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trainer_pokemon (
            trainer_id INTEGER PRIMARY KEY,
            pokemon1 TEXT NOT NULL,
            pokemon2 TEXT NOT NULL,
            pokemon3 TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()