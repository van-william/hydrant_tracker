import sqlite3

# Connect to your database
conn = sqlite3.connect('./streamlit/hydrant.db')
cursor = conn.cursor()



# Execute the above steps
create_table = """
               CREATE TABLE IF NOT EXISTS hydrant_update
               (id INTEGER PRIMARY KEY,
               latitude REAL,
               longitude REAL,
               status TEXT,
               pressure REAL
               );            
               """
cursor.execute(create_table)
modify_table = """INSERT INTO hydrant_update (id, latitude, longitude, status, pressure) 
               SELECT id, latitude, longitude, status, pressure FROM hydrant_status;"""
cursor.execute(modify_table)
cursor.execute("DROP TABLE hydrant_status;")
cursor.execute("ALTER TABLE hydrant_update RENAME TO hydrant_status;")

# Commit and close
conn.commit()
conn.close()
