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

        @self.app.route('/funds', methods=['POST'])
        def create_fund():
            """
            Create a new equity fund.
            """
            try:
                data = request.get_json()
                self.equity_manager.create_fund(data)
                return jsonify({"message": "Equity fund created successfully."}), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 400

        @self.app.route('/')
        def HomaPage():
            return render_template('HomePage.html')

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    api = FundAPI()
    api.run()
