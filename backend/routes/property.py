from flask import Blueprint, request, jsonify
from db import get_db_connection, BASE_DIR
import os
from werkzeug.utils import secure_filename

property_bp = Blueprint('property', __name__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# 🏠 ADD PROPERTY (MULTIPLE IMAGES + FIXED DB LOCK)
# =========================
@property_bp.route('/add-property', methods=['POST'])
def add_property():
    title = request.form.get('title')
    location = request.form.get('location')
    price_raw = request.form.get('price')

    if not price_raw:
        return jsonify({"error": "Price is required"}), 400

    try:
        price = int(price_raw)
    except:
        return jsonify({"error": "Invalid price"}), 400

    property_type = request.form.get('type')
    description = request.form.get('description')
    owner_id = request.form.get('owner_id')

    images = request.files.getlist('images')

    # ✅ STEP 1: SAVE IMAGES FIRST (NO DB)
    image_urls = []

    for image in images:
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)

            file_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(file_path)

            image_url = f"http://127.0.0.1:5000/uploads/{filename}"
            image_urls.append(image_url)

    # ✅ STEP 2: DB OPERATIONS
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
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

        cursor.execute(
            '''
            INSERT INTO properties (title, location, price, type, description, owner_id, fraud_flag)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (title, location, price, property_type, description, owner_id, fraud_flag)
        )

        property_id = cursor.lastrowid

        for url in image_urls:
            cursor.execute(
                "INSERT INTO property_images (property_id, image_url) VALUES (?, ?)",
                (property_id, url)
            )

        conn.commit()

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)})

    finally:
        conn.close()

    return jsonify({
        "message": "Property added successfully",
        "images": image_urls
    })


# =========================
# 📋 GET PROPERTIES
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

        cursor.execute(
            "SELECT is_verified, trust_score FROM users WHERE id=?",
            (row['owner_id'],)
        )
        owner = cursor.fetchone()

        item['is_verified'] = owner['is_verified'] if owner else 0
        item['trust_score'] = owner['trust_score'] if owner else 0

        cursor.execute(
            "SELECT image_url FROM property_images WHERE property_id=?",
            (row['id'],)
        )

        item['images'] = [img['image_url'] for img in cursor.fetchall()]

        result.append(item)

    conn.close()
    return jsonify(result)


# =========================
# 🔍 SEARCH
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

    final = []

    for row in results:
        item = dict(row)

        cursor.execute(
            "SELECT image_url FROM property_images WHERE property_id=?",
            (row['id'],)
        )

        item['images'] = [img['image_url'] for img in cursor.fetchall()]

        final.append(item)

    conn.close()
    return jsonify(final)