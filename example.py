"""
Example script demonstrating programmatic usage of Nexus Spider Agent.
"""

from nexus_spider_agent import NexusSpiderAgent


def main():
    """Demonstrate basic usage of Nexus Spider Agent."""
    
    # Create agent with a test database
    agent = NexusSpiderAgent(
        db_path="example.db",
        lm_studio_url="http://localhost:1234/v1",
        auto_execute=False  # Safety first!
    )
    
    print("Nexus Spider Agent - Example Usage")
    print("=" * 50)
    
    # Initialize the agent
    print("\n1. Initializing agent...")
    success, message = agent.initialize()
    if not success:
        print(f"Error: {message}")
        return
    print(f"✓ {message}")
    
    # Create a sample table
    print("\n2. Creating a sample users table...")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    result = agent.execute_query(create_table_query)
    print(f"✓ {result['message']}")
    
    # Insert some sample data
    print("\n3. Inserting sample data...")
    insert_queries = [
        "INSERT INTO users (name, email) VALUES ('Alice Smith', 'alice@example.com')",
        "INSERT INTO users (name, email) VALUES ('Bob Johnson', 'bob@example.com')",
        "INSERT INTO users (name, email) VALUES ('Charlie Brown', 'charlie@example.com')"
    ]
    for query in insert_queries:
        result = agent.execute_query(query)
        if not result['success']:
            print(f"Note: {result['message']}")
    print("✓ Sample data inserted")
    
    # Show database schema
    print("\n4. Database Schema:")
    schema = agent.get_schema()
    print(schema)
    
    # List tables
    print("\n5. Tables in database:")
    tables = agent.list_tables()
    for table in tables:
        print(f"  - {table}")
    
    # Get table info
    print("\n6. Detailed information for 'users' table:")
    table_info = agent.get_table_info('users')
    if table_info:
        for col in table_info:
            print(f"  - {col['name']}: {col['type']}", end="")
            if col['pk']:
                print(" (PRIMARY KEY)", end="")
            if col['notnull']:
                print(" NOT NULL", end="")
            print()
    
    # Process natural language commands
    print("\n7. Processing natural language commands...")
    
    commands = [
        "Show me all users",
        "Find users whose names start with A",
        "Count how many users we have"
    ]
    
    for cmd in commands:
        print(f"\n   Command: \"{cmd}\"")
        result = agent.process_command(cmd)
        if result['query']:
            print(f"   Generated: {result['query']}")
        if result['success']:
            print(f"   Status: {result['message']}")
        else:
            print(f"   Error: {result['message']}")
    
    # Show conversation history
    print("\n8. Conversation History:")
    history = agent.get_conversation_history()
    for i, entry in enumerate(history, 1):
        print(f"   {i}. {entry['command']}")
        print(f"      → {entry['query']}")
    
    # Clean up
    print("\n9. Cleaning up...")
    agent.close()
    print("✓ Agent closed")
    
    print("\n" + "=" * 50)
    print("Example completed successfully!")
    print("\nNote: This example requires LM Studio to be running.")
    print("Run 'python -m nexus_spider_agent' for the interactive CLI.")


if __name__ == "__main__":
    main()
