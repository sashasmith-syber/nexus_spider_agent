"""
Nexus Spider Agent - A lightweight, privacy-focused Python agent
that connects to locally running LLMs to manage SQLite databases.
"""

__version__ = "0.1.0"
__author__ = "Nexus Spider Agent Contributors"

from .agent import NexusSpiderAgent
from .llm_client import LMStudioClient
from .db_manager import DatabaseManager

__all__ = ["NexusSpiderAgent", "LMStudioClient", "DatabaseManager"]
