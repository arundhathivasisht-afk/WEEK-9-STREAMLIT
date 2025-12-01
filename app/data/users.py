from app.data.db import connect_database

def get_user_by_username(username):
    """Look up a user record based on their username."""
    conn = connect_database()
    cursor = conn.cursor()

    sql = "SELECT * FROM users WHERE username = ?"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    conn.close()
    return result


def insert_user(username, password_hash, role="user"):
    """Add a new user into the users table."""
    conn = connect_database()
    cursor = conn.cursor()

    insert_sql = (
        "INSERT INTO users (username, password_hash, role) "
        "VALUES (?, ?, ?)"
    )
    cursor.execute(insert_sql, (username, password_hash, role))

    conn.commit()
    conn.close()