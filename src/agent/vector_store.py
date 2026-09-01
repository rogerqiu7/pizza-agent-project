"""Load reviews, index them in Chroma, and expose a similarity retriever."""

import os  # Reads required Azure credentials for Azure embeddings.
import pandas as pd  # Reads the CSV review dataset into rows.
from .config import (
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
    BEDROCK_EMBEDDING_MODEL_ID,
    DATA_PATH,
    LLM_PROVIDER,
    OPENAI_EMBEDDING_MODEL,
    VECTOR_DB_PATH,
)
from langchain_chroma import Chroma  # Stores vectors and performs similarity searches.
from langchain_core.documents import Document  # Represents review text plus metadata.
from langchain_aws import BedrockEmbeddings  # Creates embeddings through Amazon Bedrock.
from langchain_openai import OpenAIEmbeddings  # Creates embeddings through OpenAI-compatible APIs.

# Read the source reviews once when this module is imported.
df = pd.read_csv(DATA_PATH)

def _get_embeddings():
    """Create embeddings using the provider selected in the environment."""

    # OpenAI embeddings use OPENAI_API_KEY loaded by the provider SDK.
    if LLM_PROVIDER == "openai":
        return OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    
    # Azure exposes an OpenAI-compatible embeddings API, so the OpenAI wrapper is reused.
    if LLM_PROVIDER == "azure":
        return OpenAIEmbeddings(
            model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
            base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
        )
    # Bedrock has its own LangChain embedding implementation and AWS credential discovery.
    if LLM_PROVIDER == "bedrock":
        return BedrockEmbeddings(model_id=BEDROCK_EMBEDDING_MODEL_ID)
    
    # Fail early with a useful message instead of failing later during retrieval.
    raise ValueError("LLM_PROVIDER must be one of: openai, azure, bedrock")

# Connect to (or create) the persistent review collection.
vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=VECTOR_DB_PATH,
    embedding_function=_get_embeddings(),
)

# Index the CSV only when the collection is empty, preventing duplicate reviews on later runs.
add_documents = not vector_store.get()["ids"]

# Build Chroma documents only on the first run.
if add_documents:
    # Keep the text and IDs separate because Chroma needs both when inserting records.
    documents = []
    ids = []
    
    # Convert every CSV row into searchable text plus filterable metadata.
    for i, row in df.iterrows():
        document = Document(
            page_content=f"{row['Title']}. {row['Review']}",
            metadata={"rating": row["Rating"], "date": row["Date"]},
        )
        ids.append(str(i))
        documents.append(document)

    # Insert one document at a time to keep embedding requests simple and reliable.
    for doc, id_ in zip(documents, ids):
        vector_store.add_documents(documents=[doc], ids=[id_])

# Wrap the vector store so each question retrieves its five most similar reviews.
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)
