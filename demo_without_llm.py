"""
Demo script showing Nexus Spider Agent database operations without LLM.
This demonstrates the secure database management features.
"""

from nexus_spider_agent import DatabaseManager
import tempfile
import os


def print_section(title):
    """Print a section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def main():
    """Run the demo."""
    print("\n" + "█" * 60)
    print("  Nexus Spider Agent - Database Management Demo")
    print("  (LLM features require LM Studio)")
    print("█" * 60)
    
    # Create a temporary database
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        # Initialize database manager
        print_section("1. Initialize Database Manager")
        db = DatabaseManager(db_path)
        print(f"✓ Database path: {db_path}")
        
        db.create_database_if_not_exists()
        print("✓ Database file created")
        
        db.connect()
        print("✓ Connected to database")
        
        # Create tables
        print_section("2. Create Database Schema")
        
        # Users table
        create_users = """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        success, msg = db.execute_query(create_users)
        print(f"✓ Created 'users' table: {success}")
        
        # Products table
        create_products = """
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            category TEXT
        )
        """
        success, msg = db.execute_query(create_products)
        print(f"✓ Created 'products' table: {success}")
        
        # Insert sample data
        print_section("3. Insert Sample Data")
        
        users_data = [
            ("Alice Smith", "alice@example.com", 28),
            ("Bob Johnson", "bob@example.com", 35),
            ("Charlie Brown", "charlie@example.com", 42),
            ("Diana Prince", "diana@example.com", 30),
            ("Eve Wilson", "eve@example.com", 25)
        ]
        
        for name, email, age in users_data:
            success, msg = db.execute_query(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (name, email, age)
            )
            print(f"  • Inserted user: {name}")
        
        products_data = [
            ("Laptop", 999.99, 10, "Electronics"),
            ("Mouse", 25.50, 100, "Electronics"),
            ("Keyboard", 75.00, 50, "Electronics"),
            ("Monitor", 299.99, 25, "Electronics"),
            ("Desk Chair", 199.99, 15, "Furniture"),
            ("Standing Desk", 449.99, 8, "Furniture")
        ]
        
        for name, price, stock, category in products_data:
            success, msg = db.execute_query(
                "INSERT INTO products (name, price, stock, category) VALUES (?, ?, ?, ?)",
                (name, price, stock, category)
            )
            print(f"  • Inserted product: {name}")
        
        # Query data
        print_section("4. Query Data")
        
        print("\n→ All users:")
        success, results = db.execute_query("SELECT id, name, email, age FROM users")
        if success:
            for user in results:
                print(f"  {user['id']:2}. {user['name']:20} | {user['email']:25} | Age: {user['age']}")
        
        print("\n→ Users older than 30:")
        success, results = db.execute_query("SELECT name, age FROM users WHERE age > 30")
        if success:
            for user in results:
                print(f"  • {user['name']} (age {user['age']})")
        
        print("\n→ Electronics products:")
        success, results = db.execute_query(
            "SELECT name, price, stock FROM products WHERE category = ?",
            ("Electronics",)
        )
        if success:
            for product in results:
                print(f"  • {product['name']:15} | ${product['price']:7.2f} | Stock: {product['stock']}")
        
        print("\n→ Products under $100:")
        success, results = db.execute_query(
            "SELECT name, price FROM products WHERE price < 100 ORDER BY price"
        )
        if success:
            for product in results:
                print(f"  • {product['name']:15} | ${product['price']:6.2f}")
        
        # Demonstrate schema introspection
        print_section("5. Schema Introspection")
        
        tables = db.list_tables()
        print(f"\n→ Tables in database: {', '.join(tables)}")
        
        for table in tables:
            print(f"\n→ Structure of '{table}' table:")
            table_info = db.get_table_info(table)
            if table_info:
                for col in table_info:
                    pk = " [PRIMARY KEY]" if col['pk'] else ""
                    nn = " NOT NULL" if col['notnull'] else ""
                    print(f"  • {col['name']:15} {col['type']:10}{nn}{pk}")
        
        # Demonstrate security features
        print_section("6. Security Validation")
        
        test_queries = [
            ("SELECT * FROM users", True, "Valid SELECT query"),
            ("DROP DATABASE test", False, "Dangerous DROP DATABASE"),
            ("SELECT * FROM users; DROP TABLE users", False, "Multiple statements"),
            ("UPDATE users SET age = 99 WHERE id = 1", True, "Valid UPDATE"),
            ("TRUNCATE TABLE users", False, "Dangerous TRUNCATE")
        ]
        
        for query, should_pass, description in test_queries:
            is_valid, error_msg = db.validate_query(query)
            status = "✓" if (is_valid == should_pass) else "✗"
            result = "PASSED" if is_valid else f"BLOCKED: {error_msg}"
            print(f"  {status} {description:30} → {result}")
        
        # Aggregate queries
        print_section("7. Aggregate Queries")
        
        success, results = db.execute_query("SELECT COUNT(*) as total_users FROM users")
        if success and results:
            print(f"→ Total users: {results[0]['total_users']}")
        
        success, results = db.execute_query("SELECT AVG(age) as avg_age FROM users")
        if success and results:
            print(f"→ Average user age: {results[0]['avg_age']:.1f}")
        
        success, results = db.execute_query(
            "SELECT category, COUNT(*) as count, SUM(stock) as total_stock FROM products GROUP BY category"
        )
        if success:
            print("\n→ Products by category:")
            for row in results:
                print(f"  • {row['category']:15} | Items: {row['count']:2} | Total stock: {row['total_stock']:3}")
        
        success, results = db.execute_query(
            "SELECT SUM(price * stock) as inventory_value FROM products"
        )
        if success and results:
            print(f"\n→ Total inventory value: ${results[0]['inventory_value']:,.2f}")
        
        # Display full schema
        print_section("8. Complete Database Schema")
        schema = db.get_schema_info()
        print(f"\n{schema}")
        
        # Cleanup
        print_section("9. Cleanup")
        db.disconnect()
        print("✓ Database connection closed")
        
        print("\n" + "█" * 60)
        print("  Demo completed successfully!")
        print("  All database operations work correctly.")
        print()
        print("  To use natural language features:")
        print("  1. Install and run LM Studio")
        print("  2. Load a model (e.g., Mistral, Llama)")
        print("  3. Start the local server")
        print("  4. Run: python -m nexus_spider_agent")
        print("█" * 60 + "\n")
        
    finally:
        # Clean up temporary database
        if os.path.exists(db_path):
            os.unlink(db_path)


if __name__ == "__main__":
    main()
