# Import the same orchestrated answer function used by the application.
from .main import answer_question

# Define representative questions and words expected in grounded answers.
test_cases = [
    {
        "question": "What do people think of the cheese pizza?", 
        "expected_keywords": ["cheese", "crust"]
     },
    {
        "question": "How’s the service quality?", 
        "expected_keywords": ["friendly", "slow", "attentive"]
    },
]
# Run each evaluation case independently so one result is easy to inspect.
for test in test_cases:

    # Generate an answer using the same orchestrator as the production app.
    result = answer_question(test["question"])

    # Print the question and generated answer for manual review.
    print(f"Q: {test['question']}\nA: {result}\n")

    # Perform a basic keyword check; this is a smoke test, not a quality score.
    for keyword in test["expected_keywords"]:
        # Report whether each expected concept appears in the model's response.
        print(f"✓ {keyword} in output: {keyword in result}")
    # Separate cases visually in the console output.
    print("\n---\n")
