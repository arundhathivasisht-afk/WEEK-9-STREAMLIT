import sqlite3
import bcrypt
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user

def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    existing = get_user_by_username(username)
    if existing:
        return False, f"Username '{username}' already exists."

    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    stored_hash = user[2]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful!"
    return False, "Incorrect password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from text file into SQLite database."""
    conn = connect_database()
    cursor = conn.cursor()
    migrated = 0

    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(',')
                username = parts[0]
                password_hash = parts[1]
                role = parts[2] if len(parts) > 2 else 'user'

                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, role)
                    )
                    if cursor.rowcount > 0:
                        migrated += 1
                except sqlite3.Error as e:
                    print(f"Error migrating {username}: {e}")

        conn.commit()
        print(f"Migrated {migrated} users from {filepath}")
    finally:
        conn.close()

    return migrated