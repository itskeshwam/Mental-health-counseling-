from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import os

def chatbot_response(request):
    if request.method == 'POST':
        client = OpenAI(api_key=os.getenv('key_b1iGCPMiKoRwHKzk'))
        user_input = request.POST.get('user_input')
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="gpt-5-nano",
        )
        chatbot_reply = response.choices[0].message.content 
        return JsonResponse({'reply': chatbot_reply})
    return render(request, 'chatbot/chat.html')