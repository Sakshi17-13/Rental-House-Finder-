import sqlite3

def create_db():
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, '..', 'database', 'rental.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    ''')

    # Properties Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        location TEXT,
        price INTEGER,
        type TEXT,
        description TEXT,
        owner_id INTEGER
    )
    ''')

    # Favorites Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        property_id INTEGER
    )
    ''')
    # Insert sample properties
    cursor.execute('''
    INSERT INTO properties (title, location, price, type, description, owner_id)
    VALUES
    ('1BHK in Wakad', 'Wakad', 15000, '1BHK', 'Near IT park', 1),
    ('2BHK in Hinjewadi', 'Hinjewadi', 22000, '2BHK', 'Spacious flat', 2),
    ('1BHK in Baner', 'Baner', 18000, '1BHK', 'Fully furnished', 1)
    ''')
    conn.commit()
    conn.close()
    print("✅ Database & tables created successfully")

if __name__ == "__main__":
    create_db()
