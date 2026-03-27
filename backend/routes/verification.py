from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from db import get_db_connection, BASE_DIR
from db import BASE_DIR

# ✅ Blueprint (VERY IMPORTANT)
verification_bp = Blueprint('verification', __name__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# =========================
# 📤 Upload Documents
# =========================
@verification_bp.route('/upload-documents', methods=['POST'])
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


# =========================
# 🧑‍💼 Admin Verify User
# =========================
@verification_bp.route('/admin/verify/<int:user_id>', methods=['POST'])
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


# =========================
# 📧 Email Verification
# =========================
@verification_bp.route('/verify-email/<int:user_id>', methods=['POST'])
def verify_email(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET email_verified=1 WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Email verified"})