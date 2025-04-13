"""
Configuration settings for the MSSQL Database Analyzer
"""

# Database connection settings
DB_CONFIG = {
    "username": "sa",
    "password": "123",
    "server": "NUCBOX\\SQLEXPRESS",
    "database": "Aghna_contracting_2025",
    "driver": "ODBC Driver 17 for SQL Server"
}

# Ollama settings
OLLAMA_API = "http://localhost:11434/api"
DEFAULT_MODEL = "llama3"
RECOMMENDED_MODELS = ["llama3", "codellama", "mistral"]

# Application settings
SAMPLE_LIMIT = 10  # Number of sample rows to fetch per table
HISTORY_ENABLED = True
