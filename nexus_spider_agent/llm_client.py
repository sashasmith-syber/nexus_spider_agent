"""
LM Studio client for connecting to locally running LLMs.
"""

import json
import requests
from typing import Dict, Optional, Any


class LMStudioClient:
    """Client for interacting with LM Studio's local API."""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1", timeout: int = 30):
        """
        Initialize the LM Studio client.
        
        Args:
            base_url: Base URL for LM Studio API (default: http://localhost:1234/v1)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.chat_endpoint = f"{self.base_url}/chat/completions"
    
    def check_connection(self) -> bool:
        """
        Check if LM Studio is running and accessible.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Use a shorter timeout for connection checks
            check_timeout = min(5, self.timeout)
            response = requests.get(f"{self.base_url}/models", timeout=check_timeout)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def generate_sql_query(
        self,
        natural_language_command: str,
        schema_info: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        Generate SQL query from natural language command.
        
        Args:
            natural_language_command: User's natural language request
            schema_info: Database schema information for context
            temperature: LLM temperature (lower = more deterministic)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated SQL query or None if generation failed
        """
        system_prompt = """You are an expert SQL query generator. Given a natural language command and optional database schema, generate a valid SQLite query.

Rules:
1. Return ONLY the SQL query, no explanations or markdown
2. Use proper SQLite syntax
3. Ensure queries are safe and do not contain dangerous operations
4. Use parameterized queries when possible
5. For SELECT queries, include appropriate WHERE clauses when needed
6. For INSERT/UPDATE/DELETE, be cautious and validate the operation"""

        user_prompt = f"Natural language command: {natural_language_command}"
        if schema_info:
            user_prompt += f"\n\nDatabase schema:\n{schema_info}"
        
        user_prompt += "\n\nGenerate the SQLite query:"
        
        try:
            response = self._chat_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if response:
                # Clean up the response
                sql_query = response.strip()
                # Remove markdown code blocks if present
                if sql_query.startswith("```sql"):
                    sql_query = sql_query[6:]
                if sql_query.startswith("```"):
                    sql_query = sql_query[3:]
                if sql_query.endswith("```"):
                    sql_query = sql_query[:-3]
                return sql_query.strip()
            
            return None
        except Exception as e:
            print(f"Error generating SQL query: {e}")
            return None
    
    def interpret_command(
        self,
        command: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Interpret a natural language command and extract intent and parameters.
        
        Args:
            command: Natural language command
            context: Additional context for interpretation
            
        Returns:
            Dictionary with intent and parameters, or None if interpretation failed
        """
        system_prompt = """You are an intelligent command interpreter. Analyze natural language commands and extract:
1. Intent: what the user wants to do (e.g., query, insert, update, delete, create_table, describe)
2. Parameters: relevant details from the command

Return your response as a JSON object with 'intent' and 'parameters' keys."""

        user_prompt = f"Command: {command}"
        if context:
            user_prompt += f"\n\nContext: {json.dumps(context)}"
        
        try:
            response = self._chat_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.2,
                max_tokens=300
            )
            
            if response:
                # Try to parse as JSON
                try:
                    return json.loads(response)
                except json.JSONDecodeError:
                    # Extract JSON from response if embedded
                    start = response.find('{')
                    end = response.rfind('}') + 1
                    if start != -1 and end > start:
                        return json.loads(response[start:end])
            
            return None
        except Exception as e:
            print(f"Error interpreting command: {e}")
            return None
    
    def _chat_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        Send a chat completion request to LM Studio.
        
        Args:
            system_prompt: System prompt for the LLM
            user_prompt: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text or None if request failed
        """
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.chat_endpoint,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Response parsing error: {e}")
            return None
