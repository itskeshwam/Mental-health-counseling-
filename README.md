# Mental Health Counseling Chatbot

A Django-based chat interface backed by the OpenAI Chat Completions API.

## Requirements

- Python 3.10–3.12 (Django 4.2 compatibility)
- An OpenAI API key

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Create a `.env` file in the repository root:

   ```dotenv
   DJANGO_SECRET_KEY=replace-with-a-long-random-secret
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_MODEL=gpt-5-nano
   ```

4. Run database migrations and start the development server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. Open http://127.0.0.1:8000/.

## Tests

Run the Django test suite:

```bash
python manage.py test
```

## Production configuration

Set a strong `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=False`, and configure `DJANGO_ALLOWED_HOSTS` with the actual host names. Enable secure cookies when serving over HTTPS by setting `DJANGO_SECURE_COOKIES=True`. Keep `.env` out of version control.

## Important

This project provides a conversational interface, not clinical care. It must not be presented as diagnosis, therapy, or a crisis-response service. Users in immediate danger should contact local emergency services or a qualified crisis resource.
