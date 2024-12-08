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
    
    def update_fund(self, fund_id, fund_data):
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE funds 
                    SET name = ?, manager_name = ?, description = ?, nav = ?, creation_date = ?, performance = ?
                    WHERE fund_id = ?
                """, (
                    fund_data['name'],
                    fund_data['manager_name'],
                    fund_data['description'],
                    fund_data['nav'],
                    fund_data['creation_date'],
                    fund_data['performance'],
                    fund_id,
                ))
                conn.commit()
                if cursor.rowcount == 0:
                    return {"error": "No fund with given ID"}
                return {"message": "Fund successfully updated."}
        except Exception as e:
            return {"error": str(e)}



    def create_fund(self, fund_data, funds_id):
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

    def get_all_funds(self):
        query = "SELECT * FROM funds"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Dynamically map column names to rows
            column_names = [description[0] for description in cursor.description]  # Get column names dynamically
            rows = cursor.fetchall()
            
            # Map rows into a list of dictionaries
            funds = [dict(zip(column_names, row)) for row in rows]
            
            return funds

class EquityFundManager(FundManager):
    def __init__(self, db_handler):
        super().__init__(db_handler)
