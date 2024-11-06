import openai
import os

# Retrieve API key and endpoint from environment variables
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_id = "gpt-4o"  # Use the deployment ID from the PDF

# Set up OpenAI configuration
openai.api_key = api_key
openai.api_base = endpoint
openai.api_type = "azure"
openai.api_version = "2024-02-01"  # Use the API version specified in the PDF

# Test prompt
response = openai.ChatCompletion.create(
    deployment_id=deployment_id,  # Specify the deployment ID here
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Provide a summary of how AI helps with SQL data insights."}
    ]
)

# Print the response
print(response['choices'][0]['message']['content'])
