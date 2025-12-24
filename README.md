<div align="center">

# 🕷️ Nexus Spider Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

*A lightweight, privacy-focused Python agent that connects to locally running LLMs in LM Studio to interpret natural language commands, generate SQL queries, and securely manage SQLite databases.*

[Features](#-features) •
[Installation](#-installation) •
[Usage](#-usage) •
[Documentation](#-documentation) •
[Contributing](#-contributing) •
[License](#-license)

</div>

---

## 🌟 Features

- **🔒 Privacy-First**: All processing happens locally with your own LLM - no data leaves your machine
- **🤖 Natural Language Interface**: Interact with databases using plain English commands
- **⚡ LM Studio Integration**: Seamlessly connects to locally running LLMs via LM Studio
- **🗃️ SQLite Management**: Secure and efficient SQLite database operations
- **🛡️ Safe Query Generation**: Built-in safeguards for SQL query validation
- **📊 Database Insights**: Get intelligent insights about your data structure and content

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **LM Studio** - [Download LM Studio](https://lmstudio.ai/)
- **SQLite3** - Usually pre-installed with Python

## 🚀 Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/sashasmith-syber/nexus_spider_agent.git

# Navigate to the project directory
cd nexus_spider_agent

# Install dependencies (once available)
pip install -r requirements.txt

# Run the agent
python nexus_spider_agent.py
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/sashasmith-syber/nexus_spider_agent.git
cd nexus_spider_agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
```

## 💡 Usage

### Basic Example

```python
from nexus_spider_agent import NexusAgent

# Initialize the agent
agent = NexusAgent(
    lm_studio_url="http://localhost:1234",
    database_path="./my_database.db"
)

# Execute natural language queries
response = agent.query("Show me all users who registered last month")
print(response)

# Get database insights
insights = agent.analyze_database()
print(insights)
```

### Advanced Usage

```python
# Connect to specific LLM model
agent = NexusAgent(
    lm_studio_url="http://localhost:1234",
    model_name="mistral-7b-instruct",
    database_path="./my_database.db",
    safety_mode=True
)

# Execute complex queries
result = agent.query("""
    Find the average purchase amount for customers 
    who made more than 5 orders in the last quarter
""")
```

## 📚 Documentation

### Core Components

- **NexusAgent**: Main interface for interacting with the agent
- **QueryParser**: Interprets natural language and generates SQL
- **DatabaseManager**: Handles secure database operations
- **LLMConnector**: Manages communication with LM Studio

### Configuration

Create a `config.yaml` file to customize the agent:

```yaml
lm_studio:
  url: "http://localhost:1234"
  model: "mistral-7b-instruct"
  timeout: 30

database:
  path: "./data/database.db"
  read_only: false
  
safety:
  enabled: true
  max_query_length: 1000
  allowed_operations: ["SELECT", "INSERT", "UPDATE"]
```

## 🛠️ Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=nexus_spider_agent

# Run specific test file
pytest tests/test_query_parser.py
```

### Code Style

This project uses [Black](https://github.com/psf/black) for code formatting and [Flake8](https://flake8.pycqa.org/) for linting.

```bash
# Format code
black .

# Run linter
flake8 nexus_spider_agent/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to:

- Report bugs
- Suggest features
- Submit pull requests
- Follow our code of conduct

## 🔒 Security

Security is a top priority. If you discover a security vulnerability, please follow our [Security Policy](SECURITY.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LM Studio](https://lmstudio.ai/) - For providing an excellent local LLM runtime
- The open-source community for inspiration and tools
- All contributors who help improve this project

## 📞 Support

- 📫 **Issues**: [GitHub Issues](https://github.com/sashasmith-syber/nexus_spider_agent/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/sashasmith-syber/nexus_spider_agent/discussions)

## 🗺️ Roadmap

- [ ] Multi-database support (PostgreSQL, MySQL)
- [ ] Web UI dashboard
- [ ] Query history and caching
- [ ] Advanced security features
- [ ] API endpoint support
- [ ] Cloud LLM integration (optional)

---

<div align="center">

**Made with ❤️ by the Nexus Spider Agent Team**

⭐ Star this repository if you find it helpful!

</div>
