from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.


def index(request):
    """
    Render the index page.
    """
    page = loader.get_template("index.html")
    context = {
        "images": [{"name": "1"}],
    }
    return HttpResponse(page.render(context, request))
