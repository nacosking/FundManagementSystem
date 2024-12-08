import sqlite3
import os


class DatabaseHandler:
    def __init__(self, db_file):
        # Ensure the database directory exists
        db_dir = os.path.dirname(db_file)  # Extract directory from the full path
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)  # Create the directory if it doesn't exist
        self.db_file = db_file

    def connect(self):
        # Connect to SQLite database at the specified path
        return sqlite3.connect(self.db_file)
