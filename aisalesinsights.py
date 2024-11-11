import pyodbc
import openai
import gradio as gr
from collections import defaultdict
import os
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

# Function to connect to Azure SQL Database and fetch data with product names
def fetch_and_summarize_data():
    # Retrieve credentials from environment variables
    server = os.getenv("AZURE_SQL_SERVER")
    database = os.getenv("AZURE_SQL_DATABASE")
    username = os.getenv("AZURE_SQL_USERNAME")
    password = os.getenv("AZURE_SQL_PASSWORD")
    driver = "{ODBC Driver 18 for SQL Server}"
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

    # Connect to Azure SQL Database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Fetch sales data with product names
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
    response = openai.ChatCompletion.create(
        deployment_id=deployment_id,
        messages=[
            {"role": "system", "content": "You are a data insights assistant specializing in sales and inventory analysis. Provide actionable recommendations based on the summarized data."},
            {"role": "user", "content": summary}
        ]
    )
    return response['choices'][0]['message']['content']

# Gradio function
def chatbot(prompt):
    # Fetch and summarize data from SQL
    data_summary = fetch_and_summarize_data()
    # Generate AI insights
    ai_response = get_ai_insights(data_summary)
    return f"Data Summary:\n{data_summary}\n\nAI Insights:\n{ai_response}"

# Launch Gradio interface
gr.Interface(fn=chatbot, inputs="text", outputs="text", title="AI-Driven Sales & Inventory Insights").launch()