import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
server = os.getenv("AZURE_SQL_SERVER")
database = os.getenv("AZURE_SQL_DATABASE")
username = os.getenv("AZURE_SQL_USERNAME")
password = os.getenv("AZURE_SQL_PASSWORD")
driver = "{ODBC Driver 18 for SQL Server}"

# Connection string
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Connect to Azure SQL Database
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Execute a sample query
cursor.execute("SELECT * FROM customers")
for row in cursor:
    print(row)

conn.close()
