from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Database Path Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'database', 'rental.db')

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Home Route
@app.route('/')
def home():
    return "✅ Backend is running"

# =========================
# 🔐 REGISTER API
# =========================
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"})
    
    except:
        return jsonify({"error": "User already exists"})
    
    finally:
        conn.close()

# =========================
# 🔑 LOGIN API
# =========================
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        })
    else:
        return jsonify({"error": "Invalid credentials"})

# =========================
# 🏠 ADD PROPERTY
# =========================
@app.route('/add-property', methods=['POST'])
def add_property():
    data = request.json

    title = data.get('title')
    location = data.get('location')
    price = data.get('price')
    property_type = data.get('type')
    description = data.get('description')
    owner_id = data.get('owner_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO properties (title, location, price, type, description, owner_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (title, location, price, property_type, description, owner_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Property added successfully"})

# =========================
# 📋 GET ALL PROPERTIES
# =========================
@app.route('/get-properties', methods=['GET'])
def get_properties():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM properties")
    properties = cursor.fetchall()

    conn.close()

    result = [dict(row) for row in properties]

    return jsonify(result)

# =========================
# 🔍 SEARCH PROPERTIES
# =========================
@app.route('/search', methods=['GET'])
def search_properties():
    location = request.args.get('location')
    property_type = request.args.get('type')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM properties WHERE 1=1"
    params = []

    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")

    if property_type:
        query += " AND type=?"
        params.append(property_type)

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in results])

@app.route('/add-favorite', methods=['POST'])
def add_favorite():
    data = request.json

    user_id = data.get('user_id')
    property_id = data.get('property_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO favorites (user_id, property_id) VALUES (?, ?)",
        (user_id, property_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Added to favorites"})

@app.route('/get-favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT properties.* FROM properties
        JOIN favorites ON properties.id = favorites.property_id
        WHERE favorites.user_id = ?
    ''', (user_id,))

    results = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in results])

@app.route('/analytics', methods=['GET'])
def analytics():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT location, AVG(price) as avg_price FROM properties GROUP BY location")
    data = cursor.fetchall()

    conn.close()

    result = [dict(row) for row in data]

    return jsonify(result)

@app.route('/recommend/<int:property_id>', methods=['GET'])
def recommend(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get selected property
    cursor.execute("SELECT * FROM properties WHERE id=?", (property_id,))
    prop = cursor.fetchone()

    if not prop:
        return jsonify({"error": "Property not found"})

    # Find similar
    cursor.execute('''
        SELECT * FROM properties
        WHERE type=? AND price BETWEEN ? AND ? AND id != ?
    ''', (
        prop['type'],
        prop['price'] - 5000,
        prop['price'] + 5000,
        property_id
    ))

    results = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in results])

@app.route('/budget', methods=['POST'])
def budget():
    data = request.json
    salary = data.get('salary')

    recommended_rent = int(salary * 0.3)

    # 🔥 NEW PART (add this)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM properties WHERE price <= ?",
        (recommended_rent,)
    )

    houses = cursor.fetchall()
    conn.close()

    return jsonify({
        "salary": salary,
        "recommended_rent": recommended_rent,
        "suggested_houses": [dict(row) for row in houses]
    })
# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == '__main__':
    app.run(debug=True)