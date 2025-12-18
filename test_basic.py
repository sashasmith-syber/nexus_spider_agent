"""
Basic tests for Nexus Spider Agent components.
"""

import os
import tempfile
from nexus_spider_agent import DatabaseManager, LMStudioClient


def test_database_manager():
    """Test basic database manager functionality."""
    print("Testing DatabaseManager...")
    
    # Create a temporary database using mkstemp for better cleanup
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)  # Close the file descriptor
    
    try:
        # Initialize database manager
        db = DatabaseManager(db_path)
        assert db.create_database_if_not_exists(), "Failed to create database"
        assert db.connect(), "Failed to connect to database"
        
        # Test query validation
        valid, msg = db.validate_query("SELECT * FROM users")
        assert valid, f"Valid query rejected: {msg}"
        
        valid, msg = db.validate_query("DROP DATABASE test")
        assert not valid, "Dangerous query not rejected"
        
        valid, msg = db.validate_query("SELECT * FROM users; DROP TABLE users")
        assert not valid, "Multiple statements not rejected"
        
        # Test table creation
        success, result = db.execute_query("""
            CREATE TABLE test_users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )
        """)
        assert success, f"Failed to create table: {result}"
        
        # Test insertion
        success, result = db.execute_query(
            "INSERT INTO test_users (name, email) VALUES (?, ?)",
            ("John Doe", "john@example.com")
        )
        assert success, f"Failed to insert data: {result}"
        
        # Test selection
        success, results = db.execute_query("SELECT * FROM test_users")
        assert success, f"Failed to select data: {results}"
        assert len(results) == 1, "Expected 1 row"
        assert results[0]['name'] == "John Doe", "Data mismatch"
        
        # Test schema info
        schema = db.get_schema_info()
        assert schema is not None, "Failed to get schema"
        assert "test_users" in schema, "Table not in schema"
        
        # Test list tables
        tables = db.list_tables()
        assert "test_users" in tables, "Table not listed"
        
        # Test table info
        table_info = db.get_table_info("test_users")
        assert table_info is not None, "Failed to get table info"
        assert len(table_info) == 3, "Expected 3 columns"
        
        db.disconnect()
        print("✓ DatabaseManager tests passed")
        
    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_llm_client():
    """Test LLM client initialization."""
    print("Testing LMStudioClient...")
    
    client = LMStudioClient()
    assert client.base_url == "http://localhost:1234/v1", "Wrong base URL"
    assert client.timeout == 30, "Wrong timeout"
    
    # Connection test will fail if LM Studio is not running, but that's OK
    is_connected = client.check_connection()
    if is_connected:
        print("✓ LM Studio is running and accessible")
    else:
        print("⚠ LM Studio is not running (this is OK for basic tests)")
    
    print("✓ LMStudioClient tests passed")


def main():
    """Run all tests."""
    print("Running basic tests for Nexus Spider Agent")
    print("=" * 50)
    
    test_database_manager()
    test_llm_client()
    
    print("=" * 50)
    print("All basic tests passed!")


if __name__ == "__main__":
    main()
