import pyodbc
import openai
import gradio as gr
import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI configuration
api_key = "39fa9771-399e-4640-b877-26c415ceb508"
endpoint = os.getenv("OPENAI_ENDPOINT")
deployment_id = "gpt-4o"

openai.api_key = api_key
openai.api_base = endpoint
openai.api_type = "azure"
openai.api_version = "2024-02-01"

# Function to connect to Azure SQL or SQLite and fetch data
def fetch_and_summarize_data():
    use_azure = os.getenv("USE_AZURE_SQL", "true").lower() == "true"

    if use_azure:
        try:
            # Retrieve Azure SQL credentials from environment variables
            server = os.getenv("AZURE_SQL_SERVER")
            database = os.getenv("AZURE_SQL_DATABASE")
            username = os.getenv("AZURE_SQL_USERNAME")
            password = os.getenv("AZURE_SQL_PASSWORD")
            driver = "{ODBC Driver 18 for SQL Server}"
            connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

            # Connect to Azure SQL Database
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
        except Exception as e:
            return f"Error connecting to Azure SQL: {e}"
    else:
        try:
            # Use SQLite for mock data
            conn = sqlite3.connect("mock_data.db")
            cursor = conn.cursor()

            # Create mock tables if they don't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Products (
                    ProductID INTEGER PRIMARY KEY,
                    ProductName TEXT,
                    UnitPrice REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS SalesTransactions (
                    TransactionID INTEGER PRIMARY KEY,
                    ProductID INTEGER,
                    Quantity INTEGER,
                    UnitPrice REAL,
                    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS InventoryLevels (
                    ProductID INTEGER PRIMARY KEY,
                    StockLevel INTEGER
                )
            """)

            # Insert mock data if tables are empty
            cursor.execute("SELECT COUNT(*) FROM Products")
            if cursor.fetchone()[0] == 0:
                cursor.executemany("INSERT INTO Products (ProductID, ProductName, UnitPrice) VALUES (?, ?, ?)", [
                    (1, 'Product A', 10.00),
                    (2, 'Product B', 20.00),
                    (3, 'Product C', 30.00)
                ])
                cursor.executemany("INSERT INTO SalesTransactions (TransactionID, ProductID, Quantity, UnitPrice) VALUES (?, ?, ?, ?)", [
                    (1, 1, 5, 10.00),
                    (2, 2, 3, 20.00),
                    (3, 3, 7, 30.00)
                ])
                cursor.executemany("INSERT INTO InventoryLevels (ProductID, StockLevel) VALUES (?, ?)", [
                    (1, 100),
                    (2, 150),
                    (3, 200)
                ])
                conn.commit()
        except Exception as e:
            return f"Error setting up SQLite: {e}"

    # Fetch sales data with product names
    try:
        cursor.execute("""
            SELECT p.ProductID, p.ProductName, SUM(st.Quantity) AS UnitsSold, 
                   SUM(st.Quantity * st.UnitPrice) AS TotalRevenue, il.StockLevel
            FROM SalesTransactions st
            JOIN Products p ON st.ProductID = p.ProductID
            JOIN InventoryLevels il ON p.ProductID = il.ProductID
            GROUP BY p.ProductID, p.ProductName, il.StockLevel
        """)
        sales_summary = cursor.fetchall()
        conn.close()
    except Exception as e:
        return f"Error fetching data: {e}"

    # Format the sales summary
    formatted_summary = "### Sales and Inventory Summary:\n"
    for row in sales_summary:
        product_id, product_name, units_sold, total_revenue, stock_level = row
        formatted_summary += (
            f"- Product: {product_name} (ID: {product_id})\n"
            f"  - Units Sold: {units_sold}\n"
            f"  - Total Revenue: ${total_revenue:.2f}\n"
            f"  - Stock Level: {stock_level}\n\n"
        )

    return formatted_summary

# Function to get AI insights based on the summary
def get_ai_insights(summary):
    try:
        response = openai.ChatCompletion.create(
            deployment_id=deployment_id,
            messages=[
                {"role": "system", "content": "You are a data insights assistant specializing in sales and inventory analysis. Provide actionable recommendations based on the summarized data."},
                {"role": "user", "content": summary}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error with AI insights: {e}"

# Gradio function
def chatbot(prompt):
    # Fetch and summarize data from SQL or SQLite
    data_summary = fetch_and_summarize_data()
    # Generate AI insights
    ai_response = get_ai_insights(data_summary)
    return f"Data Summary:\n{data_summary}\n\nAI Insights:\n{ai_response}"

# Launch Gradio interface
gr.Interface(fn=chatbot, inputs="text", outputs="text", title="AI-Driven Sales & Inventory Insights").launch()