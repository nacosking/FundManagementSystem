from flask import Flask, request, jsonify
from DatabaseConnection import DatabaseHandler
from fund_manager import EquityFundManager

class FundAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.db_handler = DatabaseHandler('funds.db')
        self.equity_manager = EquityFundManager(self.db_handler)

        self.setup_routes()

    def setup_routes(self):
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

    def run(self):
        self.app.run(debug=True)
