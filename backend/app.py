from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_db_connection, BASE_DIR
from werkzeug.utils import secure_filename
from routes.verification import verification_bp
from routes.property import property_bp
import os
app = Flask(__name__)
CORS(app)

# Database Path Setup
#db_path = os.path.join(BASE_DIR, 'database', 'rental.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

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
# 🏠 ADD FAVORITE
# =========================

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

@app.route('/upload-documents', methods=['POST'])
def upload_documents():
    user_id = request.form.get('user_id')

    id_file = request.files['id_proof']
    property_file = request.files['property_proof']

    id_filename = secure_filename(id_file.filename)
    property_filename = secure_filename(property_file.filename)

    id_path = os.path.join(UPLOAD_FOLDER, 'id_proofs', id_filename)
    property_path = os.path.join(UPLOAD_FOLDER, 'property_proofs', property_filename)

    id_file.save(id_path)
    property_file.save(property_path)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO verification_documents (user_id, id_proof, property_proof)
        VALUES (?, ?, ?)
    ''', (user_id, id_path, property_path))

    conn.commit()
    conn.close()

    return jsonify({"message": "Documents uploaded. Pending approval"})

@app.route('/admin/verify/<int:user_id>', methods=['POST'])
def admin_verify(user_id):
    status = request.json.get('status')  # approved / rejected

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE verification_documents SET status=? WHERE user_id=?",
        (status, user_id)
    )

    if status == "approved":
        cursor.execute(
            "UPDATE users SET is_verified=1 WHERE id=?",
            (user_id,)
        )

    conn.commit()
    conn.close()

    return jsonify({"message": f"User {status}"})

def update_trust_score(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    score = 0

    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    if user['is_verified']:
        score += 40

    if user['email_verified']:
        score += 20

    cursor.execute("SELECT COUNT(*) as count FROM complaints WHERE user_id=?", (user_id,))
    complaints = cursor.fetchone()['count']

    if complaints == 0:
        score += 20
    else:
        score -= 30

    cursor.execute(
        "UPDATE users SET trust_score=? WHERE id=?",
        (score, user_id)
    )

    conn.commit()
    conn.close()

@app.route('/verify-email/<int:user_id>', methods=['POST'])
def verify_email(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET email_verified=1 WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    update_trust_score(user_id)

    return jsonify({"message": "Email verified"})

app.register_blueprint(verification_bp)
app.register_blueprint(property_bp)
# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == '__main__':
    app.run(debug=True)