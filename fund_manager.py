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
                
                # Check if the update impacted any rows
                if cursor.rowcount == 0:
                    return {"error": "No fund with given ID"}
                return {"status": "success", "message": "Fund successfully updated."}
        except Exception as e:
            return {"error": str(e)}

    def create_fund(self, fund_data):
        required_fields = ["fund_id", "name", "manager_name", "description", "nav", "creation_date", "performance"]
        
        # Validate required fields
        for field in required_fields:
            if field not in fund_data:
                return {"error": f"Missing required field: {field}"}

        # Prepare and execute query
        try:
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
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
            return {"status": "success", "message": "Fund successfully created."}
        except Exception as e:
            return {"error": str(e)}

    def get_all_funds(self):
        try:
            query = "SELECT * FROM funds"
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query)

                # Dynamically map column names to rows
                column_names = [description[0] for description in cursor.description]
                rows = cursor.fetchall()

                # Map rows into a list of dictionaries
                funds = [dict(zip(column_names, row)) for row in rows]
            return {"status": "success", "data": funds}
        except Exception as e:
            return {"error": str(e)}

    def delete_funds(self, fund_id):
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM funds WHERE fund_id = ?", (fund_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    return {"error": "No fund with the given ID"}
                return {"status": "success", "message": "Fund successfully deleted"}
        except Exception as e:
            return {"error": str(e)}


class EquityFundManager(FundManager):
    def __init__(self, db_handler):
        super().__init__(db_handler)
