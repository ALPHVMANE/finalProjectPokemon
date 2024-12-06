import sqlite3
import os

pokemon_data = [
    (26, 'raichu', 60, 90, 55, 90, 110, 'electric'),
    (6,'charizard', 78, 84, 78, 85, 100, 'fire/flying'),
    (9, 'blastoise', 79, 83, 100, 85, 78, 'water'),
    (150, 'mewtwo', 106, 110, 90, 154, 130, 'psychic'),
    (94, 'gengar', 60, 65, 60, 130, 110, 'ghost/poison'),
    (3, 'venusaur', 80, 82, 83, 100, 80, 'grass/poison')
]
def get_db_conn():
    """Create a database connection and return connection and cursor"""
    conn = sqlite3.connect('poke.db')
    conn.row_factory = sqlite3.Row  # column access by name
    return conn

def init_db():
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trainer_pokemon (
            trainer_id  INTEGER PRIMARY KEY,
            pokemon1    TEXT NOT NULL,
            pokemon2    TEXT NOT NULL,
            pokemon3    TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()