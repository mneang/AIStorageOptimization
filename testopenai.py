import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and endpoint from environment variables
api_key = "39fa9771-399e-4640-b877-26c415ceb508"
endpoint = os.getenv("OPENAI_ENDPOINT")
deployment_id = "gpt-4o"

# Set up OpenAI configuration
openai.api_key = api_key
openai.api_base = endpoint
openai.api_type = "azure"
openai.api_version = "2024-02-01"

# Test prompt
response = openai.ChatCompletion.create(
    deployment_id=deployment_id,
    messages=[
        {"role": "system", "content": "You are a data insights assistant."},
        {"role": "user", "content": "Based on the sales data from October and early November, provide a sales forecast and inventory recommendations."}
    ]
)

# Print the response
print(response['choices'][0]['message']['content'])
