import pandas as pd
from app.data.db import connect_database


def fetch_all_tickets():
    """Retrieve every IT ticket as a DataFrame."""
    conn = connect_database()

    query = "SELECT * FROM it_tickets ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)

    conn.close()
    return df