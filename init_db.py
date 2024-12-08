import sqlite3

# Path to the database
db_path = 'database/funds.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open('database/database.sql', 'r') as f:
    cursor.executescript(f.read())

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully.")
