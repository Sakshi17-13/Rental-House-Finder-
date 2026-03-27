from flask import Blueprint, request, jsonify
from db import get_db_connection

property_bp = Blueprint('property', __name__)

# =========================
# 🏠 ADD PROPERTY (with fraud detection)
# =========================
@property_bp.route('/add-property', methods=['POST'])
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

    # 🚨 Fraud Detection
    fraud_flag = 0

    cursor.execute(
        "SELECT AVG(price) as avg_price FROM properties WHERE location=?",
        (location,)
    )
    avg = cursor.fetchone()['avg_price']

    if avg and price < avg * 0.5:
        fraud_flag = 1

    if not description or description.strip() == "":
        fraud_flag = 1

    # Insert property
    cursor.execute(
        '''
        INSERT INTO properties (title, location, price, type, description, owner_id, fraud_flag)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (title, location, price, property_type, description, owner_id, fraud_flag)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Property added successfully"})


# =========================
# 📋 GET PROPERTIES (with verified badge)
# =========================
@property_bp.route('/get-properties', methods=['GET'])
def get_properties():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM properties")
    properties = cursor.fetchall()

    result = []

    for row in properties:
        item = dict(row)

        # 🔥 Add verification badge
        cursor.execute(
            "SELECT is_verified, trust_score FROM users WHERE id=?",
            (row['owner_id'],)
        )
        owner = cursor.fetchone()

        if owner:
            item['is_verified'] = owner['is_verified']
            item['trust_score'] = owner['trust_score']
        else:
            item['is_verified'] = 0
            item['trust_score'] = 0

        result.append(item)

    conn.close()

    return jsonify(result)


# =========================
# 🔍 SEARCH PROPERTIES
# =========================
@property_bp.route('/search', methods=['GET'])
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
