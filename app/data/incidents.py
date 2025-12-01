import pandas as pd
from app.data.db import connect_database


def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """Insert a new cyber incident."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))

    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id


def get_all_incidents():
    """Return all cyber incidents as a DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)
    conn.close()
    return df


# ============================
#   UPDATE INCIDENT STATUS
# ============================
def update_incident_status(incident_id, new_status):
    """Update the status of an incident."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )

    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated


# ============================
#        DELETE INCIDENT
# ============================
def delete_incident(incident_id):
    """Delete an incident from the database."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()

    deleted = cursor.rowcount
    conn.close()
    return deleted


# ============================
#     ANALYTICAL QUERIES
# ============================
def get_incidents_by_type_count():
    """Count incidents grouped by type."""
    conn = connect_database()
    df = pd.read_sql_query("""
        SELECT incident_type, COUNT(*) AS count
        FROM cyber_incidents
        GROUP BY incident_type
        ORDER BY count DESC
    """, conn)
    conn.close()
    return df


def get_high_severity_by_status():
    """Count high-severity incidents by status."""
    conn = connect_database()
    df = pd.read_sql_query("""
        SELECT status, COUNT(*) AS count
        FROM cyber_incidents
        WHERE severity = 'High'
        GROUP BY status
        ORDER BY count DESC
    """, conn)
    conn.close()
    return df


def get_incident_types_with_many_cases(min_count=5):
    """Return incident types with more than min_count cases."""
    conn = connect_database()
    df = pd.read_sql_query("""
        SELECT incident_type, COUNT(*) AS count
        FROM cyber_incidents
        GROUP BY incident_type
        HAVING COUNT(*) > ?
        ORDER BY count DESC
    """, conn, params=(min_count,))
    conn.close()
    return df
