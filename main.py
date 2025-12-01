from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
from app.data.datasets import load_all_csv_data


def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # 2. Migrate users from users.txt
    migrate_users_from_file()

    # 3. Load CSV data (new)
    load_all_csv_data()

    # 4. Test user registration
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)

    # 5. Test login
    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    # 6. Test inserting an incident
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    # 7. Test reading incidents
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")


if __name__ == "__main__":
    main()
