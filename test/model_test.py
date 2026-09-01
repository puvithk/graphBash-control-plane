import unittest
from unittest.mock import MagicMock, patch
import os
from pydantic import BaseModel, Field

from app.agent.utils.models import ChatLLM, GroqLLM
from app.core import config


class SampleOutputSchema(BaseModel):
    intent: str = Field(description="The detected intent")
    confidence: float = Field(description="Confidence score between 0 and 1")


class TestGroqLLM(unittest.TestCase):
    """Unit test suite for GroqLLM wrapper."""

    @patch("app.agent.utils.models.ChatGroq")
    def test_initialization_default_model(self, mock_chat_groq):
        model = GroqLLM()
        self.assertEqual(model.model_provider(), "groq")
        mock_chat_groq.assert_called_once_with(
            model="llama-3.1-8b-instant",
            verbose=True,
            max_tokens=1000,
            temperature=0.7,
            api_key=config.GROQ_API_KEY,
        )

    @patch("app.agent.utils.models.ChatGroq")
    def test_initialization_custom_model(self, mock_chat_groq):
        custom_model_name = "llama-3.3-70b-versatile"
        model = GroqLLM(model=custom_model_name)
        mock_chat_groq.assert_called_once_with(
            model=custom_model_name,
            verbose=True,
            max_tokens=1000,
            temperature=0.7,
            api_key=config.GROQ_API_KEY,
        )

    @patch("app.agent.utils.models.ChatGroq")
    def test_invoke(self, mock_chat_groq):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = "System status: Healthy"
        mock_chat_groq.return_value = mock_instance

        groq_llm = GroqLLM()
        result = groq_llm.invoke("What is the system status?")

        mock_instance.invoke.assert_called_once_with("What is the system status?")
        self.assertEqual(result, "System status: Healthy")

    @patch("app.agent.utils.models.ChatGroq")
    def test_with_structured_output(self, mock_chat_groq):
        mock_instance = MagicMock()
        mock_structured_llm = MagicMock()
        mock_instance.with_structured_output.return_value = mock_structured_llm
        mock_chat_groq.return_value = mock_instance

        groq_llm = GroqLLM()
        structured_llm = groq_llm.with_structured_output(SampleOutputSchema)

        mock_instance.with_structured_output.assert_called_once_with(SampleOutputSchema)
        self.assertEqual(structured_llm, mock_structured_llm)


class TestChatLLM(unittest.TestCase):
    """Unit test suite for ChatLLM factory, retries, and structured output."""

    @patch("app.agent.utils.models.GroqLLM")
    def test_chat_llm_default_initialization(self, mock_groq_llm):
        chat = ChatLLM()
        self.assertEqual(chat.llm_provider, "groq")
        self.assertEqual(chat.llm_model, "llama-3.1-8b-instant")
        mock_groq_llm.assert_called_once_with("llama-3.1-8b-instant")

    @patch("app.agent.utils.models.GroqLLM")
    def test_chat_llm_custom_initialization(self, mock_groq_llm):
        chat = ChatLLM(llm_provider="groq", llm_model="llama-3.3-70b-versatile")
        self.assertEqual(chat.llm_provider, "groq")
        self.assertEqual(chat.llm_model, "llama-3.3-70b-versatile")
        mock_groq_llm.assert_called_once_with("llama-3.3-70b-versatile")

    def test_unsupported_provider_raises_error(self):
        with self.assertRaises(ValueError) as ctx:
            ChatLLM(llm_provider="unsupported_provider")
        self.assertIn("LLM Provider is not supported", str(ctx.exception))

    @patch("app.agent.utils.models.GroqLLM")
    def test_invoke_success(self, mock_groq_llm):
        mock_model_instance = MagicMock()
        mock_model_instance.invoke.return_value = "Response from LLM"
        mock_groq_llm.return_value = mock_model_instance

        chat = ChatLLM()
        response = chat.invoke("Explain CPU metrics")

        self.assertEqual(response, "Response from LLM")
        mock_model_instance.invoke.assert_called_once_with("Explain CPU metrics")

    @patch("app.agent.utils.models.GroqLLM")
    def test_invoke_retry_and_succeed(self, mock_groq_llm):
        mock_model_instance = MagicMock()
        # Simulate failure on first call, success on second call
        mock_model_instance.invoke.side_effect = [
            RuntimeError("Temporary network timeout"),
            "Recovered response",
        ]
        mock_groq_llm.return_value = mock_model_instance

        chat = ChatLLM()
        response = chat.invoke("Test prompt")

        self.assertEqual(response, "Recovered response")
        self.assertEqual(mock_model_instance.invoke.call_count, 2)

    @patch("app.agent.utils.models.GroqLLM")
    def test_invoke_failure_max_retries_exceeded(self, mock_groq_llm):
        mock_model_instance = MagicMock()
        mock_model_instance.invoke.side_effect = RuntimeError("Service unavailable")
        mock_groq_llm.return_value = mock_model_instance

        chat = ChatLLM()
        with self.assertRaises(ValueError) as ctx:
            chat.invoke("Test prompt")

        self.assertIn("LLM Error Service unavailable", str(ctx.exception))
        self.assertEqual(mock_model_instance.invoke.call_count, config.MAX_LLM_TRIES)

    @patch("app.agent.utils.models.GroqLLM")
    def test_invoke_with_structured_output_success(self, mock_groq_llm):
        mock_model_instance = MagicMock()
        mock_structured_llm = MagicMock()
        parsed_obj = SampleOutputSchema(intent="check_health", confidence=0.98)
        mock_structured_llm.invoke.return_value = parsed_obj
        mock_model_instance.with_structured_output.return_value = mock_structured_llm
        mock_groq_llm.return_value = mock_model_instance

        chat = ChatLLM()
        result = chat.invoke_with_structured_output("Check server health", SampleOutputSchema)

        self.assertEqual(result, parsed_obj.model_dump_json())
        mock_model_instance.with_structured_output.assert_called_once_with(SampleOutputSchema)
        mock_structured_llm.invoke.assert_called_once_with("Check server health")

    @patch("app.agent.utils.models.GroqLLM")
    def test_invoke_with_structured_output_failure(self, mock_groq_llm):
        mock_model_instance = MagicMock()
        mock_structured_llm = MagicMock()
        mock_structured_llm.invoke.side_effect = ValueError("Schema validation error")
        mock_model_instance.with_structured_output.return_value = mock_structured_llm
        mock_groq_llm.return_value = mock_model_instance

        chat = ChatLLM()
        with self.assertRaises(ValueError) as ctx:
            chat.invoke_with_structured_output("Invalid input", SampleOutputSchema)

        self.assertIn("LLM Error Schema validation error", str(ctx.exception))
        self.assertEqual(mock_structured_llm.invoke.call_count, config.MAX_LLM_TRIES)


class TestLiveModelIntegration(unittest.TestCase):
    """Integration test suite for live API testing when GROQ_API_KEY is available."""

    @unittest.skipUnless(
        bool(os.getenv("RUN_LIVE_LLM_TESTS") and (os.getenv("GROQ_API_KEY") or config.GROQ_API_KEY)),
        "Live tests skipped. Set RUN_LIVE_LLM_TESTS=1 and ensure GROQ_API_KEY is configured to run live tests.",
    )
    def test_live_groq_invocation(self):
        chat = ChatLLM(llm_provider="groq", llm_model="llama-3.3-70b-versatile")
        response = chat.invoke("Reply with the single word: OK")
        self.assertIsNotNone(response)
        content = response.content if hasattr(response, "content") else str(response)
        self.assertIn("OK", content)


if __name__ == "__main__":
    unittest.main()
