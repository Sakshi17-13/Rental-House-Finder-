from app import get_db_connection

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