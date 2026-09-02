# Technical Design

## Components

| Component | Responsibility |
| --- | --- |
| Orchestrator agent | Selects one specialist tool for each customer question. |
| Pizza-review specialist | Retrieves similar reviews from Chroma and creates an evidence-based answer. |
| Customer-support specialist | Drafts a concise response to an order issue. |
| Chroma | Persists embeddings and metadata for the local review dataset. |
| Provider model | Supplies chat and embeddings through OpenAI, Azure OpenAI, or Bedrock. |

## Routing rules

- Route flavor, crust, ingredient, quality, review, and value questions to `pizza_review_specialist`.
- Route late, cold, wrong, missing, damaged, refund, replacement, and complaint questions to `customer_support_specialist`.
- The orchestrator must call one specialist tool per customer question.

## Data flow

1. Load the restaurant review CSV.
2. Create embeddings and persist them in Chroma when the collection is empty.
3. Send a customer question to the orchestrator.
4. The orchestrator calls the selected specialist.
5. The pizza-review specialist retrieves the five most similar reviews before calling the chat model.
6. Return the specialist's answer to the user.

