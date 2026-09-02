# Acceptance Criteria

## Review questions

- Given a question about pizza quality or menu value, the orchestrator calls the pizza-review specialist.
- The specialist retrieves review documents before generating an answer.
- The answer does not invent review evidence when none is supplied.

## Support questions

- Given a late, cold, missing, or incorrect order, the orchestrator calls the customer-support specialist.
- The answer acknowledges the issue and suggests a next step.
- The answer does not claim that a refund or replacement has already been issued.

## Quality checks

- Unit tests run without provider credentials, model calls, or embedding costs.
- The application runs with one configured provider: OpenAI, Azure OpenAI, or Amazon Bedrock.
- The review vector store persists locally and is not re-indexed when it already contains documents.
