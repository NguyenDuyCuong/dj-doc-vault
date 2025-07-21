from django.shortcuts import render
from .chat import chat_completion

# Create your views here.
def chat_page(request):
    response = ""
    if request.method == "POST":
        user_msg = request.POST.get("message")
        response = chat_completion([{"role": "user", "content": user_msg}])
    return render(request, "chat/chat.html", {"response": response})