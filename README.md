# Nexus Spider Agent

A lightweight, privacy-focused Python agent that connects to locally running LLMs in LM Studio to interpret natural language commands, generate SQL queries, and securely manage SQLite databases.

## Features

- 🔒 **Privacy-Focused**: All processing happens locally - no data leaves your machine
- 🤖 **LLM-Powered**: Leverages locally running LLMs via LM Studio for natural language understanding
- 🛡️ **Secure**: Built-in SQL injection prevention and query validation
- 🗃️ **SQLite Management**: Easy database operations with natural language
- 💬 **Interactive CLI**: User-friendly command-line interface
- 📝 **Query History**: Track your conversation and generated queries

## Prerequisites

- Python 3.7 or higher
- [LM Studio](https://lmstudio.ai/) installed and running locally
- A language model loaded in LM Studio (e.g., Mistral, Llama, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sashasmith-syber/nexus_spider_agent.git
cd nexus_spider_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

1. **Start LM Studio**:
   - Open LM Studio
   - Load a model (recommended: a code-capable model like CodeLlama or Mistral)
   - Start the local server (default: http://localhost:1234)

2. **Run Nexus Spider Agent**:
```bash
python -m nexus_spider_agent
```

Or specify a custom database:
```bash
python -m nexus_spider_agent --db mydata.db
```

## Usage

### Interactive CLI

Once started, you can interact with the agent using natural language:

```
nexus> Show me all users
Processing: Show me all users
Generating SQL query...

Generated Query:
SELECT * FROM users

Execute this query? (y/n): y

Results:
1. {
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
...
```

### Special Commands

- `/execute <query>` - Execute a SQL query directly
- `/schema [table]` - Show database schema (optionally for a specific table)
- `/tables` - List all tables in the database
- `/info <table>` - Show detailed information about a table
- `/history` - Show conversation history
- `/clear` - Clear conversation history
- `/help` - Show help message
- `/quit` or `/exit` - Exit the application

### Command-Line Options

```bash
python -m nexus_spider_agent --help

Options:
  --db DB                Path to SQLite database (default: database.db)
  --lm-studio-url URL    LM Studio API URL (default: http://localhost:1234/v1)
  --auto-execute         Automatically execute generated queries (use with caution)
```

## Example Usage

### Create a Table
```
nexus> Create a table called products with id, name, price, and description
```

### Insert Data
```
nexus> Insert a product with name "Laptop", price 999.99, and description "High-performance laptop"
```

### Query Data
```
nexus> Show me all products where price is less than 1000
```

### Update Data
```
nexus> Update the price of Laptop to 899.99
```

### Complex Queries
```
nexus> Show me the top 5 most expensive products with their names and prices
```

## Python API

You can also use Nexus Spider Agent programmatically:

```python
from nexus_spider_agent import NexusSpiderAgent

# Create agent
agent = NexusSpiderAgent(
    db_path="mydata.db",
    lm_studio_url="http://localhost:1234/v1"
)

# Initialize
success, message = agent.initialize()
if success:
    # Process natural language command
    result = agent.process_command("Show me all users")
    
    if result["query"]:
        print(f"Generated Query: {result['query']}")
    
    # Execute query directly
    exec_result = agent.execute_query("SELECT * FROM users")
    print(exec_result["results"])
    
    # Get schema
    schema = agent.get_schema()
    print(schema)
    
    # Clean up
    agent.close()
```

## Security Features

### SQL Injection Prevention
- Query validation before execution
- Parameterized queries support
- Multiple statement detection
- Dangerous keyword blocking

### Safe by Default
- Auto-execute is disabled by default
- User confirmation required for query execution
- Dangerous operations (DROP DATABASE, etc.) are blocked
- Comprehensive error handling

## Configuration

Copy `config.example.json` to `config.json` and customize:

```json
{
  "database": {
    "path": "database.db"
  },
  "lm_studio": {
    "base_url": "http://localhost:1234/v1",
    "timeout": 30
  },
  "security": {
    "auto_execute": false
  }
}
```

## Architecture

```
┌─────────────────┐
│   User Input    │
│ (Natural Lang)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  Nexus Spider   │─────▶│  LM Studio   │
│     Agent       │      │  (Local LLM) │
└────────┬────────┘      └──────────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│   DB Manager    │─────▶│   SQLite     │
│  (Validation)   │      │   Database   │
└─────────────────┘      └──────────────┘
```

## Components

- **NexusSpiderAgent**: Main orchestrator that coordinates LLM and database operations
- **LMStudioClient**: Handles communication with LM Studio's local API
- **DatabaseManager**: Secure SQLite database operations with validation
- **CLI**: Interactive command-line interface

## Troubleshooting

### "Failed to connect to LM Studio"
- Ensure LM Studio is running
- Check that a model is loaded in LM Studio
- Verify the server is started (check LM Studio's server tab)
- Confirm the URL is correct (default: http://localhost:1234)

### Queries Not Generating Correctly
- Try a different model in LM Studio (code-capable models work best)
- Be more specific in your natural language commands
- Provide schema context by running `/schema` first

### Permission Errors
- Check database file permissions
- Ensure the database directory is writable

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Privacy & Data

All processing happens locally on your machine:
- No data is sent to external servers
- No telemetry or tracking
- No API keys required
- Your database stays private

## Acknowledgments

- Built for use with [LM Studio](https://lmstudio.ai/)
- Inspired by the need for privacy-focused AI tools
