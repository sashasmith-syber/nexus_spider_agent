"""
Main Nexus Spider Agent that orchestrates LLM interaction and database management.
"""

from typing import Dict, Any, Optional, List, Tuple
from .llm_client import LMStudioClient
from .db_manager import DatabaseManager


class NexusSpiderAgent:
    """
    Main agent class that coordinates between LLM and database operations.
    """
    
    def __init__(
        self,
        db_path: str,
        lm_studio_url: str = "http://localhost:1234/v1",
        auto_execute: bool = False
    ):
        """
        Initialize the Nexus Spider Agent.
        
        Args:
            db_path: Path to SQLite database
            lm_studio_url: URL for LM Studio API
            auto_execute: Whether to automatically execute queries (use with caution)
        """
        self.db_manager = DatabaseManager(db_path)
        self.llm_client = LMStudioClient(base_url=lm_studio_url)
        self.auto_execute = auto_execute
        self.conversation_history: List[Dict[str, str]] = []
    
    def initialize(self) -> Tuple[bool, str]:
        """
        Initialize the agent by connecting to database and checking LLM connection.
        
        Returns:
            Tuple of (success, message)
        """
        # Create database if it doesn't exist
        if not self.db_manager.create_database_if_not_exists():
            return False, "Failed to create database"
        
        # Connect to database
        if not self.db_manager.connect():
            return False, "Failed to connect to database"
        
        # Check LLM connection
        if not self.llm_client.check_connection():
            return False, "Failed to connect to LM Studio. Make sure it's running on the configured URL."
        
        return True, "Agent initialized successfully"
    
    def process_command(
        self,
        command: str,
        execute: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Process a natural language command.
        
        Args:
            command: Natural language command from user
            execute: Whether to execute the generated query (overrides auto_execute)
            
        Returns:
            Dictionary with processing results
        """
        result = {
            "command": command,
            "success": False,
            "message": "",
            "query": None,
            "results": None
        }
        
        # Get database schema for context
        schema_info = self.db_manager.get_schema_info()
        
        # Generate SQL query
        query = self.llm_client.generate_sql_query(
            natural_language_command=command,
            schema_info=schema_info
        )
        
        if not query:
            result["message"] = "Failed to generate SQL query"
            return result
        
        result["query"] = query
        
        # Validate query
        is_valid, error_msg = self.db_manager.validate_query(query)
        if not is_valid:
            result["message"] = f"Invalid query: {error_msg}"
            return result
        
        # Determine if we should execute
        should_execute = execute if execute is not None else self.auto_execute
        
        if should_execute:
            success, output = self.db_manager.execute_query(query)
            result["success"] = success
            result["results"] = output if success else None
            result["message"] = output if isinstance(output, str) else "Query executed successfully"
        else:
            result["success"] = True
            result["message"] = "Query generated (not executed). Review and execute manually if desired."
        
        # Store in conversation history
        self.conversation_history.append({
            "command": command,
            "query": query,
            "executed": should_execute
        })
        
        return result
    
    def execute_query(self, query: str) -> Dict[str, Any]:
        """
        Execute a SQL query directly.
        
        Args:
            query: SQL query to execute
            
        Returns:
            Dictionary with execution results
        """
        result = {
            "query": query,
            "success": False,
            "message": "",
            "results": None
        }
        
        success, output = self.db_manager.execute_query(query)
        result["success"] = success
        result["results"] = output if success else None
        result["message"] = output if isinstance(output, str) else "Query executed successfully"
        
        return result
    
    def get_schema(self, table_name: Optional[str] = None) -> Optional[str]:
        """
        Get database schema information.
        
        Args:
            table_name: Specific table name, or None for all tables
            
        Returns:
            Schema information as a string
        """
        return self.db_manager.get_schema_info(table_name)
    
    def list_tables(self) -> List[str]:
        """
        List all tables in the database.
        
        Returns:
            List of table names
        """
        return self.db_manager.list_tables()
    
    def get_table_info(self, table_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get detailed information about a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information
        """
        return self.db_manager.get_table_info(table_name)
    
    def interpret_command(self, command: str) -> Optional[Dict[str, Any]]:
        """
        Interpret a command to understand user intent.
        
        Args:
            command: Natural language command
            
        Returns:
            Dictionary with intent and parameters
        """
        context = {
            "tables": self.list_tables(),
            "database": self.db_manager.db_path
        }
        
        return self.llm_client.interpret_command(command, context)
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Returns:
            List of conversation entries
        """
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history.clear()
    
    def close(self):
        """Close all connections and clean up resources."""
        self.db_manager.disconnect()
