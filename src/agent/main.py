"""Entry point for the pizza-review retrieval-augmented generation app."""

from typing import Any  # Allows type hints for provider agents and retrieved documents.

from .config import LLM_PROVIDER  # Reads the provider choice from environment configuration.
from .vector_store import retriever  # Provides similarity search over the review dataset.


def _load_agent() -> Any:
    """Load only the selected chat provider so unused credentials are not required."""
    # Import Bedrock only when selected, avoiding unnecessary client setup for other providers.
    if LLM_PROVIDER == "bedrock":
        from .providers.bedrock import agent
    # Import Azure only when selected, avoiding Azure credential requirements for other providers.
    elif LLM_PROVIDER == "azure":
        from .providers.azure import agent
    # Import OpenAI only when selected; it is the default provider.
    elif LLM_PROVIDER == "openai":
        from .providers.openai import agent
    # Reject typos in LLM_PROVIDER before attempting a model call.
    else:
        raise ValueError("LLM_PROVIDER must be one of: openai, azure, bedrock")
    # Return the configured LangChain agent used to generate the final answer.
    return agent


# These instructions keep the model grounded in retrieved reviews instead of general knowledge.
SYSTEM_INSTRUCTIONS = """You are a pizza review analyst.
Answer questions using only the restaurant review evidence supplied by the user.
Synthesize patterns across reviews, mention uncertainty when evidence is limited,
and include ratings or dates when they help. Do not invent restaurants, reviews,
or facts. If the evidence does not answer the question, say so clearly.
"""


def answer_question(question: str, reviews: list[Any] | None = None) -> str:
    """Retrieve evidence when needed, then ask the selected model to answer."""

    # Reuse supplied reviews during evaluation; otherwise search the vector store for this question.
    reviews = reviews or retriever.invoke(question)

    # Convert retrieved Documents into a readable evidence block for the chat model.
    evidence = "\n\n".join(
        f"Review {index}: {doc.page_content} "
        f"(rating: {doc.metadata.get('rating')}, date: {doc.metadata.get('date')})"
        for index, doc in enumerate(reviews, start=1)
    )

    # Combine behavior instructions, evidence, and the user's question into one grounded prompt.
    prompt = f"{SYSTEM_INSTRUCTIONS}\n\nReview evidence:\n{evidence}\n\nQuestion: {question}"

    # Create the provider agent and send it the prompt in the message format it expects.
    result = _load_agent().invoke({"messages": [{"role": "user", "content": prompt}]})

    # Return only the final assistant text, rather than the full LangChain message state.
    return result["messages"][-1].content


def main() -> None:
    # Define the sample question used when the command-line app starts.
    question = "What do customers say about the best pizza flavors, crusts, and value?"

    # Run retrieval plus generation and print the answer for the user.
    print(answer_question(question))


# Run main() only when this file is executed as the application, not when imported by eval.py.
if __name__ == "__main__":
    main()