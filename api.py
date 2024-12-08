from flask import Flask, request, jsonify, render_template
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
        
        

        #Home page
        @self.app.route('/')
        def HomaPage():
            return render_template('HomePage.html')

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    api = FundAPI()
    api.run()
