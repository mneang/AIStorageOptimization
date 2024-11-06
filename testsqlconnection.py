import pyodbc
import os

# Retrieve environment variables for SQL Server credentials
server = os.getenv("AZURE_SQL_SERVER")  # e.g., "your_server.database.windows.net"
database = os.getenv("AZURE_SQL_DATABASE")  # e.g., "HackathonSQLDB"
username = os.getenv("AZURE_SQL_USERNAME")
password = os.getenv("AZURE_SQL_PASSWORD")
driver = "{ODBC Driver 18 for SQL Server}"

# Connection string
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Connect to Azure SQL Database
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Execute a sample query
cursor.execute("SELECT * FROM customers")  # Replace 'your_table' with an actual table name
for row in cursor:
    print(row)

conn.close()
