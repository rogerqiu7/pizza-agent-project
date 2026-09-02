# Product Requirements

## Problem

A pizza restaurant needs a simple assistant that can answer review-based questions and respond appropriately when an order goes wrong.

## Users

- Customers asking about pizza quality, flavors, crust, ingredients, or value.
- Customers reporting a late, cold, missing, damaged, or incorrect order.

## Functional requirements

1. The app must accept one customer question at a time.
2. It must route review questions to a pizza-review specialist.
3. It must route order-problem questions to a customer-support specialist.
4. Review answers must use retrieved historic review evidence.
5. Support answers must be empathetic and suggest a realistic next step without making guarantees.
6. The app must support OpenAI, Azure OpenAI, or Amazon Bedrock through configuration.

## Out of scope

- Placing refunds, replacements, or orders.
- Saving customer personal data or support tickets.
- Live delivery tracking.

