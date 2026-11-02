from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from openai import APIError

from .views import MAX_MESSAGE_LENGTH


@override_settings(DEBUG=True, ALLOWED_HOSTS=["testserver"])
class ChatbotResponseTests(TestCase):
    def test_get_renders_chat_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mental Health Support Chatbot")

    def test_empty_message_is_rejected(self):
        response = self.client.post("/", {"user_input": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_oversized_message_is_rejected(self):
        response = self.client.post(
            "/", {"user_input": "x" * (MAX_MESSAGE_LENGTH + 1)}
        )
        self.assertEqual(response.status_code, 400)

    @patch.dict("os.environ", {}, clear=True)
    def test_missing_api_key_returns_service_unavailable(self):
        response = self.client.post("/", {"user_input": "Hello"})
        self.assertEqual(response.status_code, 503)

    @patch("chatbot.views.OpenAI")
    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_successful_chat_response(self, openai_class):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="Hello."))
        ]
        openai_class.return_value = mock_client

        response = self.client.post("/", {"user_input": "Hello"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"reply": "Hello."})
        mock_client.chat.completions.create.assert_called_once()

    @patch("chatbot.views.OpenAI")
    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_openai_failure_returns_gateway_error(self, openai_class):
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = APIError(
            message="API unavailable", request=MagicMock(), body=None
        )
        openai_class.return_value = mock_client

        response = self.client.post("/", {"user_input": "Hello"})

        self.assertEqual(response.status_code, 502)
        self.assertIn("error", response.json())
