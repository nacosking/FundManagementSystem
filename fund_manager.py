from DatabaseConnection import DatabaseHandler

class FundManager:
    def __init__(self, db_handler):
        self.db = db_handler
        self.ensure_table_exists()  # Ensure the table exists for all managers.

    def ensure_table_exists(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS funds (
            fund_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            manager_name TEXT NOT NULL,
            description TEXT,
            nav REAL NOT NULL,
            creation_date TEXT NOT NULL,
            performance REAL
        );
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()

    def create_fund(self, fund_data):
        required_fields = ["fund_id", "name", "manager_name", "description", "nav", "creation_date", "performance"]
        
        # Validate input data
        for field in required_fields:
            if field not in fund_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Prepare the SQL query
        query = """
        INSERT INTO funds (fund_id, name, manager_name, description, nav, creation_date, performance)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            fund_data["fund_id"],
            fund_data["name"],
            fund_data["manager_name"],
            fund_data["description"],
            fund_data["nav"],
            fund_data["creation_date"],
            fund_data["performance"],
        )
        
        # Execute the query
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()



class EquityFundManager(FundManager):
    def __init__(self, db_handler):
        super().__init__(db_handler)
