import sqlite3
from pathlib import Path

# Always build absolute path based on project root
ROOT_DIR = Path(__file__).resolve().parents[2]   # → project root
DATA_DIR = ROOT_DIR / "DATA"
DB_PATH = DATA_DIR / "intelligence_platform.db"

def connect_database():
    """Connect to SQLite database using absolute path."""
    DATA_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(str(DB_PATH))
