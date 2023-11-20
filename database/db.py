import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

def create_table(db_file):
    conn = sqlite3.connect(db_file)
    try:
        c = conn.cursor()
        c.execute("""
    
    CREATE TABLE IF NOT EXISTS hydrant_status (
        lat REAL,
        lon REAL,
        status TEXT,
        comments TEXT);
                    """)
    except Error as e:
        print(e)

if __name__ == '__main__':
    create_connection("./streamlit/hydrant_tracker.db")
    create_table("./streamlit/hydrant_tracker.db")