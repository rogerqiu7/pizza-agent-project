from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://rogerqiu-7379-resource.services.ai.azure.com/mai/v1"
deployment_name = "MAI-Thinking-1"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

openai_client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

response = openai_client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "system",
            "content": "You are an AI assistant.",
        },
        {
            "role": "user",
            "content": "What are three major announcements from Microsoft Build this week?",
        },
    ],
)

print(response.choices[0].message.content)
