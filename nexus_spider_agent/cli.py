"""
Command-line interface for Nexus Spider Agent.
"""

import sys
import json
from typing import Optional
from .agent import NexusSpiderAgent


class CLI:
    """Interactive command-line interface for the agent."""
    
    def __init__(self, agent: NexusSpiderAgent):
        """
        Initialize CLI.
        
        Args:
            agent: Nexus Spider Agent instance
        """
        self.agent = agent
        self.running = True
    
    def print_banner(self):
        """Print welcome banner."""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║         Nexus Spider Agent - Database Assistant           ║
║    Privacy-focused SQL agent powered by local LLMs        ║
╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_help(self):
        """Print help information."""
        help_text = """
Available Commands:
  - Type natural language queries to generate SQL
  - /execute <query>  - Execute a SQL query directly
  - /schema [table]   - Show database schema (optionally for specific table)
  - /tables           - List all tables in the database
  - /info <table>     - Show detailed information about a table
  - /history          - Show conversation history
  - /clear            - Clear conversation history
  - /help             - Show this help message
  - /quit or /exit    - Exit the application

Examples:
  > Show me all users
  > Create a table called products with id, name, and price columns
  > Insert a new user with name John and email john@example.com
  > /schema users
  > /execute SELECT * FROM users LIMIT 10
        """
        print(help_text)
    
    def format_results(self, results):
        """
        Format query results for display.
        
        Args:
            results: Query results (list of dicts or string)
        """
        if isinstance(results, str):
            print(f"\n{results}\n")
        elif isinstance(results, list):
            if not results:
                print("\nNo results found.\n")
            else:
                # Pretty print as JSON for now
                print("\nResults:")
                for i, row in enumerate(results, 1):
                    print(f"\n{i}. {json.dumps(row, indent=2)}")
                print(f"\nTotal rows: {len(results)}\n")
        else:
            print(f"\n{results}\n")
    
    def handle_command(self, command: str):
        """
        Handle a user command.
        
        Args:
            command: User input command
        """
        command = command.strip()
        
        if not command:
            return
        
        # Handle special commands
        if command.startswith('/'):
            self.handle_special_command(command)
        else:
            # Process as natural language query
            self.handle_natural_language(command)
    
    def handle_special_command(self, command: str):
        """
        Handle special slash commands.
        
        Args:
            command: Special command starting with /
        """
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else None
        
        if cmd in ['/quit', '/exit']:
            print("\nGoodbye!")
            self.running = False
        
        elif cmd == '/help':
            self.print_help()
        
        elif cmd == '/execute':
            if not args:
                print("Error: Please provide a SQL query to execute")
                return
            
            print(f"\nExecuting query: {args}")
            result = self.agent.execute_query(args)
            
            if result["success"]:
                self.format_results(result["results"])
            else:
                print(f"\nError: {result['message']}\n")
        
        elif cmd == '/schema':
            schema = self.agent.get_schema(args)
            if schema:
                print(f"\n{schema}\n")
            else:
                print("\nNo schema information available.\n")
        
        elif cmd == '/tables':
            tables = self.agent.list_tables()
            if tables:
                print("\nTables in database:")
                for table in tables:
                    print(f"  - {table}")
                print()
            else:
                print("\nNo tables found in database.\n")
        
        elif cmd == '/info':
            if not args:
                print("Error: Please provide a table name")
                return
            
            info = self.agent.get_table_info(args)
            if info:
                print(f"\nTable: {args}")
                print("\nColumns:")
                for col in info:
                    pk_marker = " (PRIMARY KEY)" if col["pk"] else ""
                    notnull = " NOT NULL" if col["notnull"] else ""
                    default = f" DEFAULT {col['default_value']}" if col["default_value"] else ""
                    print(f"  - {col['name']}: {col['type']}{notnull}{default}{pk_marker}")
                print()
            else:
                print(f"\nTable '{args}' not found or error retrieving information.\n")
        
        elif cmd == '/history':
            history = self.agent.get_conversation_history()
            if history:
                print("\nConversation History:")
                for i, entry in enumerate(history, 1):
                    executed = "✓" if entry["executed"] else "○"
                    print(f"\n{i}. [{executed}] Command: {entry['command']}")
                    print(f"   Query: {entry['query']}")
                print()
            else:
                print("\nNo conversation history.\n")
        
        elif cmd == '/clear':
            self.agent.clear_history()
            print("\nConversation history cleared.\n")
        
        else:
            print(f"\nUnknown command: {cmd}")
            print("Type /help for available commands.\n")
    
    def handle_natural_language(self, command: str):
        """
        Handle natural language command.
        
        Args:
            command: Natural language command
        """
        print(f"\nProcessing: {command}")
        print("Generating SQL query...")
        
        result = self.agent.process_command(command)
        
        if result["query"]:
            print(f"\nGenerated Query:\n{result['query']}\n")
        
        if result["success"]:
            if result["results"]:
                self.format_results(result["results"])
            else:
                print(result["message"])
        else:
            print(f"Error: {result['message']}\n")
            
        # Ask if user wants to execute (if not auto-executed)
        if result["query"] and not self.agent.auto_execute:
            response = input("Execute this query? (y/n): ").strip().lower()
            if response == 'y':
                exec_result = self.agent.execute_query(result["query"])
                if exec_result["success"]:
                    self.format_results(exec_result["results"])
                else:
                    print(f"\nError: {exec_result['message']}\n")
    
    def run(self):
        """Run the interactive CLI."""
        self.print_banner()
        print("Type /help for available commands.\n")
        
        while self.running:
            try:
                command = input("nexus> ").strip()
                if command:
                    self.handle_command(command)
            except KeyboardInterrupt:
                print("\n\nInterrupted. Type /quit to exit.\n")
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")


def main():
    """Main entry point for CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Nexus Spider Agent - Privacy-focused database assistant"
    )
    parser.add_argument(
        "--db",
        default="database.db",
        help="Path to SQLite database (default: database.db)"
    )
    parser.add_argument(
        "--lm-studio-url",
        default="http://localhost:1234/v1",
        help="LM Studio API URL (default: http://localhost:1234/v1)"
    )
    parser.add_argument(
        "--auto-execute",
        action="store_true",
        help="Automatically execute generated queries (use with caution)"
    )
    
    args = parser.parse_args()
    
    # Create agent
    agent = NexusSpiderAgent(
        db_path=args.db,
        lm_studio_url=args.lm_studio_url,
        auto_execute=args.auto_execute
    )
    
    # Initialize
    success, message = agent.initialize()
    if not success:
        print(f"Error: {message}")
        sys.exit(1)
    
    print(f"Connected to database: {args.db}")
    print(f"LM Studio URL: {args.lm_studio_url}")
    if args.auto_execute:
        print("⚠️  Auto-execute mode enabled")
    print()
    
    # Run CLI
    cli = CLI(agent)
    try:
        cli.run()
    finally:
        agent.close()


if __name__ == "__main__":
    main()
