import sqlite3
import os

def create_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, '..', 'database', 'rental.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # =========================
    # USERS TABLE
    # =========================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        is_verified INTEGER DEFAULT 0,
        trust_score INTEGER DEFAULT 0,
        email_verified INTEGER DEFAULT 0
    )
    ''')

    # =========================
    # PROPERTIES TABLE
    # =========================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        location TEXT,
        price INTEGER,
        type TEXT,
        description TEXT,
        owner_id INTEGER,
        fraud_flag INTEGER DEFAULT 0
    )
    ''')

    # =========================
    # FAVORITES TABLE
    # =========================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        property_id INTEGER
    )
    ''')

    # =========================
    # VERIFICATION DOCUMENTS
    # =========================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS verification_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        id_proof TEXT,
        property_proof TEXT,
        status TEXT DEFAULT 'pending'
    )
    ''')

    # =========================
    # COMPLAINTS TABLE
    # =========================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        property_id INTEGER,
        reason TEXT
    )
    ''')

    # =========================
    # INSERT SAMPLE DATA (SAFE)
    # =========================
    cursor.execute("SELECT COUNT(*) FROM properties")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''
        INSERT INTO properties (title, location, price, type, description, owner_id)
        VALUES
        ('1BHK in Wakad', 'Wakad', 15000, '1BHK', 'Near IT park', 1),
        ('2BHK in Hinjewadi', 'Hinjewadi', 22000, '2BHK', 'Spacious flat', 2),
        ('1BHK in Baner', 'Baner', 18000, '1BHK', 'Fully furnished', 1)
        ''')

    conn.commit()
    conn.close()

    print("✅ Database with verification system created successfully")

if __name__ == "__main__":
    create_db()