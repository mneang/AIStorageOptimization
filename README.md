# SmartAIventory: AI-Enhanced Sales Forecasting and Inventory Optimization

**SmartAIventory** is a cutting-edge solution built to revolutionize retail analytics. By leveraging **Microsoft Fabric**, **Azure SQL**, **Power BI**, and **Gradio** with **Azure OpenAI**, our project empowers businesses to make **data-driven decisions that minimize inventory risks and maximize sales opportunities**. 


---

## 1. Introduction

In the fast-paced world of retail, balancing inventory with demand is crucial. Overstock leads to wasted resources, while stockouts result in missed sales opportunities. SmartAIventory bridges this gap, turning raw data into actionable insights, allowing businesses to stay one step ahead. 

Our seamless integration of Microsoft’s data processing tools with AI-driven analytics ensures that retailers can make informed decisions that drive profitability and customer satisfaction.


---

## 2. Problem Statement & Objective

### The Challenge
Retailers often grapple with predicting demand and managing inventory efficiently. Mismanagement can lead to substantial revenue losses. 

### Our Solution
SmartAIventory addresses this by providing:
- **Accurate Sales Forecasts**: Leveraging historical data to anticipate future trends.
- **Optimized Inventory Management**: Strategic recommendations to prevent overstock and stockouts.

*Note: This is not just a dashboard; it’s a comprehensive solution designed to transform retail analytics.*


---

## 3. Technology Architecture Overview

### Core Technologies
- **Microsoft Fabric**: For seamless data ingestion and processing, leveraging the strengths of Synapse Analytics and Azure SQL.
- **Azure SQL Database**: Secure and centralized storage of sales and inventory data.
- **Power BI**: Interactive visualizations that provide actionable insights for decision-makers.
- **Gradio + Azure OpenAI**: An intuitive interface for generating AI-driven insights using natural language.

### Why We Chose Batch Processing
Our decision to use batch processing was deliberate and based on the real-world needs of retail analytics. While real-time data processing is often hyped, it introduces unnecessary complexity and cost when the source systems themselves only update at intervals (e.g., daily or hourly). 

**Batch Processing Advantages:**
- **Optimal Efficiency**: Since retail data, such as sales transactions and inventory updates, typically refresh at set intervals, batch processing ensures that we efficiently process large volumes of data without straining system resources.
- **Cost-Effectiveness**: Maintaining real-time analytics infrastructure can be expensive and over-engineered for most retail scenarios. Batch processing strikes the right balance, providing timely insights without unnecessary overhead.
- **Scalability**: Our architecture is designed to scale effortlessly as data volumes increase, handling everything from daily sales summaries to monthly inventory forecasts.

> *“In retail, it’s not about having data every second—it’s about having the right insights at the right time. Batch processing allows us to deliver this, maximizing impact while minimizing complexity.”*

*Note: The flexibility of our architecture means we can seamlessly integrate real-time components in the future if business needs evolve.*

### Data Flow Diagram
![aistoragearchitecture drawio](https://github.com/user-attachments/assets/07d6c7c8-8aaf-4175-89fb-0940896a978e)
*Figure: SmartAIventory architecture leveraging Microsoft Fabric for data processing and analytics, integrated with AI-driven insights through Gradio and Azure OpenAI.*

### Database Schema
The following ERD (Entity-Relationship Diagram) illustrates how our data is structured in the Azure SQL Database:

![Database_Schema_HackathonDB](https://github.com/user-attachments/assets/504bb060-94f1-4635-b02a-ac5884fc6784)

The schema highlights key relationships:
- **Customers**: Stores customer information and regions.
- **Products**: Captures product details and pricing.
- **SalesTransactions**: Links customers and products to record sales, with calculated fields for revenue.
- **InventoryLevels**: Manages stock levels for each product, linked via ProductID.

This schema ensures that our data is well-organized and optimized for efficient querying and analysis, which is pivotal for generating actionable insights.


---

## 4. Setup Guide

### Prerequisites
- **Azure Account**: Access to Microsoft Fabric, Synapse Pipelines, and Azure SQL.
- **Python Environment**: For running the Gradio-based AI insights interface.
- **Power BI**: Use either Power BI Desktop or connect via a browser.

### Step-by-Step Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/username/SmartAIventory.git
   cd SmartAIventory

### Step-by-Step Setup

2. **Environment Configuration**
   - Create a `.env` file in the root directory and add your Azure and OpenAI credentials:
     ```plaintext
     AZURE_SQL_SERVER=your_server_name
     AZURE_SQL_DATABASE=your_database_name
     AZURE_SQL_USERNAME=your_username
     AZURE_SQL_PASSWORD=your_password
     OPENAI_API_KEY=your_openai_api_key
     OPENAI_API_ENDPOINT=your_openai_api_endpoint
     ```

3. **Run the Synapse Pipeline**
   - Access Microsoft Fabric and run the Synapse Pipeline to ingest data.
   - Our Synapse Pipeline uses batch processing to efficiently ingest and transform data. This method is optimal for retail scenarios where data updates occur on a regular schedule, ensuring timely and impactful insights without the overhead of real-time analytics.
   ![Screenshot 2024-11-07 at 10 16 15 PM](https://github.com/user-attachments/assets/3fc5276b-0574-4062-b155-bc95110fd5f9)
   *Figure: Azure Synapse Pipeline: Sequential data copy from SalesTransactions, Products, to InventoryLevels.*

4. **Connect Power BI**
   - Open Power BI and connect to your Azure SQL Database.
   - *Screenshot*: Show the data connection setup and highlight the dashboard features.
  
5. **Launch the Gradio Chatbot (See below section for more details)**
   - Run the Gradio interface for AI insights using the following command:
     ```bash
     python aisalesinsights.py
     ```
   - *Screenshot*: Capture the chatbot in action with a sample query and insightful response.
   
### Launching and Using the Gradio Chatbot
1. **Ensure Dependencies Are Installed**:
   - Make sure you have all necessary Python packages installed. If not, run:
     ```bash
     pip install -r requirements.txt
     ```
2. **Run the Gradio Interface**:
   - Navigate to the project directory in your terminal and execute:
     ```bash
     python testopenai.py
     ```
3. **Interacting with the Chatbot**:
   - The Gradio interface will open in your default web browser.
   - **Input**: Type in queries like, *“What are the sales trends for October?”* or *“Which products need urgent restocking?”*
   - **Output**: The AI assistant will generate tailored recommendations based on the data.
4. **Stopping the Interface**:
   - To stop the Gradio server, return to your terminal and press `CTRL + C`.


---

## 5. Data Processing & Pipeline

### Data Overview
Our solution leverages synthetic data to mimic real-world scenarios, covering:
- **Sales Transactions**: Capturing key details like date, product, quantity, and revenue.
- **Inventory Levels**: Reflecting stock statuses for efficient supply management.


Our solution utilizes efficient data processing to derive actionable insights. Here’s an example of a critical query used in our analysis:

### Monthly Demand Forecast Query
To forecast product demand and aid in strategic inventory planning, we use the following SQL query:

```sql
SELECT 
    ProductID, 
    DATEPART(MONTH, TransactionDate) AS Month, 
    SUM(Quantity) AS TotalSales
FROM 
    SalesTransactions
GROUP BY 
    ProductID, DATEPART(MONTH, TransactionDate)
ORDER BY 
    ProductID, Month;
```

### Pipeline Functionality
Using batch processing, our Synapse Pipeline efficiently handles data ingestion and transformation, preparing it for analysis and ensuring high-quality output.


---

## 6. Power BI Dashboard Insights

### Main Dashboard Features
1. **Total Sales Overview**: Key metrics such as total revenue and units sold.
2. **Sales Trends Line Chart**: Visual representation of sales performance over the month.
3. **Top Products & Inventory Levels**: Insightful visuals showcasing best sellers and stock status.

### User-Centric Design
Designed with business leaders in mind, the dashboard is intuitive, providing easy-to-understand visuals that drive decision-making.

![2024-11-09_21h12_25](https://github.com/user-attachments/assets/dd802589-04d6-4717-8480-73547f25ae84)


---

## 7. AI Insights & Recommendations

Our AI-powered Gradio Chatbot delivers actionable insights based on sales and inventory data. Here’s how it simplifies complex data for business decision-makers:

### Example Interactions:
- **Prompt**: "Analyze the sales trends for October and suggest inventory adjustments for November."
  - **Response**: 
    - **Best-Selling Products**: ProductID 6 (Gaming Laptop) - 15 units sold, $14,999.85 in revenue.
    - **Recommendations**: Maintain high stock levels for ProductID 6 to avoid stockouts.
- **Prompt**: "Which products should we focus on promoting in November?"
  - **Response**:
    - **Slow-Moving Items**: ProductID 8 (Ergonomic Office Chair) - Low sales, consider running promotions or bundling offers.
    - **Promotional Strategy**: Implement targeted discounts to increase demand.

### How to Use the AI Chatbot:
1. **Launch the Gradio Interface**:
   - Navigate to the project directory and run:
     ```bash
     python aisalesinsights.py
     ```
2. **Interact with the Chatbot**:
   - Input natural language queries, such as:
     - "What are the key sales trends for October?"
     - "Provide inventory recommendations for November."
   - The AI will analyze the data and provide clear, actionable recommendations.
3. **Sample Output**:
  ![Screen Recording 2024-11-10 at 4 22 43 PM](https://github.com/user-attachments/assets/5eec5743-716b-438a-8fee-23e60ce2804d)
*Figure:* Demonstration of the Gradio AI Chatbot responding to the query "What are the key sales trends for October?" and providing structured data insights and actionable recommendations.

### Why It’s User-Friendly:
- **Natural Language Queries**: No need for complex SQL queries. Simply ask questions in plain English.
- **Actionable Insights**: The AI summarizes data trends and suggests practical strategies, making it easy for decision-makers to act.
- **Clear Visuals**: Easy-to-read tables and bullet points ensure the insights are digestible.

### AI Insights: Keeping It Clear and Actionable

When it comes to AI-driven recommendations, clarity is king. Here’s how **SmartAIventory** delivers:

1. **Best-Selling Products**: Our insights don't just highlight what's selling; they provide concrete suggestions to keep momentum strong. For example, “Product X is flying off the shelves—consider a stock increase to meet growing demand.”
2. **Slow Movers**: Instead of leaving retailers wondering, we pinpoint underperforming items and suggest actionable next steps. Whether it's promotional pricing or strategic bundling, our AI ensures businesses have a game plan.
3. **Seasonal Adjustments**: We make complex seasonal patterns simple. Clear forecasts give businesses the edge to plan ahead, ensuring the right products are available when customers need them most.

By presenting AI insights this way, **SmartAIventory** transforms data complexity into business clarity, empowering stakeholders to make confident, data-driven decisions.

---

### 8. Business Value & Key Insights

**Tangible Business Impact**  
SmartAIventory’s predictive analytics and AI-driven insights are designed to deliver measurable results, helping businesses make informed decisions in an unpredictable retail landscape. Here’s the potential impact for a mid-sized retail chain:

- **Reduced Overstock Costs**: By optimizing inventory levels, businesses can decrease overstock costs by up to 15%, translating to substantial savings. *Context*: Excess inventory ties up capital and can lead to significant markdown losses.
- **Increased Revenue**: Leveraging accurate sales forecasting can boost revenue by up to 10% through better stock availability and improved customer satisfaction. *Context*: Meeting customer demand efficiently leads to higher retention rates and market competitiveness.
- **Efficiency Gains**: Automating inventory analysis and recommendations reduces manual effort, allowing teams to focus on strategic initiatives, leading to a 20% increase in operational efficiency. *Context*: Streamlined operations free up resources for innovation and expansion.

These metrics underscore how SmartAIventory can transform inventory management into a strategic advantage, improving both top-line and bottom-line performance while future-proofing businesses in a dynamic market.

---

## 9. Challenges & Solutions

### Integration Complexity
Integrating multiple Microsoft services was challenging but ultimately rewarding, enhancing our understanding of data ecosystems.

### Data Limitations
We overcame the challenge of using synthetic data by designing our architecture to scale effortlessly for real-world scenarios.

---

## 10. Future Potential & Scalability

### Real-Time Data Integration
The next iteration will feature real-time data processing, enhancing the immediacy of insights.

### Advanced AI Models
Future updates will incorporate more sophisticated models to refine forecasting and analysis further.

---

## 11. Caveats & Assumptions

### Data Quality
Our solution assumes consistent and accurate data input. Real-world deployment would require continuous monitoring.

### Use Case Focus
While tailored for retail, our solution is versatile and can be adapted to other industries with similar needs.
