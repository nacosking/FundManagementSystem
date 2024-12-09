import sqlite3
import mysql.connector

# MySQL configuration
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Add your MySQL password here
    "database": "fund_management"
}

def migrate_data(sqlite_db_file):
    """
    Migrate data from SQLite to MySQL.
    """
    # Connect to SQLite
    sqlite_conn = sqlite3.connect(sqlite_db_file)
    sqlite_cursor = sqlite_conn.cursor()

    # Connect to MySQL
    mysql_conn = mysql.connector.connect(**mysql_config)
    mysql_cursor = mysql_conn.cursor()

    # Ensure MySQL table exists
    mysql_cursor.execute("""
    CREATE TABLE IF NOT EXISTS funds (
        fund_id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        manager_name VARCHAR(255) NOT NULL,
        description TEXT,
        nav DECIMAL(10, 2) NOT NULL,
        creation_date DATE NOT NULL,
        performance DECIMAL(5, 2)
    );
    """)

    # Fetch data from SQLite
    sqlite_cursor.execute("SELECT * FROM funds")
    rows = sqlite_cursor.fetchall()

    # Insert data into MySQL
    for row in rows:
        mysql_cursor.execute("""
        INSERT INTO funds (fund_id, name, manager_name, description, nav, creation_date, performance)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, row)

    # Commit and close connections
    mysql_conn.commit()
    sqlite_conn.close()
    mysql_conn.close()
    print("Migration completed.")
