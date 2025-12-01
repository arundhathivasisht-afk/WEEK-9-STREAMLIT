# app/data/datasets.py

import pandas as pd
from pathlib import Path
from app.data.db import connect_database


def get_table_columns(table_name):
    """Return list of valid SQL table columns."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cursor.fetchall()]
    conn.close()
    return cols


def load_csv_to_table(csv_path, table_name):
    """Load a CSV into the specified SQL table, with automatic column mapping."""
    csv_file = Path(csv_path)

    if not csv_file.exists():
        print(f"CSV not found: {csv_path}")
        return 0

    # Read CSV
    df = pd.read_csv(csv_file)

    # Normalize headers
    df.columns = [c.lower().strip() for c in df.columns]

    # Column rename rules (CSV → SQL)
    RENAME_MAP = {

        # cyber_incidents.csv
        "incident_id": "id",
        "timestamp": "date",
        "category": "incident_type",

        # datasets_metadata.csv
        "dataset_id": "id",
        "name": "dataset_name",
        "rows": "record_count",
        "columns": "file_size_mb",          # closest match
        "uploaded_by": "source",
        "upload_date": "last_updated",

        # it_tickets.csv
        "ticket_id": "ticket_id",
        "priority": "priority",
        "description": "description",        # keep description
        "created_at": "created_date",
        "resolution_time_hours": "resolved_date",
    }

    # Apply renaming
    df = df.rename(columns=RENAME_MAP)

    # SPECIAL FIX — IT tickets require subject (NOT NULL)
    if table_name == "it_tickets":
        if "subject" not in df.columns:
            # Use description as subject
            df["subject"] = df["description"]

        # category is required but missing → set to None
        if "category" not in df.columns:
            df["category"] = None

    # Get valid SQL table columns
    valid_cols = get_table_columns(table_name)

    # Filter DF → only keep columns that exist in SQL table
    df = df[[c for c in df.columns if c in valid_cols]]

    if df.empty:
        print(f"No valid columns to insert for {table_name} — check CSV structure.")
        return 0

    # Insert into SQL
    conn = connect_database()
    try:
        df.to_sql(table_name, conn, if_exists="append", index=False)
        print(f"Loaded {len(df)} rows into {table_name}")
        return len(df)
    except Exception as e:
        print(f"Error loading into {table_name}: {e}")
        return 0
    finally:
        conn.close()


def load_all_csv_data():
    """Load all required CSV files into all database tables."""
    total = 0
    total += load_csv_to_table("DATA/cyber_incidents.csv", "cyber_incidents")
    total += load_csv_to_table("DATA/datasets_metadata.csv", "datasets_metadata")
    total += load_csv_to_table("DATA/it_tickets.csv", "it_tickets")
    print(f"Total CSV rows loaded: {total}")
    return total
