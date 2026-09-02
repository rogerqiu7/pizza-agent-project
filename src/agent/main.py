"""Multi-agent pizza review and customer-support application."""

from typing import Any

from langchain.agents import create_agent
from langchain.tools import tool

from .config import LLM_PROVIDER
from .vector_store import retriever


def _load_model() -> Any:
    """Return the chat model selected by LLM_PROVIDER."""
    if LLM_PROVIDER == "bedrock":
        from .providers.bedrock import model
    elif LLM_PROVIDER == "azure":
        from .providers.azure import model
    elif LLM_PROVIDER == "openai":
        from .providers.openai import model
    else:
        raise ValueError("LLM_PROVIDER must be one of: openai, azure, bedrock")
    return model


def _message_text(result: dict[str, Any]) -> str:
    """Extract the final assistant response from LangChain agent state."""
    return result["messages"][-1].content


def format_reviews(reviews: list[Any]) -> str:
    """Turn retrieved review Documents into evidence the review agent can cite."""
    return "\n\n".join(
        f"Review {index}: {doc.page_content} "
        f"(rating: {doc.metadata.get('rating')}, date: {doc.metadata.get('date')})"
        for index, doc in enumerate(reviews, start=1)
    )


model = _load_model()

# This agent analyzes only retrieved restaurant-review evidence.
pizza_review_agent = create_agent(
    model=model,
    tools=[],
    system_prompt="""You are a pizza review specialist.
Answer using only the supplied review evidence. Summarize patterns, mention
ratings or dates when useful, and say when the evidence is insufficient.
Do not invent restaurants, reviews, or facts.""",
)

# This agent handles operational issues rather than review-analysis questions.
customer_support_agent = create_agent(
    model=model,
    tools=[],
    system_prompt="""You are a pizza restaurant customer-support specialist.
Respond with empathy, briefly acknowledge the problem, suggest a practical next
step such as a replacement, refund, or escalation, and do not promise actions
you cannot actually perform. Keep the response concise and customer-friendly.""",
)


@tool
def pizza_review_specialist(question: str) -> str:
    """Use for questions about pizza flavors, ingredients, quality, value, or reviews."""
    reviews = retriever.invoke(question)
    evidence = format_reviews(reviews)
    prompt = f"Review evidence:\n{evidence}\n\nQuestion: {question}"
    result = pizza_review_agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    return _message_text(result)


@tool
def customer_support_specialist(issue: str) -> str:
    """Use for a wrong, missing, cold, late, damaged, or otherwise incorrect order."""
    prompt = f"Customer issue: {issue}"
    result = customer_support_agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    return _message_text(result)


# The orchestrator selects exactly one specialist tool based on the user's intent.
orchestrator_agent = create_agent(
    model=model,
    tools=[pizza_review_specialist, customer_support_specialist],
    system_prompt="""You are the pizza restaurant orchestrator.
Route questions about pizza quality, flavors, menu value, or customer reviews to
pizza_review_specialist. Route problems with an order, delivery, missing items,
refunds, replacements, or complaints to customer_support_specialist.
Call exactly one specialist tool, then present its answer to the user.""",
)


def answer_question(question: str) -> str:
    """Send a customer question to the orchestrator for routing."""
    result = orchestrator_agent.invoke({"messages": [{"role": "user", "content": question}]})
    return _message_text(result)


def main() -> None:
    """Run one sample question when the `agent` command is executed."""
    question = "my order never came"
    print(answer_question(question))


if __name__ == "__main__":
    main()
