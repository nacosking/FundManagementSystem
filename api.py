from flask import Flask, request, jsonify, render_template
from DatabaseConnection import DatabaseHandler
from fund_manager import EquityFundManager


class FundAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.db_handler = DatabaseHandler('funds.db')
        self.equity_manager = EquityFundManager(self.db_handler)

        self.setup_routes()

    def setup_routes(self):

        # task 1: Endpoint to retrieve a list of all funds  
        @self.app.route('/funds', methods=['GET'])
        def get_all_funds():
            """
            Retrieve a list of all equity funds and return as a dynamically generated HTML page.
            """
            try:
                # Retrieve data from the database
                equity_funds = self.equity_manager.get_all_funds()
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
            
        
        @self.app.route('/addfunds',  methods=['GET'])
        def AddNewFund():
            return render_template('AddNewFunds.html')

        @self.app.route('/')
        def HomaPage():
            return render_template('HomePage.html')

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    api = FundAPI()
    api.run()
