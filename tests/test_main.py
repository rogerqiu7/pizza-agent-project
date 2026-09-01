"""Offline unit tests for the multi-agent helpers."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from agent import main


class MainTests(unittest.TestCase):
    """Test prompt construction and agent handoffs without calling real providers."""

    def test_format_reviews_includes_text_and_metadata(self) -> None:
        review = SimpleNamespace(
            page_content="Excellent cheese pizza.",
            metadata={"rating": 5, "date": "2024-03-15"},
        )

        evidence = main.format_reviews([review])

        self.assertIn("Excellent cheese pizza.", evidence)
        self.assertIn("rating: 5", evidence)
        self.assertIn("date: 2024-03-15", evidence)

    def test_pizza_specialist_retrieves_and_uses_reviews(self) -> None:
        review = SimpleNamespace(
            page_content="Crispy crust and great pepperoni.",
            metadata={"rating": 5, "date": "2024-03-15"},
        )
        fake_agent = Mock()
        fake_agent.invoke.return_value = {
            "messages": [SimpleNamespace(content="Customers praise the crispy crust.")]
        }
        fake_retriever = Mock()
        fake_retriever.invoke.return_value = [review]

        with patch.object(main, "pizza_review_agent", fake_agent), patch.object(
            main, "retriever", fake_retriever
        ):
            answer = main.pizza_review_specialist.invoke({"question": "How is the crust?"})

        fake_retriever.invoke.assert_called_once_with("How is the crust?")
        self.assertEqual(answer, "Customers praise the crispy crust.")
        self.assertIn("Crispy crust", fake_agent.invoke.call_args.args[0]["messages"][0]["content"])

    def test_orchestrator_handles_questions_without_reviews(self) -> None:
        fake_orchestrator = Mock()
        fake_orchestrator.invoke.return_value = {
            "messages": [SimpleNamespace(content="I can help with that order issue.")]
        }

        with patch.object(main, "orchestrator_agent", fake_orchestrator):
            answer = main.answer_question("My order arrived cold.")

        self.assertEqual(answer, "I can help with that order issue.")
        self.assertEqual(
            fake_orchestrator.invoke.call_args.args[0]["messages"][0]["content"],
            "My order arrived cold.",
        )


if __name__ == "__main__":
    unittest.main()
