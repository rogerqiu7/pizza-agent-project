"""Central configuration for file locations, providers, and embedding models."""

from pathlib import Path  # Builds filesystem paths in a platform-independent way.
import os  # Reads configuration values from environment variables.

from dotenv import load_dotenv  # Loads values from the local .env file.

load_dotenv()  # Makes local credentials and settings available through os.getenv().

# Find the repository root relative to this file so the app works from any current directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Use a configurable CSV path, with the included review dataset as the default.
DATA_PATH = Path(os.getenv("REVIEW_DATA_PATH", PROJECT_ROOT / "data" / "realistic_restaurant_reviews.csv"))

# Use a configurable local persistence directory for Chroma's vector database.
VECTOR_DB_PATH = Path(os.getenv("VECTOR_DB_PATH", PROJECT_ROOT / "data" / "chroma"))

# Select which supported chat/embedding provider to use; OpenAI is the default.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

# Choose the OpenAI embedding model used to turn review text into vectors.
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# Use a separate Azure embedding deployment when supplied, or reuse the chat deployment as a fallback.
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME",
    os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
)

# Choose the Bedrock embedding model when Bedrock is the selected provider.
BEDROCK_EMBEDDING_MODEL_ID = os.getenv(
    "BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"
)
