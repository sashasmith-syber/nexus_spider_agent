"""
Setup script for Nexus Spider Agent.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="nexus-spider-agent",
    version="0.1.0",
    author="Nexus Spider Agent Contributors",
    description="A lightweight, privacy-focused Python agent for managing SQLite databases with natural language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sashasmith-syber/nexus_spider_agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "nexus-spider=nexus_spider_agent.cli:main",
        ],
    },
    keywords="llm database sqlite natural-language privacy local ai",
    project_urls={
        "Bug Reports": "https://github.com/sashasmith-syber/nexus_spider_agent/issues",
        "Source": "https://github.com/sashasmith-syber/nexus_spider_agent",
    },
)
