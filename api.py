from flask import Flask, request, jsonify, render_template, redirect
from DatabaseConnection import DatabaseHandler
from fund_manager import EquityFundManager


class FundAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.db_handler = DatabaseHandler('database/funds.db')
        self.equity_manager = EquityFundManager(self.db_handler)

        self.setup_routes()

    def setup_routes(self):

        # task 1: Endpoint to retrieve a list of all funds 
        # task 2: Endpoint to retrieve details of a specific fund using its ID
        @self.app.route('/funds', methods=['GET'])
        def get_all_funds():
            """
            Retrieves a list of all equity funds and supports search functionality by name or fund_id.
            """
            try:
                # Retrieve all funds
                equity_funds = self.equity_manager.get_all_funds()
                
                # Handle search query
                search_query = request.args.get('search', default="", type=str).lower()
                
                if search_query:
                    # Filter funds by name or fund_id (case insensitive match)
                    equity_funds = [
                        fund for fund in equity_funds 
                        if search_query in fund["name"].lower() or search_query in fund["fund_id"].lower()
                    ]
                
                # Render the template with filtered data
                return render_template("funds.html", equity_funds=equity_funds)
                
            except Exception as e:
                return f"<p>Error: {str(e)}</p>"

            

        # task 2 : Endpoint to create a new fund  
        @self.app.route('/funds', methods=['POST'])
        def create_fund():
            """
            Create a new equity fund.
            """
            try:
                if request.is_json:
                    data = request.get_json()
                else:
                    # Handle form submissions
                    data = request.form.to_dict()
                self.equity_manager.create_fund(data)
                return """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Success</title>
                </head>
                <body>
                    <h1>Equity fund created successfully.</h1>
                    <a href="/funds">Back to Funds List</a>
                </body>
                </html>
                """
            except Exception as e:
                return jsonify({"error": str(e)}), 400
            
        # task 2 part b : Endpoint to create a new fund with a form
        @self.app.route('/addfunds',  methods=['GET'])
        def AddNewFund():
            return render_template('AddNewFunds.html')
        
        
        @self.app.route('/update/<fund_id>', methods=['GET'])
        def render_update_page(fund_id):
            try:
                # Fetch fund information from the database
                equity_funds = self.equity_manager.get_all_funds()
                fund_to_update = next((fund for fund in equity_funds if fund["fund_id"] == fund_id), None)

                if not fund_to_update:
                    return jsonify({"error": "Fund not found"}), 404

                return render_template('update_fund_form.html', fund=fund_to_update, action= "update")
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/delete/<fund_id>', methods=['GET'])
        def render_delete_page(fund_id):
            try:
                # Fetch fund information from the database
                equity_funds = self.equity_manager.get_all_funds()
                fund_to_update = next((fund for fund in equity_funds if fund["fund_id"] == fund_id), None)

                if not fund_to_update:
                    return jsonify({"error": "Fund not found"}), 404

                return render_template('update_fund_form.html', fund=fund_to_update, action="delete")
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/funds/<fund_id>', methods=['POST'])
        def put_fund(fund_id):
            """
            Endpoint to update or delete a fund's information using form submission.
            """
            try:
        # Determine if the request is JSON or form-based
                if request.is_json:
                    # Handle JSON payload
                    data = request.get_json()
                    if not data:
                        return jsonify({"error": "Invalid JSON payload"}), 400

                    # Expecting fields to update
                    expected_fields = ["name", "manager_name", "description", "nav", "creation_date", "performance"]
                    if not any(field in data for field in expected_fields):
                        return jsonify({"error": "No valid fields to update"}), 400

                    # Perform database update
                    with DatabaseHandler('database/test_funds.db').connect() as conn:
                        cursor = conn.cursor()
                        query = f"UPDATE funds SET {', '.join([f'{key} = ?' for key in data.keys()])} WHERE fund_id = ?"
                        cursor.execute(query, list(data.values()) + [fund_id])
                        conn.commit()

                        if cursor.rowcount == 0:
                            return jsonify({"error": "Fund not found"}), 404

                    return jsonify({"message": "Fund updated successfully"}), 200

                else:
                    # Handle form submission
                    action = request.form.get('action')

                    if action == "update":
                        # Parse the form data for updating
                        fund_data = request.form.to_dict()

                        # Validate and process numeric fields
                        fund_data['nav'] = float(fund_data.get('nav', 0))
                        fund_data['performance'] = float(fund_data.get('performance', 0))

                        # Update the fund using the manager
                        result = self.equity_manager.update_fund(fund_id, fund_data)

                        if "error" in result:
                            return jsonify({"error": result["error"]}), 400

                        # Return success message for form submission
                        return """
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Success</title>
                        </head>
                        <body>
                            <h1>Fund updated successfully.</h1>
                            <a href="/funds">Back to Funds List</a>
                        </body>
                        </html>
                        """

                    elif action == "delete":
                        # Handle delete functionality
                        result = self.equity_manager.delete_funds(fund_id)

                        if "error" in result:
                            return jsonify({"error": result["error"]}), 400

                        # Return success message for delete
                        return """
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Success</title>
                        </head>
                        <body>
                            <h1>Fund deleted successfully.</h1>
                            <a href="/funds">Back to Funds List</a>
                        </body>
                        </html>
                        """

                    else:
                        # Invalid action
                        return jsonify({"error": "Invalid action"}), 400

            except Exception as e:
                return jsonify({"error": str(e)}), 500


        
        @self.app.route('/delete/<fund_id>', methods=['POST'])
        def delete_fund(fund_id):
            try:
                result = self.equity_manager.delete_funds(fund_id)
                
                if "error" in result:
                    return jsonify({"error": result["error"]}), 400
                
                # Return a JSON response instead of redirecting
                return jsonify({"message": "Fund deleted successfully"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500





        #Home page
        @self.app.route('/')
        def HomaPage():
            return render_template('HomePage.html')

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    api = FundAPI()
    api.run()
