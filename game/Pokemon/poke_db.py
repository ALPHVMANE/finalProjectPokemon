import os
from dotenv import load_dotenv #https://pypi.org/project/python-dotenv/
from cryptography.fernet import Fernet
import sqlite3

pokemon_stats = [
    (26, 'raichu', 60, 90, 55, 90, 110, 'electric'),
    (6,'charizard', 78, 84, 78, 85, 100, 'fire/flying'),
    (9, 'blastoise', 79, 83, 100, 85, 78, 'water'),
    (150, 'mewtwo', 106, 110, 90, 154, 130, 'psychic'),
    (94, 'gengar', 60, 65, 60, 130, 110, 'ghost/poison'),
    (3, 'venusaur', 80, 82, 83, 100, 80, 'grass/poison')
]

# Load the encryption key from .env
load_dotenv()
encryption_key = os.getenv('ENCRYPTION_KEY')

# If no key exists, generate one and save it (do this once)
if not encryption_key:
    encryption_key = Fernet.generate_key()
    with open('.env', 'w') as f:
        f.write(f'ENCRYPTION_KEY={encryption_key.decode()}')
        fernet = Fernet(encryption_key)
else:
    # Create Fernet instance
    fernet = Fernet(encryption_key.encode())

conn = sqlite3.connect('poke.db')
cursor = conn.cursor()

#Create db
def get_db_conn():
    conn = sqlite3.connect('poke.db')
    conn.row_factory = sqlite3.Row  # column access by name
    return conn

def init_db():
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS trainer_pokemon')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS trainer_pokemon (
                    trainer_id      INTEGER PRIMARY KEY,
                    encrypted_ssn   TEXT NOT NULL,
                    pokemon1        TEXT NOT NULL,
                    pokemon2        TEXT NOT NULL,
                    pokemon3        TEXT NOT NULL
                )
            ''')
        conn.commit()

        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def encrypt_data(data: str) -> str:
    """Encrypt a string"""
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt an encrypted string"""
    return fernet.decrypt(encrypted_data.encode()).decode()


def add_trainer(trainer_id: int, ssn: str, pokemon_list: list):
    if len(pokemon_list) != 3:
        return False

    conn = get_db_conn()
    cursor = conn.cursor()

    encrypted_ssn = encrypt_data(ssn)

    cursor.execute('''
        INSERT OR REPLACE INTO trainer_pokemon 
        (trainer_id, encrypted_ssn, pokemon1, pokemon2, pokemon3)
        VALUES (?, ?, ?, ?, ?)
    ''', (trainer_id, encrypted_ssn, pokemon_list[0], pokemon_list[1], pokemon_list[2]))

    conn.commit()
    conn.close()


def get_trainer(trainer_id: int) -> dict:
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM trainer_pokemon WHERE trainer_id = ?', (trainer_id,))
    trainer = cursor.fetchone()
    conn.close()

    if trainer:
        return {
            'trainer_id': trainer['trainer_id'],
            'pokemon_list': [trainer['pokemon1'], trainer['pokemon2'], trainer['pokemon3']],
            'ssn': decrypt_data(trainer['encrypted_ssn'])
        }
    return None

# if __name__ == "__main__":
#     # Initialize the database
#     init_db()
#
#     if not encryption_key:
#         print("Warning: No encryption key found in .env file")
#
#
#     conn = get_db_conn()
#     cursor = conn.cursor()
#
#     # Demo: Add some trainers with consistently encrypted SSNs using the key from .env
#     demo_trainers = [
#         ("123-45-6789", "Raichu", "Charizard", "Blastoise"),
#         ("987-65-4321", "Mewtwo", "Gengar", "Venusaur"),
#         ("456-78-9012", "Charizard", "Mewtwo", "Gengar")
#     ]
#
#     # Clear existing trainer data for demo
#     cursor.execute('DELETE FROM trainer_pokemon')
#
#     # Insert demo trainers with encrypted SSNs using the existing encryption key
#     for ssn, pokemon1, pokemon2, pokemon3 in demo_trainers:
#         # Use the fernet instance initialized with the .env key
#         encrypted_ssn = encrypt_data(ssn)
#         cursor.execute('''
#             INSERT INTO trainer_pokemon (encrypted_ssn, pokemon1, pokemon2, pokemon3)
#             VALUES (?, ?, ?, ?)
#         ''', (encrypted_ssn, pokemon1, pokemon2, pokemon3))
#
#     # Demo: Query and display trainer data
#     print("\n=== Pokemon Trainer Database Demo ===\n")
#
#     # Display trainer information
#     print("All Trainer Information:")
#     cursor.execute('SELECT * FROM trainer_pokemon')
#     for trainer in cursor.fetchall():
#         decrypted_ssn = decrypt_data(trainer['encrypted_ssn'])
#         print(f"\nTrainer ID: {trainer['trainer_id']}")
#         print(f"SSN (decrypted): {decrypted_ssn}")
#         print(f"SSN (encrypted): {trainer['encrypted_ssn']}")
#         print(f"Pokemon Team: {trainer['pokemon1']}, {trainer['pokemon2']}, {trainer['pokemon3']}")
#
#     conn.commit()
#     conn.close()