from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .forms import ContactForm

def contact(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        form = ContactForm()
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass
    else:
        raise NotImplementedError
    return render(request, "contact.html", {"form": form})