"""OpenAI model configuration."""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


# Expose a chat model so the application can create agents with task-specific prompts.
model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-5.4-nano"),
)
