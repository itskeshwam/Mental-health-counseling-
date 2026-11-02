import logging
import os

from django.http import JsonResponse
from django.shortcuts import render
from openai import APIError, OpenAI

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 4000


def chatbot_response(request):
    if request.method == "GET":
        return render(request, "chatbot/chat.html")

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed."}, status=405)

    user_input = (request.POST.get("user_input") or "").strip()
    if not user_input:
        return JsonResponse({"error": "Please enter a message."}, status=400)

    if len(user_input) > MAX_MESSAGE_LENGTH:
        return JsonResponse(
            {"error": f"Messages must be {MAX_MESSAGE_LENGTH} characters or fewer."},
            status=400,
        )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY is not configured.")
        return JsonResponse(
            {"error": "The chatbot is not configured. Please contact the administrator."},
            status=503,
        )

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5-nano"),
            messages=[{"role": "user", "content": user_input}],
        )
        chatbot_reply = response.choices[0].message.content
        if not chatbot_reply:
            logger.error("The OpenAI API returned an empty response.")
            return JsonResponse(
                {"error": "The chatbot could not generate a response. Please try again."},
                status=502,
            )
        return JsonResponse({"reply": chatbot_reply})
    except APIError:
        logger.exception("OpenAI API request failed.")
        return JsonResponse(
            {"error": "The chatbot service is temporarily unavailable. Please try again."},
            status=502,
        )
    except Exception:
        logger.exception("Unexpected chatbot error.")
        return JsonResponse(
            {"error": "An unexpected error occurred. Please try again."},
            status=500,
        )
