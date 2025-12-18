"""
Secure SQLite database manager with input validation and SQL injection prevention.
"""

import sqlite3
import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


class DatabaseManager:
    """Secure manager for SQLite database operations."""
    
    # Dangerous SQL keywords that should be blocked in certain contexts
    DANGEROUS_KEYWORDS = [
        'DROP DATABASE', 'DROP SCHEMA', 'TRUNCATE', 
        'GRANT', 'REVOKE', 'ALTER SYSTEM'
    ]
    
    # Allowed SQL operations
    ALLOWED_OPERATIONS = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
    
    def __init__(self, db_path: str):
        """
        Initialize the database manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
    
    def connect(self) -> bool:
        """
        Connect to the database.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def validate_query(self, query: str) -> Tuple[bool, Optional[str]]:
        """
        Validate SQL query for safety.
        
        Args:
            query: SQL query to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not query or not query.strip():
            return False, "Query is empty"
        
        query_upper = query.upper()
        
        # Check for dangerous keywords
        for keyword in self.DANGEROUS_KEYWORDS:
            if keyword in query_upper:
                return False, f"Dangerous operation detected: {keyword}"
        
        # Check if query starts with an allowed operation
        query_stripped = query.strip()
        first_word = query_stripped.split()[0].upper() if query_stripped else ""
        
        if first_word not in self.ALLOWED_OPERATIONS:
            return False, f"Operation not allowed: {first_word}"
        
        # Additional validation for DROP operations
        if first_word == 'DROP':
            if 'DROP DATABASE' in query_upper or 'DROP SCHEMA' in query_upper:
                return False, "Cannot drop database or schema"
        
        # Check for multiple statements (SQL injection prevention)
        if ';' in query.rstrip(';'):
            return False, "Multiple statements not allowed"
        
        return True, None
    
    def execute_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
        fetch: bool = True
    ) -> Tuple[bool, Any]:
        """
        Execute a SQL query with validation.
        
        Args:
            query: SQL query to execute
            parameters: Query parameters for parameterized queries
            fetch: Whether to fetch results (for SELECT queries)
            
        Returns:
            Tuple of (success, result/error_message)
        """
        if not self.connection:
            return False, "Not connected to database"
        
        # Validate query
        is_valid, error_msg = self.validate_query(query)
        if not is_valid:
            return False, f"Invalid query: {error_msg}"
        
        try:
            cursor = self.connection.cursor()
            
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            
            if fetch and query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                # Convert Row objects to dictionaries
                return True, [dict(row) for row in results]
            else:
                self.connection.commit()
                return True, f"Query executed successfully. Rows affected: {cursor.rowcount}"
        
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"
    
    def get_schema_info(self, table_name: Optional[str] = None) -> Optional[str]:
        """
        Get database schema information.
        
        Args:
            table_name: Specific table name, or None for all tables
            
        Returns:
            Schema information as a formatted string
        """
        if not self.connection:
            return None
        
        try:
            cursor = self.connection.cursor()
            
            if table_name:
                # Get schema for specific table
                cursor.execute(
                    "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
                    (table_name,)
                )
                result = cursor.fetchone()
                return result[0] if result else None
            else:
                # Get all tables
                cursor.execute(
                    "SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name"
                )
                tables = cursor.fetchall()
                
                if not tables:
                    return "No tables found in database"
                
                schema_info = "Database Schema:\n\n"
                for table in tables:
                    schema_info += f"Table: {table[0]}\n{table[1]}\n\n"
                
                return schema_info.strip()
        
        except sqlite3.Error as e:
            print(f"Error getting schema: {e}")
            return None
    
    def list_tables(self) -> List[str]:
        """
        List all tables in the database.
        
        Returns:
            List of table names
        """
        if not self.connection:
            return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error listing tables: {e}")
            return []
    
    def get_table_info(self, table_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get detailed information about a table's columns.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information dictionaries
        """
        if not self.connection:
            return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            return [
                {
                    "cid": col[0],
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "default_value": col[4],
                    "pk": bool(col[5])
                }
                for col in columns
            ]
        except sqlite3.Error as e:
            print(f"Error getting table info: {e}")
            return None
    
    def create_database_if_not_exists(self) -> bool:
        """
        Create database file if it doesn't exist.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            db_path = Path(self.db_path)
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not db_path.exists():
                # Create an empty database
                conn = sqlite3.connect(self.db_path)
                conn.close()
            
            return True
        except Exception as e:
            print(f"Error creating database: {e}")
            return False
