import pytest
import json
from api import FundAPI
from DatabaseConnection import DatabaseHandler
from fund_manager import EquityFundManager


# Fixture to create the Flask app for testing
@pytest.fixture
def test_app():
    # Use the test database
    test_api = FundAPI()
    test_api.db_handler = DatabaseHandler('database/test_funds.db')  # Set the test DB
    test_api.equity_manager = EquityFundManager(test_api.db_handler)

    # Initialize database schema for clean slate
    with test_api.db_handler.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS funds (
            fund_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            manager_name TEXT NOT NULL,
            description TEXT,
            nav REAL NOT NULL,
            creation_date TEXT NOT NULL,
            performance REAL
        );
        """)
        conn.commit()

    yield test_api.app.test_client()
    
    # Cleanup database after test
    with test_api.db_handler.connect() as conn:
        conn.execute("DROP TABLE IF EXISTS funds")
        conn.commit()


# Test Cases
def test_home_page(test_app):
    """Test the home page renders properly."""
    response = test_app.get('/')
    assert response.status_code == 200


def test_get_all_funds(test_app):
    """Test retrieving all funds with no funds yet."""
    response = test_app.get('/funds')
    assert response.status_code == 200
    assert b"No funds found" or b"equity funds" in response.data


def test_create_fund(test_app):
    """Test creating a new equity fund."""
    fund_data = {
        "fund_id": "123",
        "name": "Test Fund",
        "manager_name": "John Doe",
        "description": "A sample equity fund",
        "nav": 100.0,
        "creation_date": "2024-01-01",
        "performance": 10.0
    }
    response = test_app.post('/funds', data=json.dumps(fund_data), content_type="application/json")
    
    assert response.status_code == 200
    assert b"Equity fund created successfully" in response.data


def test_update_fund(test_app):
    """Test updating a fund."""
    # First, insert a fund into the database
    fund_data = {
        "fund_id": "123",
        "name": "Initial Test Fund",
        "manager_name": "John Doe",
        "description": "Initial fund description",
        "nav": 100.0,
        "creation_date": "2024-01-01",
        "performance": 10.0
    }

    with DatabaseHandler('database/test_funds.db').connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO funds (fund_id, name, manager_name, description, nav, creation_date, performance)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            fund_data["fund_id"],
            fund_data["name"],
            fund_data["manager_name"],
            fund_data["description"],
            fund_data["nav"],
            fund_data["creation_date"],
            fund_data["performance"]
        ))
        conn.commit()

    # Test updating the fund
    updated_data = {
        "name": "Updated Fund",
        "manager_name": "Jane Doe",
        "description": "Updated description",
        "nav": 200.0,
        "creation_date": "2024-02-01",
        "performance": 20.0
    }

    response = test_app.post('/funds/123', data=json.dumps(updated_data), content_type="application/json")
    assert response.status_code == 200
    assert b"Fund updated successfully" in response.data



def test_delete_fund(test_app):
    """Test deleting a fund."""
    with DatabaseHandler('database/test_funds.db').connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO funds (fund_id, name, manager_name, description, nav, creation_date, performance)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("delete_test", "Test Delete Fund", "Manager", "Sample description", 100.0, "2024-01-01", 5.0))
        conn.commit()

    # Send delete request
    response = test_app.post('/delete/delete_test')
    assert response.status_code == 200


def test_search(test_app):
    """Test the search functionality by query string."""
    # Add sample data to database for search
    with DatabaseHandler('database/test_funds.db').connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO funds (fund_id, name, manager_name, description, nav, creation_date, performance)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("search_001", "Alpha Fund", "Manager A", "A search test", 100.0, "2023-12-01", 12.0))
        conn.commit()

    # Perform search
    response = test_app.get('/funds?search=alpha')
    assert response.status_code == 200
    assert b"Alpha Fund" in response.data
